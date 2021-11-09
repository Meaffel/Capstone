from itertools import permutations

import torch

from espnet2.enh.loss.criterions.abs_loss import AbsEnhLoss
from espnet2.enh.loss.wrappers.abs_wrapper import AbsLossWrapper

class PITSolver(AbsLossWrapper):
    def __init__(self, criterion:AbsEnhLoss):
        super().__init__()
        self.criterion = criterion
    
    def forward(self, ref, inf, perm=None):
        """
        Args:
            ref (List[torch.Tensor]): [(batch, ...), ...] x n_spk
            inf (List[torch.Tensor]): [(batch, ...), ...]
        
        Returns:
            loss: (torch.Tensor): minimum loss with the best permutation
            stats: dict, for collecting training status
            others: dict, in this PIT solver, permutation order will be returned 
        """

        assert len(ref) == len(inf), (len(ref), len(inf))
        num_spk = len(ref)

        def pair_loss(permutation):
            return sum(
                [self.criterion(ref[s], inf[t]) for s, t in enumerate(permutation)]
            ) / len(permutation)

        if perm is None:
            device = ref[0].device
            all_permutations = list(permutations(range(num_spk)))
            losses = torch.stack([pair_loss(p) for p in all_permutations], dim=1)
            loss, perm = torch.min(losses, dim=1)
            perm = torch.index_select(
                torch.tensor(all_permutations, device=device, dtype=torch.long),
                0,
                perm,
            )
        else:
            loss = torch.tensor(
                [
                    torch.tensor(
                        [
                            self.criterion(
                                ref[s][batch].unsqueeze(0), inf[t][batch].unsqueeze(0)
                            )
                            for s, t in enumerate(p)
                        ]
                    ).mean()
                    for batch, p in enumerate(perm)
                ]
            )
        
        loss = loss.mean()

        stats = dict()
        stats[self.criterion.name] = loss.detach()

        return loss.mean(), stats, {'perm': perm}

