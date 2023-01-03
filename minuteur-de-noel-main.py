# Imports go at the top
from microbit import *
import power

global timer
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

def raz():
    global timer
    global timerLaunched
    global lum
    global frame
    
    timer = 0
    frame = 0
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

    force_refresh = False
    if pin_logo.is_touched():
        raz()
        power.deep_sleep(wake_on=button_a)
    
    if button_b.was_pressed():
        switch_sound()

    if button_a.was_pressed():
        if timer == 0:
            timer = TIMER_INC/2 + 5
        elif timer <= TIMER_INC/2 + 5:
            timer = timer + TIMER_INC/2
        else:
            timer = (timer + TIMER_INC) % (4*TIMER_INC);
        timerLaunched = True;
        force_refresh = True;

    if timerLaunched:
            if timer > 0:
                if frame == 0 or force_refresh:
                    display.clear()
                    print_time(timer + (1 if force_refresh and frame != 0 else 0))
                    if frame == 0:
                        timer = timer - 1
                    force_refresh = False
                
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


        
            
        
        
    

