# Imports go at the top
from microbit import *
import power

global timer
global timerLaunched
global lum
global frame
global show_sound_status
is_sound_on = False

TIMER_INC = 60
TIMER_DELAY = 1000
FRAME_FREQ = 5
MAX_MINS = 10

def switch_sound():
    global is_sound_on
    global show_sound_status
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
    global show_sound_status
    global sound_switch_frame
    
    timer = 0
    frame = 0
    lum = 0
    timerLaunched = False
    show_sound_status = False
    sound_switch_frame = 0
    display.clear()

def clean_shutdown():
    display.show(Image.HEART)
    sleep(1000)
    raz()
    power.deep_sleep(wake_on=button_a)

def print_time(timer):
    remaining_sec = (timer - 1) % 10 + 1
    tens = ((timer - 1) % 60) // 10
    mins = (timer - 1) // 60

    if mins > 5:
        for i in range(mins-5):
            display.set_pixel(i, 0, 7)
    
    for i in range(min(mins,5)):
        display.set_pixel(i, 1, 7)

    for i in range(tens):
        display.set_pixel(i, 2, 4)

    if remaining_sec > 5:
        for i in range(remaining_sec-5):
            display.set_pixel(i, 3, 7)
    
    for i in range(min(remaining_sec, 5)):
        display.set_pixel(i, 4, 7)
        

raz()

while True:

    force_refresh = False
    if accelerometer.was_gesture('shake'): 
        clean_shutdown()
    
    if pin_logo.is_touched() and not show_sound_status:
        switch_sound()
        if timer == 0:
            sleep(2/3*1000)
            display.clear()
        else:
            show_sound_status = True
            sound_switch_frame = frame

    if button_a.was_pressed():
        if timer == 0:
            timer = TIMER_INC/2 + 5
        elif timer <= TIMER_INC/2 + 5:
            timer = timer + TIMER_INC/2
        else:
            timer = (timer + TIMER_INC) % ((MAX_MINS+1)*TIMER_INC)
        timerLaunched = True;
        force_refresh = True;

    if button_b.was_pressed():
        if timer <= TIMER_INC/2:
            clean_shutdown()
        elif timer <= TIMER_INC:
            timer = timer - TIMER_INC/2
        else:
            timer = timer - TIMER_INC
        force_refresh = True;

    if timerLaunched:
            if timer > 0:
                if (frame == 0 and not show_sound_status) or force_refresh:
                    display.clear()
                    print_time(timer + (1 if force_refresh and frame != 0 else 0))
                    force_refresh = False
                if frame == 0:
                    timer = timer - 1
                
                frame = (frame + 1) % FRAME_FREQ
                sleep(1000/FRAME_FREQ)

                if show_sound_status and frame == (sound_switch_frame+(2/3*FRAME_FREQ) // 1) % FRAME_FREQ :
                    show_sound_status = False
                    force_refresh = True
        
            else:
                if is_sound_on:
                    audio.play(Sound.GIGGLE)
                clean_shutdown()
    else:
        display.set_pixel(2, 2, abs(lum-9))
        sleep(70)
        lum = (lum + 1) % 18