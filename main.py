import time
from machine import Pin, PWM
from time import sleep

#functions

def get_timestamp():
    Seconds =     	    time.localtime()[5]
    Minutes =   time.localtime()[4] * 60
    timestamp = Seconds + Minutes
    return timestamp



# LED_F settings
frequency = 800


LED_F = PWM(Pin(17), frequency)  #front 17
LED_M = PWM(Pin(16), frequency)  # 16 Mid
LED_B = PWM(Pin(2), frequency) #Back 2

duty_cycle = 800
duty_cycle_start = 800
duty_max = 800

#Button definition
btn_F = Pin(22, Pin.IN, Pin.PULL_DOWN) # front 22
btn_M = Pin(19, Pin.IN, Pin.PULL_DOWN) # Mid 19
btn_B = Pin(34, Pin.IN, Pin.PULL_DOWN) #bak 15


#status of the lights 
status_all = False # LED all 
status_F = False  #LED status_F
status_M = False  #LED status_F
status_B = False  #LED status_F


sleep_time = .01

# Dimm settings
dimm_sleep_time = .1 # timer for dimming
step = 25 #PWM step for dimming
doppelklick_timer = 1 # break between klicks

# start timer - default
t_delta = 10

timestamp_prev_F = get_timestamp()
timestamp_F = get_timestamp()
btn_count_F = 0
off_count_F = True
btn_on_time_F = 0






# Start turn all off
LED_F.duty(0)
LED_M.duty(0)
LED_B.duty(0)



if __name__ == '__main__':


    while True:
        if btn_F.value() == 1:

            # get timestmap 
            timestamp_F = get_timestamp()
            #print(f'{timestamp=}')

            # calc delta time
            t_delta = timestamp_F - timestamp_prev_F

            #print(f'{timestamp_prev=}')
            #print(f'{t_delta=}')

            # count number of clicks (depending on time delta)
            if t_delta > doppelklick_timer:
                btn_count = 0
            else:
                doppelklick = True  # indication for doppelklick
                btn_count = btn_count + 1

            #print(f"{btn_count=}")
            
            #shutting on/off
            if (status_F is False) & (btn_on_time_F == 0) & ( btn_count_F == 0 ):
                print('Shut On - Single - Front')
                #duty_cycle = duty_cycle_start
                LED_F.duty(duty_cycle)
                status_F = True
            elif (status_F is True) & (btn_on_time_F == 0) & ( btn_count_F == 0 ):
                print('Shut Off - Single- Front')
                
                LED_F.duty(0)
                status_F = False

                # if status_all == True:
                #     print('all off - Single click')
                #     status_all = False 
            elif (doppelklick is True) and (btn_count_F == 1) and (off_count_F is True):
                print('doppelklick - Front')

                if status_F is True:
                    print("All on")
                    status_F = True
                    status_B = True
                    status_M = True
                else:
                    print("All off")
                    status_F = False
                    status_B = False
                    status_M = False

                    LED_F.duty(0)
                    LED_M.duty(0)
                    LED_B.duty(0)


        


 
            # Dimmen ------------------------------------------
            # print(f'{btn_on_time_F=}')
            btn_on_time_F = btn_on_time_F + 1
            sleep(sleep_time)
            off_count = False


            if (btn_on_time_F >= 200) and (status_F == True):
                #print('Dimmen')
                print(duty_cycle)
                
                
                duty_cycle = duty_cycle - step
                LED_F.duty(duty_cycle)

                sleep(dimm_sleep_time)

                if duty_cycle > duty_max: #ensure no issue with max duty
                    duty_cycle = duty_max

                if (duty_cycle == abs(step)) or (duty_cycle == duty_max): # Flip at 0 or 100%
                    sleep(1)
                    step = - step
                    print('return')
        else:
            #reset dimm counter 
            btn_on_time_F = 0
            off_count_F = True

            # reset timer for new klick
            timestamp_prev_F = timestamp_F

           
