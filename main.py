import time
from machine import Pin, PWM
from time import sleep

# Designed by Fweiny TEST 

# LED_F settings
frequency = 800

LED_F = PWM(Pin(17), frequency)  #front 17
LED_M = PWM(Pin(16), frequency)  # 16 Mid
LED_B = PWM(Pin(2), frequency) #Back 2

# LED_F = LED_M = LED_B

duty_cycle = 800
duty_cycle_start = 800
duty_max = 800

btn_F = Pin(22, Pin.IN, Pin.PULL_DOWN) # front 22
btn_M = Pin(19, Pin.IN, Pin.PULL_DOWN) # Mid 19
btn_B = Pin(34, Pin.IN, Pin.PULL_DOWN) #bak 15

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
timestamp_s_prev = 0
timestamp_s = 0
timestamp_s_M_prev = 0
timestamp_s_M = 0
btn_count = 0
btn_count_M = 0
off_count = True



timecount = 0

LED_F.duty(0)
LED_M.duty(0)
LED_B.duty(0)

t_delta = 10




if __name__ == '__main__':


    while True:
        if btn_F.value() == 1:

            # get times
            timestamp_s = time.localtime()[5]
            timestamp_m = time.localtime()[4] * 60

            timestamp_s = timestamp_s + timestamp_m
            #print(f'{timestamp_s=}')

            # calc delta time
            t_delta = timestamp_s - timestamp_s_prev
            #print(f'{timestamp_s_prev=}')
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

                #trippelklick
                # if (t_delta <= doppelklick_timer) and (btn_count == 2) and (off_count is True):
                #     print('Trippleklick - Button 1')
                #     print('all off')
                #     duty_cycle = duty_max
                #     LED_F.duty(duty_cycle)
                #     #status_F = False


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


                # if (duty_cycle == 1000) or (duty_cycle == 0):
                #   print('reverse')
                #  step = -step

            #print("----------------")

        else:
            #reset dimm counter 
            timecount = 0
            off_count = True

            # reset timer for new klick
            timestamp_s_prev = timestamp_s

            
            # print(duty_cycle)
            # sleep(.1)


        if btn_M.value() == 1:

            # get times
            timestamp_s_M = time.localtime()[5]
            timestamp_m_M = time.localtime()[4] * 60

            timestamp_s_M = timestamp_s_M + timestamp_m_M
            #print(f'{timestamp_s=}')

            # calc delta time
            t_delta_M = timestamp_s_M - timestamp_s_M_prev
            #print(f'{timestamp_s_prev=}')
            #print(f'{t_delta_M=}')

            # count number of clicks (depending on time delta)
            if t_delta_M > doppelklick_timer:
                btn_count_M = 0
            else:
                btn_count_M = btn_count_M + 1
            #print(f"{btn_count_M=}")
            
            #shutting on/off
            if (status_M is False) & (timecount_M == 0) & ( btn_count_M == 0 ):
                #duty_cycle = duty_cycle_start
                # LED_F.duty(duty_cycle)
                LED_B.duty(duty_cycle)
                LED_M.duty(duty_cycle)

                print('Shut On - Back')
                status_M = True
            elif (status_M is True) & (timecount_M == 0) & ( btn_count_M == 0 ):
                #duty_cycle = 0
                # LED_F.duty(0)
                LED_B.duty(0)
                LED_M.duty(0)
                print('Shut Off - BacK')
                status_M = False
                if status_all == True:
                    print('all off - Single click')
                    status_all = False
            
            elif (t_delta_M <= doppelklick_timer) and (btn_count_M == 1) and (off_count_M is True):
                print('doppelklick - Front')
                
                if status_all is False:
                    print('all on')
                    status_M = True
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
                    

                #trippelklick
                # if (t_delta <= doppelklick_timer) and (btn_count_M == 2) and (off_count_M is True):
                #     print('Trippleklick - Button 1')
                #     print('all off')
                #     duty_cycle = duty_max
                #     LED_F.duty(duty_cycle)
                #     #status_M = False


            # Dimmen ------------------------------------------
            # print(f'{timecount_M=}')
            timecount_M = timecount_M + 1
            sleep(sleep_time)
            off_count_M = False

            if (timecount_M >= 200) and (status_M == True):
                #print('Dimmen')
                print(duty_cycle)
                
                
                duty_cycle = duty_cycle - step
                LED_M.duty(duty_cycle)
                LED_B.duty(duty_cycle)

                sleep(dimm_sleep_time)

                if duty_cycle > duty_max: #ensure no issue with max duty
                    duty_cycle = duty_max

                if (duty_cycle == abs(step)) or (duty_cycle == duty_max): # Flip at 0 or 100%
                    sleep(1)
                    step = - step
                    print('return')


                # if (duty_cycle == 1000) or (duty_cycle == 0):
                #   print('reverse')
                #  step = -step

            #print("----------------")

        else:
            #reset dimm counter 
            timecount_M = 0
            off_count_M = True

            # reset timer for new klick
            timestamp_s_M_prev = timestamp_s_M

            
            # print(duty_cycle)
            # sleep(.1)

