import tkinter as tk
import subprocess
from pathlib import Path
from guiIO import *

END = tk.END

def update():    
    inputWav = Path('./voiceInput.wav')
    outputWav = Path('./voiceOutput.wav')
    
    if inputWav.is_file():
        inputReady['text'] = "READY"
    else:
        inputReady['text'] = "NOT READY"
    
    if outputWav.is_file():
        outputReady['text'] = "READY"
    else:
        outputReady['text'] = "NOT READY"
    
    root.after(250, update)
    
def submitButton():
    textFile = open("outText.txt", "w")
    textFile.write(textbox.get(1.0, END))
    textFile.close()
    p = subprocess.Popen([sys.executable, './examplechild.py', "/home/jetson/Desktop/voiceInput.wav", "/home/jetson/Desktop/outtext.txt", "arg3"],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)

def recordButton():
    record_audio(7)

def playButton():
    play_audio()

def helpButton():
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
    
    k7 = tk.Button(help, text="STU", font=('Arial', 18, "bold"), width=7, height=3)
    k7.grid(row=5, column=0, padx=20, pady=10)
    
    k8 = tk.Button(help, text="VWX", font=('Arial', 18, "bold"), width=7, height=3)
    k8.grid(row=5, column=1, padx=5, pady=10)
    
    k9 = tk.Button(help, text="YZ", font=('Arial', 18, "bold"), width=7, height=3)
    k9.grid(row=5, column=2, padx=20, pady=10)
    
    bClose = tk.Button(help, text="X", font=('Arial', 8, "bold"), command=help.destroy, width=3, height=1)
    bClose.grid(row=0, column=3, padx=20, pady=10)
    
    help.geometry("800x480")
    help.title("Help Window")
    #help.attributes("-fullscreen", True)


root = tk.Tk()

inputLabel = tk.Label(root, text="Voice Input:", font=('Arial', 12, "bold"))
inputLabel.grid(row=0, column=0, sticky=tk.W, padx=10, pady=2)

inputReady = tk.Label(root, text="NOT READY", font=('Arial', 12, "bold"))
inputReady.grid(row=0, column=1, sticky=tk.W, padx=0, pady=2)


outputLabel = tk.Label(root, text="Voice Output:", font=('Arial', 12, "bold"))
outputLabel.grid(row=0, column=4, sticky=tk.W, padx=1, pady=2)

outputReady = tk.Label(root, text="NOT READY", font=('Arial', 12, "bold"))
outputReady.grid(row=0, column=5, sticky=tk.W, padx=0, pady=2)


textbox = tk.Text(root, font=('Arial', 24), wrap=tk.WORD, width=32, height=12)
textbox.grid(row=1, column=0, rowspan=5, columnspan=6, padx=10, pady=2)


b1 = tk.Button(root, text="Record Voice", font=('Arial', 18, "bold"), command=recordButton, width=11, height=2)
b1.grid(row=1, column=6, padx=10, pady=2)

b3 = tk.Button(root, text="Process Text", font=('Arial', 18, "bold"), command=submitButton, width=11, height=2)
b3.grid(row=2, column=6, padx=10, pady=5)

b4 = tk.Button(root, text="Play Output", font=('Arial', 18, "bold"), command=playButton, width=11, height=2)
b4.grid(row=3, column=6, padx=10, pady=5)

b5 = tk.Button(root, text="Pre-Set Inputs", font=('Arial', 18, "bold"), width=11, height=2)
b5.grid(row=4, column=6, padx=10, pady=5)

b6 = tk.Button(root, text="Help", font=('Arial', 18, "bold"), command=helpButton, width=11, height=2)
b6.grid(row=5, column=6, padx=10, pady=5)


root.geometry("800x480")
root.title("Voice cloning")
#root.attributes("-fullscreen", True)


update()

root.mainloop()