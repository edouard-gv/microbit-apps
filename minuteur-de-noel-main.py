# Imports go at the top
from microbit import *
import power

global timer
global beepFrame
global timerLaunched
global lum
global frame
is_sound_on = False

TIMER_INC = 60
TIMER_DELAY = 1000
FRAME_FREQ = 5

def switch_sound():
    global is_sound_on
    is_sound_on = not is_sound_on
    if is_sound_on:
        display.show(Image.MUSIC_QUAVER, wait=False)
    else:
        display.show(Image.NO, wait=False)

def raz(razTimer = True):
    global timer
    global beepFrame
    global timerLaunched
    global lum
    global frame
    
    if razTimer:
        timer = 0
    beepFrame = 5
    lum = 0
    timerLaunched = False
    frame = 0
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

    if pin_logo.is_touched():
        raz()
    
    if button_b.was_pressed():
        switch_sound()

    if button_a.was_pressed():
        raz(False)
        if timer == 0:
            timer = TIMER_INC/2 + 5
        elif timer < 36:
            timer = timer + TIMER_INC/2
        else:
            timer = (timer + TIMER_INC) % (4*TIMER_INC);
        timerLaunched = True;

    if timerLaunched:
            if timer > 0:
                if frame == 0:
                    display.clear()
                    print_time(timer)
                    timer = timer - 1
                
                frame = (frame + 1) % FRAME_FREQ
                sleep(1000/FRAME_FREQ)
        
            else:
                display.show(Image.HEART)
                if is_sound_on:
                    audio.play(Sound.GIGGLE)
                sleep(1000)
                raz()
                power.deep_sleep(wake_on=button_a)

            
    else:
        display.set_pixel(2, 2, abs(lum-9))
        sleep(70)
        lum = (lum + 1) % 18


        
            
        
        
    

