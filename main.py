import time
from machine import Pin, PWM
from time import sleep

# Designed by Fweiny TEST 

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

timestamp_prev_F = 0
timestamp_F = 0
btn_count_F =  0
off_count_F = True
# Mid
timestamp_minutes_prev_M = 0
timestamp_minutes_M = 0
btn_count_M = 0
off_count_M = True
# Back
timestamp_prev_B = 0
timestamp_B = 0
btn_count_B = 0
off_count_B = True




timecount = 0


# Start turn all off
LED_F.duty(0)
LED_M.duty(0)
LED_B.duty(0)




if __name__ == '__main__':


    while True:
        if btn_F.value() == 1:

            # get times
            timestamp_F =     	    time.localtime()[5]
            timestamp_minutes_F =   time.localtime()[4] * 60

            timestamp_F = timestamp_F + timestamp_minutes_M
            #print(f'{timestamp=}')

            # calc delta time
            t_delta = timestamp_F - timestamp_prev_F
            #print(f'{timestamp_prev=}')
            #print(f'{t_delta=}')

            # count number of clicks (depending on time delta)
            if t_delta > doppelklick_timer:
                btn_count = 0
            else:
                btn_count = btn_count + 1
            #print(f"{btn_count=}")
            
            #shutting on/off
            if (status_F is False) & (timecount == 0) & ( btn_count == 0 ):
                #duty_cycle = duty_cycle_start
                LED_F.duty(duty_cycle)
                # LED_B.duty(duty_cycle)
                # LED_M.duty(duty_cycle)

                print('Shut On - Front')
                status_F = True
            elif (status_F is True) & (timecount == 0) & ( btn_count == 0 ):
                #duty_cycle = 0
                LED_F.duty(0)
                print('Shut Off - Front')
                status_F = False
                if status_all == True:
                    print('all off - Single click')
                    status_all = False
            
            elif (t_delta <= doppelklick_timer) and (btn_count == 1) and (off_count is True):
                print('doppelklick - Front')
                
                if status_all is False:
                    print('all on')
                    status_F = True
                    status_all =True

                    
                    duty_cycle = duty_max
                    # LED_F.duty(duty_cycle)
                    # LED_B.duty(duty_cycle)
                    # LED_M.duty(duty_cycle)
                else:
                    print('all off')
                    status_all = False
                    # LED_F.duty(0)
                    # LED_B.duty(0)
                    # LED_M.duty(0)

 
            # Dimmen ------------------------------------------
            # print(f'{timecount=}')
            timecount = timecount + 1
            sleep(sleep_time)
            off_count = False

            if (timecount >= 200) and (status_F == True):
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
            timecount = 0
            off_count_F = True

            # reset timer for new klick
            timestamp_prev_F = timestamp_F

           
