import tkinter as tk
from tkinter import ttk
import os
import threading
from pathlib import Path
from guiIO import *
from model import TTSmodel, PreTTSmodel

class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.inputLabel = tk.Label(self, text="Voice Input:", font=('Arial', 12, "bold"))
        self.inputLabel.grid(row=0, column=0, sticky=tk.W, padx=10, pady=2)

        self.inputReady = tk.Label(self, text="NOT READY", font=('Arial', 12, "bold"))
        self.inputReady.grid(row=0, column=1, sticky=tk.W, padx=0, pady=2)


        self.outputLabel = tk.Label(self, text="Voice Output:", font=('Arial', 12, "bold"))
        self.outputLabel.grid(row=0, column=2, sticky=tk.W, padx=1, pady=2)

        self.outputReady = tk.Label(self, text="NOT READY", font=('Arial', 12, "bold"))
        self.outputReady.grid(row=0, column=3, sticky=tk.W, padx=0, pady=2)


        #self.rtfLabel = tk.Label(self, text="Previous RTF:", font=('Arial', 12, "bold"))
        #self.rtfLabel.grid(row=0, column=4, sticky=tk.W, padx=0, pady=2)

        #self.rtfReady = tk.Label(self, text="None", font=('Arial', 12, "bold"))
        #self.rtfReady.grid(row=0, column=5, sticky=tk.W, padx=0, pady=2)
        #self.progress_bar = ttk.Progressbar(self, mode='indeterminate')
        #self.progress_bar.grid(row=0, column=5, sticky=tk.W, padx=0, pady=2)


        self.textbox = tk.Text(self, font=('Arial', 24), wrap=tk.WORD, width=32, height=12)
        self.textbox.grid(row=1, column=0, rowspan=5, columnspan=6, padx=10, pady=2)


        self.b1 = tk.Button(self, text="Select Voice", font=('Arial', 18, "bold"), command=self.choiceButton, width=11, height=2)
        self.b1.grid(row=1, column=6, padx=10, pady=2)

        self.b3 = tk.Button(self, text="Process Text", font=('Arial', 18, "bold"), command=self.submitButton, width=11, height=2)
        self.b3.grid(row=2, column=6, padx=10, pady=5)

        self.b4 = tk.Button(self, text="Play Output", font=('Arial', 18, "bold"), command=self.playButton, width=11, height=2)
        self.b4.grid(row=3, column=6, padx=10, pady=5)

        self.b5 = tk.Button(self, text="Pre-Set Inputs", font=('Arial', 18, "bold"), command=self.presetButton, width=11, height=2)
        self.b5.grid(row=4, column=6, padx=10, pady=5)

        self.b6 = tk.Button(self, text="Help", font=('Arial', 18, "bold"), command=self.helpButton, width=11, height=2)
        self.b6.grid(row=5, column=6, padx=10, pady=5)


        self.geometry("800x480")
        self.title("Voice cloning")
        self.attributes("-fullscreen", False)

        self.inputWav = Path('/home/raffelm/Capstone/voice_subsystem/wav/voiceInput.wav')
        self.outputWav = Path('/home/raffelm/Capstone/voice_subsystem/wav/voiceOutput.wav')

        self.speaker_mode = "Personal"
        self.tts_model = TTSmodel(str(self.inputWav), str(self.outputWav))

        self.model_thread = None
        self.is_new_speaker = False
        #self.progress_thread = None

        self.update()


    def update(self):
        if self.inputWav.is_file():
            self.inputReady['text'] = "READY"
        else:
            self.inputReady['text'] = "NOT READY"

        if self.outputWav.is_file():
            self.outputReady['text'] = "READY"
            if self.model_thread is not None:
                self.model_thread.join()
            #if self.progress_thread is not None:
                #self.progress_bar.stop()
                #self.progress_thread.join()
        else:
            self.outputReady['text'] = "NOT READY"

        #self.rtfReady['text'] = str(self.tts_model.get_rtf())

        self.after(1000, self.update)


    def submitButton(self):
        if self.outputWav.is_file():
            os.remove('/home/raffelm/Capstone/voice_subsystem/wav/voiceOutput.wav')

        if self.inputWav.is_file():
            if(self.model_thread is None or not self.model_thread.is_alive()):
                self.model_thread = threading.Thread(target=self.tts_model.run, args=(self.textbox.get(1.0, tk.END),self.is_new_speaker))
                self.model_thread.start()
                self.is_new_speaker = False
                #self.progress_thread = threading.Thread(target=self.progress_bar.start)
                #self.progress_thread.start()


    def delayDestroy(self, recording, recordTime, count):
        recordTime['text'] = str(count)

        if count == 0:
            recording.destroy()
        else:
            recording.after(1000, self.delayDestroy, recording, recordTime, count-1)

    def set_pretrained_model(self, voice, choice_button):
        if self.speaker_mode != voice:
            self.speaker_mode = voice
        self.tts_model = PreTTSmodel(voice, self.outputWav)
        choice_button.destroy()

    def choiceButton(self):
        choice = tk.Toplevel()

        buttonActions = tk.Label(choice, text="Select a voice to clone from the options below:", font=('Arial', 14, "bold"))
        buttonActions.grid(row=0, column=0, columnspan=3, sticky=tk.W, padx=20, pady=2)

        k1 = tk.Button(choice, text="Personal Voice.", font=('Arial', 18, "bold"), command=lambda: self.recordButton(choice), width=56, height=2)
        k1.grid(row=1, column=0, columnspan=21, padx=20, pady=12)

        k1 = tk.Button(choice, text="Donald Trump Voice.", font=('Arial', 18, "bold"), command=lambda: self.set_pretrained_model("Trump", choice),width=56, height=2)
        k1.grid(row=2, column=0, columnspan=21, padx=20, pady=12)

        k1 = tk.Button(choice, text="Obiwan Kenobi Voice.", font=('Arial', 18, "bold"), command=lambda: self.set_pretrained_model("Obiwan", choice), width=56, height=2)
        k1.grid(row=3, column=0, columnspan=21, padx=20, pady=12)

        k1 = tk.Button(choice, text="David Attenborough Voice.", font=('Arial', 18, "bold"), command=lambda: self.set_pretrained_model("David", choice), width=56, height=2)
        k1.grid(row=4, column=0, columnspan=21, padx=20, pady=12)

        bClose = tk.Button(choice, text="X", font=('Arial', 8, "bold"), command=choice.destroy, width=3, height=1)
        bClose.grid(row=0, column=20, sticky=tk.E, padx=20, pady=10)

        choice.geometry("800x480")
        choice.title("Voice Select Window")
        choice.attributes("-fullscreen", True)


    def recordButton(self, choice_button):
        recording = tk.Toplevel()

        if self.speaker_mode != "Personal":
            self.speaker_mode = "Personal"
        self.tts_model = TTSmodel(str(self.inputWav), str(self.outputWav))
        self.is_new_speaker = True

        recordLabel = tk.Label(recording, text="Recording Time:", font=('Arial', 12, "bold"))
        recordLabel.grid(row=0, column=1, sticky=tk.W, padx=0, pady=2)

        recordTime = tk.Label(recording, text="15", font=('Arial', 12, "bold"))
        recordTime.grid(row=0, column=2, sticky=tk.W, padx=0, pady=2)

        k1 = tk.Button(recording, text="Try reading one of the example sentences below:", font=('Arial', 18, "bold"), width=56, height=2)
        k1.grid(row=1, column=0, columnspan=21, padx=20, pady=12)

        k1 = tk.Button(recording, text="The quick brown fox jumps over the lazy dog.", font=('Arial', 18, "bold"), width=56, height=2)
        k1.grid(row=2, column=0, columnspan=21, padx=20, pady=12)

        k1 = tk.Button(recording, text="With tenure, Suzie'd have all the more leisure for yachting,\nbut her publications are no good.", font=('Arial', 18, "bold"), width=56, height=2)
        k1.grid(row=3, column=0, columnspan=21, padx=20, pady=12)

        k1 = tk.Button(recording, text="The beige hue on the waters of the loch impressed\nall, including the French queen, before she heard\nthat symphony again, just as young Arthur wanted.", font=('Arial', 18, "bold"), width=56, height=3)
        k1.grid(row=4, column=0, columnspan=21, padx=20, pady=12)

        recording.geometry("800x480")
        recording.title("Recording Window")
        recording.attributes("-fullscreen", True)

        p = subprocess.Popen([sys.executable, './record.py'])

        self.delayDestroy(recording, recordTime, 10)
        choice_button.destroy()


    def playButton(self):
        play_audio2()


    def clearBox(self, window):
        self.textbox.delete('1.0', tk.END)
        window.destroy()

    def preset1(self, preset):
        self.textbox.delete('1.0', tk.END)
        self.textbox.insert('1.0', "The quick brown fox jumps over the lazy dog")
        preset.destroy()

    def preset2(self, preset):
        self.textbox.delete('1.0', tk.END)
        self.textbox.insert('1.0', "The quick brown fox jumps over the lazy dog")
        preset.destroy()

    def preset3(self, preset):
        self.textbox.delete('1.0', tk.END)
        self.textbox.insert('1.0', "The quick brown fox jumps over the lazy dog")
        preset.destroy()

    def preset4(self, preset):
        self.textbox.delete('1.0', tk.END)
        self.textbox.insert('1.0', "According to all known laws of aviation there is no way a bee should be able to fly")
        preset.destroy()

    def presetButton(self):
        preset = tk.Toplevel()

        k1 = tk.Button(preset, text="The quick brown fox jumps over the lazy dog", font=('Arial', 18, "bold"), width=50, height=2, command=lambda: self.preset1(preset))
        k1.grid(row=1, column=0, columnspan=21, padx=20, pady=12)

        k2 = tk.Button(preset, text="The quick brown fox jumps over the lazy dog", font=('Arial', 18, "bold"), width=50, height=2, command=lambda: self.preset2(preset))
        k2.grid(row=2, column=0, columnspan=21, padx=20, pady=12)

        k3 = tk.Button(preset, text="The quick brown fox jumps over the lazy dog", font=('Arial', 18, "bold"), width=50, height=2, command=lambda: self.preset3(preset))
        k3.grid(row=3, column=0, columnspan=21, padx=20, pady=12)

        k4 = tk.Button(preset, text="According to all known laws of aviation\n there is no way a bee should be able to fly", font=('Arial', 18, "bold"), width=50, height=2, command=lambda: self.preset4(preset))
        k4.grid(row=4, column=0, columnspan=21, padx=20, pady=12)

        bClose = tk.Button(preset, text="X", font=('Arial', 8, "bold"), command=preset.destroy, width=3, height=1)
        bClose.grid(row=0, column=22, padx=0, pady=10)

        preset.geometry("800x480")
        preset.title("Preset Window")
        preset.attributes("-fullscreen", True)


    def helpButton(self):
        help = tk.Toplevel()

        buttonActions = tk.Label(help, text="Keyboard Button Actions:", font=('Arial', 14, "bold"))
        buttonActions.grid(row=0, column=0, columnspan=3, sticky=tk.W, padx=20, pady=2)

        buttonDesc = tk.Label(help, text="Keyboard functions as a 10 key", font=('Arial', 12, "bold"))
        buttonDesc.grid(row=1, column=0, columnspan=3, sticky=tk.W, padx=20, pady=0)

        buttonDesc2 = tk.Label(help, text="e.g. press button ABC 3 times to input a C", font=('Arial', 12, "bold"))
        buttonDesc2.grid(row=2, column=0, columnspan=3, sticky=tk.W, padx=20, pady=0)

        k1 = tk.Button(help, text="ABC", font=('Arial', 18, "bold"), width=7, height=3)
        k1.grid(row=3, column=0, padx=20, pady=10)

        k2 = tk.Button(help, text="DEF", font=('Arial', 18, "bold"), width=7, height=3)
        k2.grid(row=3, column=1, padx=5, pady=10)

        k3 = tk.Button(help, text="GHI", font=('Arial', 18, "bold"), width=7, height=3)
        k3.grid(row=3, column=2, padx=20, pady=10)

        k4 = tk.Button(help, text="JKL", font=('Arial', 18, "bold"), width=7, height=3)
        k4.grid(row=4, column=0, padx=20, pady=10)

        k5 = tk.Button(help, text="MNO", font=('Arial', 18, "bold"), width=7, height=3)
        k5.grid(row=4, column=1, padx=5, pady=10)

        k6 = tk.Button(help, text="PQR", font=('Arial', 18, "bold"), width=7, height=3)
        k6.grid(row=4, column=2, padx=20, pady=10)

        k7 = tk.Button(help, text="STUV", font=('Arial', 18, "bold"), width=7, height=3)
        k7.grid(row=5, column=0, padx=20, pady=10)

        k8 = tk.Button(help, text="WXYZ", font=('Arial', 18, "bold"), width=7, height=3)
        k8.grid(row=5, column=1, padx=5, pady=10)

        k9 = tk.Button(help, text="Space\nBack", font=('Arial', 18, "bold"), width=7, height=3)
        k9.grid(row=5, column=2, padx=20, pady=10)

        bClear = tk.Button(help, text="Clear Textbox", font=('Arial', 18, "bold"), width=15, height=3, command=lambda: self.clearBox(help))
        bClear.grid(row=3, column=3, padx=20, pady=10)

        bClose = tk.Button(help, text="X", font=('Arial', 8, "bold"), command=help.destroy, width=3, height=1)
        bClose.grid(row=0, column=4, padx=20, pady=10)

        help.geometry("800x480")
        help.title("Help Window")
        help.attributes("-fullscreen", True)

gui = GUI()
gui.mainloop()
