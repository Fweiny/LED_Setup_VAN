import time
from machine import Pin, PWM
from time import sleep

#functions
def Btn_function(LED,btn_on_time):          
    global doppelklick, duty_cycle
    #print(f'{LED.duty()=}')

    #shutting on/off
    if (doppelklick is False) & (btn_on_time == 0):
        if (LED.duty() == 0):
            print('Lights on - Single')
            #duty_cycle = duty_cycle_start
            LED.duty(duty_cycle)
        else:
            print('Lights off - Single')
            LED.duty(0)      
    elif (btn_on_time == 0):
        doppelklick = False
        if (LED.duty() == 0):
            print("All off")
            LED_F.duty(0)
            LED_M.duty(0)
            LED_B.duty(0)
        else:
            print("All on")
            LED_F.duty(duty_cycle)
            LED_M.duty(duty_cycle)
            LED_B.duty(duty_cycle)
   
    return LED_B,LED_F,LED_M


def get_timestamp():
    Seconds =   time.localtime()[5]
    Minutes =   time.localtime()[4] * 60
    timestamp = Seconds + Minutes
    return timestamp

def dimmen():
    global duty_cycle,step
    print(f'Dimmen from {duty_cycle}% to {(duty_cycle-step)}')
    # Change duty 
    duty_cycle = duty_cycle - step

    if (LED_F.duty() > 0):
        LED_F.duty(duty_cycle)

    if (LED_M.duty() > 0):
        LED_M.duty(duty_cycle)

    if (LED_B.duty() > 0):
        LED_B.duty(duty_cycle)

    sleep(dimm_sleep_time)

    if duty_cycle > duty_max: #ensure no issue with max duty
        duty_cycle = duty_max

    if (duty_cycle == abs(step)) or (duty_cycle == duty_max): # Flip at 0 or 100%
        sleep(1)
        step = - step
        print('return')
    return duty_cycle, step

# LED_F settings
frequency = 800
duty_cycle = 800
duty_max = 800


LED_F = PWM(Pin(17), frequency)         # Front Pin 17
LED_M = PWM(Pin(16), frequency)         # Mid   Pin 16
LED_B = PWM(Pin(2), frequency)          # Back  Pin 2


#Button definition
btn_F = Pin(22, Pin.IN, Pin.PULL_DOWN) # Front  Pin 22
btn_M = Pin(19, Pin.IN, Pin.PULL_DOWN) # Mid    Pin 19
btn_B = Pin(34, Pin.IN, Pin.PULL_DOWN) # Back   Pin 15


# Dimm settings
sleep_time = .01            # Sleep on timer
dimm_sleep_time = .1        # Timer for dimming
step = 25                   # PWM step for dimming
doppelklick_timer = 1       # Break between klicks
doppelklick = False         # Req. 

# start timer - default
t_delta = 10
timestamp_prev_F = get_timestamp()
timestamp_F = get_timestamp()
btn_count_F = 0
off_count_F = True
btn_on_time_F = 0


# Start turn all off as start up
LED_F.duty(0)
LED_M.duty(0)
LED_B.duty(0)

#LED_Dict={LED_F:"Front",LED_B:"Back",LED_M:"Mid"}


if __name__ == '__main__':
    while True:

        if btn_F.value() == 1:
            if off_count_F is True:
                print("---------------------")
                timestamp_F = get_timestamp()  # get timestmap 
                t_delta = timestamp_F - timestamp_prev_F # calc delta time
                #print(f'{t_delta=}')

                # count number of clicks (depending on time delta)
                if (t_delta <= doppelklick_timer) and (btn_count_F == 1):
                    print('Doppelklick')
                    doppelklick = True  # indication for doppelklick
                    btn_count_F = 0     # reset button count
                elif (btn_count_F == 0): # increase for buttun push
                    btn_count_F = 1

            #print(f"{btn_count=}")

            #Button fuctnion
            Btn_function(LED_F,btn_on_time_F)
 
            # Dimmen ------------------------------------------
            if (btn_on_time_F >= 100):
                dimmen()

            btn_on_time_F = btn_on_time_F + 1   # increasing depending on Actuator on time  # noqa: E501
            off_count_F = False                 # ensuring on time
            sleep(sleep_time)                   # delay 
        else:
            btn_on_time_F = 0                   # reset dimm counter 
            off_count_F = True
            timestamp_prev_F = timestamp_F       # reset timer for new klick

           
