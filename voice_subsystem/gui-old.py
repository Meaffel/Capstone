import tkinter as tk
import os
import subprocess
from pathlib import Path
from guiIO import *

END = tk.END

inputWav = Path('/home/raffelm/capstone/Capstone/voice_subsystem/wav/voiceInput.wav')
outputWav = Path('/home/raffelm/capstone/Capstone/voice_subsystem/wav/voiceOutput.wav')

def update():
    
    if inputWav.is_file():
        inputReady['text'] = "READY"
    else:
        inputReady['text'] = "NOT READY"
    
    if outputWav.is_file():
        outputReady['text'] = "READY"
    else:
        outputReady['text'] = "NOT READY"
    
    root.after(1000, update)
    
def submitButton():
    if outputWav.is_file():
        os.remove('/home/raffelm/capstone/Capstone/voice_subsystem/wav/voiceOutput.wav')
    p = subprocess.Popen([sys.executable, './generate_clone.py', textbox.get(1.0, END)])#,
                      #stdout=subprocess.PIPE,
                      #stderr=subprocess.STDOUT)
                      
def delayDestroy(recording, recordTime, count):
    recordTime['text'] = str(count)
    
    if count == 0:
        recording.destroy()
    else:
        recording.after(1000, delayDestroy, recording, recordTime, count-1)
        
def recordButton():
    recording = tk.Toplevel()

    recordLabel = tk.Label(recording, text="Recording Time:", font=('Arial', 12, "bold"))
    recordLabel.grid(row=0, column=1, sticky=tk.W, padx=0, pady=2)

    recordTime = tk.Label(recording, text="12", font=('Arial', 12, "bold"))
    recordTime.grid(row=0, column=2, sticky=tk.W, padx=0, pady=2)
    
    k1 = tk.Button(recording, text="Try reading one of the example sentences below:", font=('Arial', 18, "bold"), width=50, height=2)
    k1.grid(row=1, column=0, columnspan=21, padx=20, pady=12)
    
    k1 = tk.Button(recording, text="The quick brown fox jumps over the lazy dog.", font=('Arial', 18, "bold"), width=50, height=2)
    k1.grid(row=2, column=0, columnspan=21, padx=20, pady=12)
    
    k1 = tk.Button(recording, text="With tenure, Suzie'd have all the more leisure for yachting,\nbut her publications are no good.", font=('Arial', 18, "bold"), width=50, height=2)
    k1.grid(row=3, column=0, columnspan=21, padx=20, pady=12)
    
    k1 = tk.Button(recording, text="The beige hue on the waters of the loch impressed\nall, including the French queen, before she heard\nthat symphony again, just as young Arthur wanted.", font=('Arial', 18, "bold"), width=50, height=3)
    k1.grid(row=4, column=0, columnspan=21, padx=20, pady=12)
    
    recording.geometry("800x480")
    recording.title("recording Window")
    recording.attributes("-fullscreen", True)
    
    record_audio(12)
    
    delayDestroy(recording, recordTime, 12)

def playButton():
    play_audio2()
    
def clearBox(window):
    textbox.delete('1.0', END)
    window.destroy()
    
def preset1(preset):
    textbox.delete('1.0', END)
    textbox.insert('1.0', "The quick brown fox jumps over the lazy dog")
    preset.destroy()
    
def preset2(preset):
    textbox.delete('1.0', END)
    textbox.insert('1.0', "The quick brown fox jumps over the lazy dog")
    preset.destroy()
    
def preset3(preset):
    textbox.delete('1.0', END)
    textbox.insert('1.0', "The quick brown fox jumps over the lazy dog")
    preset.destroy()
    
def preset4(preset):
    textbox.delete('1.0', END)
    textbox.insert('1.0', "According to all known laws of aviation there is no way a bee should be able to fly")
    preset.destroy()

def presetButton():
    preset = tk.Toplevel()
    
    k1 = tk.Button(preset, text="The quick brown fox jumps over the lazy dog", font=('Arial', 18, "bold"), width=50, height=2, command=lambda: preset1(preset))
    k1.grid(row=1, column=0, columnspan=21, padx=20, pady=12)
    
    k2 = tk.Button(preset, text="The quick brown fox jumps over the lazy dog", font=('Arial', 18, "bold"), width=50, height=2, command=lambda: preset2(preset))
    k2.grid(row=2, column=0, columnspan=21, padx=20, pady=12)
    
    k3 = tk.Button(preset, text="The quick brown fox jumps over the lazy dog", font=('Arial', 18, "bold"), width=50, height=2, command=lambda: preset3(preset))
    k3.grid(row=3, column=0, columnspan=21, padx=20, pady=12)
    
    k4 = tk.Button(preset, text="According to all known laws of aviation\n there is no way a bee should be able to fly", font=('Arial', 18, "bold"), width=50, height=2, command=lambda: preset4(preset))
    k4.grid(row=4, column=0, columnspan=21, padx=20, pady=12)
    
    bClose = tk.Button(preset, text="X", font=('Arial', 8, "bold"), command=preset.destroy, width=3, height=1)
    bClose.grid(row=0, column=22, padx=0, pady=10)
    
    preset.geometry("800x480")
    preset.title("Preset Window")
    preset.attributes("-fullscreen", True)

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
    
    k7 = tk.Button(help, text="STUV", font=('Arial', 18, "bold"), width=7, height=3)
    k7.grid(row=5, column=0, padx=20, pady=10)
    
    k8 = tk.Button(help, text="WXYZ", font=('Arial', 18, "bold"), width=7, height=3)
    k8.grid(row=5, column=1, padx=5, pady=10)
    
    k9 = tk.Button(help, text="Space\nBack", font=('Arial', 18, "bold"), width=7, height=3)
    k9.grid(row=5, column=2, padx=20, pady=10)
    
    bClear = tk.Button(help, text="Clear Textbox", font=('Arial', 18, "bold"), width=15, height=3, command=lambda: clearBox(help))
    bClear.grid(row=3, column=3, padx=20, pady=10)
    
    bClose = tk.Button(help, text="X", font=('Arial', 8, "bold"), command=help.destroy, width=3, height=1)
    bClose.grid(row=0, column=4, padx=20, pady=10)
    
    help.geometry("800x480")
    help.title("Help Window")
    help.attributes("-fullscreen", True)


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

b5 = tk.Button(root, text="Pre-Set Inputs", font=('Arial', 18, "bold"), command=presetButton, width=11, height=2)
b5.grid(row=4, column=6, padx=10, pady=5)

b6 = tk.Button(root, text="Help", font=('Arial', 18, "bold"), command=helpButton, width=11, height=2)
b6.grid(row=5, column=6, padx=10, pady=5)


root.geometry("800x480")
root.title("Voice cloning")
root.attributes("-fullscreen", True)


update()

root.mainloop()
