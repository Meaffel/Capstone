#Reading shift reg
import time
import keyboard
import RPi.GPIO as GPIO
import spidev

pload = 29
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pload, GPIO.OUT)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000

waitTime = 1000000000 #(ns)

timer = 0

spinput = []

keyTimes = [0, 0, 0, 0, 0, 0, 0, 0, 0]
prevKeyS = [0, 0, 0, 0, 0, 0, 0, 0, 0]
keyState = [0, 0, 0, 0, 0, 0, 0, 0, 0]
keyCodes = [[0,64],
            [0,8],
            [0,1],
            [1,128],
            [0,16],
            [0,2],
            [2,0],
            [0,32],
            [0,4]]

#keyChars = [['a', 'b', 'c'],
#            ['d', 'e', 'f'],
#            ['g', 'h', 'i'],
#            ['j', 'k', 'l'],
#            ['m', 'n', 'o'],
#            ['p', 'q', 'r'],
#            ['s', 't', 'u', 'v'],
#            ['w', 'x', 'y', 'z'],
#            ['space', '/b']]

keyChars = [['s', 't', 'u', 'v'],
            ['j', 'k', 'l'],
            ['a', 'b', 'c'],
            ['w', 'x', 'y', 'z'],
            ['m', 'n', 'o'],
            ['d', 'e', 'f'],
            ['space', '\b'],
            ['p', 'q', 'r'],
            ['g', 'h', 'i']]

def clearTimes(i):
    j = 0
    while (j < 9):
        if (j != i):
            keyTimes[j] = 0
        j = j + 1

def keyPress(i):
    if prevKeyS[i] == 1:
        return()

    prevKeyS[i] = 1
    
    prevTime = keyTimes[i]
    keyTimes[i] = time.time_ns()

    if (keyTimes[i] - prevTime > waitTime):
        keyboard.send(keyChars[i][0])
        keyState[i] = 1
        return()
    
    k = len(keyChars[i])
    
    for j in range (0, k):
        if (keyState[i] == j):
            if (keyChars[i][j] != 'space'):
                keyboard.send('\b')
            keyboard.send(keyChars[i][j])
            if (keyState[i] == k-1):
                keyState[i] = 0
            else:
                keyState[i] = keyState[i]+1
            return()


while (not keyboard.is_pressed('1')):
    GPIO.output(pload, GPIO.LOW)
    GPIO.output(pload, GPIO.HIGH)
    spinput = spi.readbytes(2)

    timer = time.time_ns()

    i = 0
    while (i < 9):
        tempSpi = [spinput[0] & keyCodes[i][0], spinput[1] & keyCodes[i][1]]
        if (tempSpi == keyCodes[i]):
            clearTimes(i)
            keyPress(i)
        else:
            prevKeyS[i] = 0
        i = i + 1

GPIO.cleanup()
