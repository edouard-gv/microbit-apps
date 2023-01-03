# Imports go at the top
from microbit import *
import power

global timer
global beepFrame
global timerLaunched
global lum

TIMER_INC = 60
TIMER_DELAY = 1000

def raz(razTimer = True):
    global timer
    global beepFrame
    global timerLaunched
    global lum
    
    if razTimer:
        timer = 0
    beepFrame = 5
    lum = 0
    timerLaunched = False  
    display.clear()

def print_time(timer):
    remaining_sec = (timer - 1) % 10 + 1
    tens = ((timer - 1) % 60) // 10
    mins = (timer - 1) // 60

    for i in range(mins):
        display.set_pixel(i, 0, 7)

    for i in range(tens):
        display.set_pixel(i, 1, 7)

    if remaining_sec > 5:
        for i in range(remaining_sec-5):
            display.set_pixel(i, 3, 7)
    
    for i in range(min(remaining_sec, 5)):
        display.set_pixel(i, 4, 7)
        


raz()

while True:
    if button_b.was_pressed():
        raz()
    
    clicks = button_a.get_presses()
    if clicks > 0:
        if timer < 30:
            clicks = clicks - 0.5
        raz(False)
        timer = (TIMER_INC*clicks+timer) % (4*TIMER_INC);
        timerLaunched = True;

    if timerLaunched:
        if timer > 0:
            display.clear()
            print_time(timer)
            timer = timer - 1
            sleep(TIMER_DELAY)

        else:
            display.show(Image.HEART)
            audio.play(Sound.GIGGLE)
            sleep(1000)
            raz()
            power.off()
    else:
        display.set_pixel(2, 2, abs(lum-9))
        sleep(70)
        lum = (lum + 1) % 18
        
            
        
        
    

