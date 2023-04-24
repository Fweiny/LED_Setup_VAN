import time
from machine import Pin, PWM

# Pin constants
FRONT_LED_PIN = 17
MID_LED_PIN = 16
BACK_LED_PIN = 2
FRONT_BTN_PIN = 22
MID_BTN_PIN = 19
BACK_BTN_PIN = 34

# PWM constants
PWM_FREQUENCY = 800
PWM_DUTY_CYCLE_START = 800
PWM_DUTY_CYCLE_MAX = 800
PWM_STEP = 25
PWM_DIMM_SLEEP_TIME = 0.1

# Button constants
BUTTON_DOUBLE_CLICK_TIME = 1
BUTTON_TRIPLE_CLICK_TIME = 2

# LED states
LED_OFF = 0
LED_ON = 1
LED_DIMMING = 2

# LED objects
front_led = PWM(Pin(FRONT_LED_PIN), PWM_FREQUENCY)
mid_led = PWM(Pin(MID_LED_PIN), PWM_FREQUENCY)
back_led = PWM(Pin(BACK_LED_PIN), PWM_FREQUENCY)

# Button objects
front_btn = Pin(FRONT_BTN_PIN, Pin.IN, Pin.PULL_DOWN)
mid_btn = Pin(MID_BTN_PIN, Pin.IN, Pin.PULL_DOWN)
back_btn = Pin(BACK_BTN_PIN, Pin.IN, Pin.PULL_DOWN)

# State variables
front_led_state = LED_OFF
mid_led_state = LED_OFF
back_led_state = LED_OFF
led_all_on = False
front_btn_state = LED_OFF
mid_btn_state = LED_OFF
back_btn_state = LED_OFF
front_btn_last_click_time = 0
mid_btn_last_click_time = 0
back_btn_last_click_time = 0
front_btn_click_count = 0
mid_btn_click_count = 0
back_btn_click_count = 0
front_led_duty_cycle = PWM_DUTY_CYCLE_START
mid_led_duty_cycle = PWM_DUTY_CYCLE_START
back_led_duty_cycle = PWM_DUTY_CYCLE_START
dimm_timer = 0

def handle_button_click(btn_pin, led_pin, led_state, last_click_time, click_count):
    current_time = time.monotonic()
    delta_time = current_time - last_click_time
    if delta_time > BUTTON_TRIPLE_CLICK_TIME:
        click_count = 0
    else:
        click_count += 1
        
    if click_count == 1:
        if led_state == LED_OFF:
            led_pin.duty(front_led_duty_cycle)
            led_state = LED_ON
        elif led_state == LED_ON:
            led_pin.duty(0)
            led_state = LED_OFF
            if led_all_on:
                led_all_on = False
        elif led_state == LED_DIMMING:
            led_state = LED_ON
    elif click_count == 2:
        if led_all_on:
            led_pin.duty(0)
            led_all_on = False
        else:
            front_led.duty(PWM_DUTY_CYCLE_MAX)
            mid_led.duty(PWM_DUTY_CYCLE_MAX)
            back_led.duty(PWM_DUTY_CYCLE_MAX)
            led_all_on = True
    elif click_count == 3:
        led_pin.duty(0)
        led_state = LED_OFF
        led_all_on = False
    return led_state, click_count, current_time

while True:
    # Handle front button click
    if front_btn.value() == 1:
        front_led_state, front_btn_click_count, front_btn_last_click_time = handle_button_click(
            front_btn, front_led, front_led_state, front_btn_last_click_time, front_btn_click_count)
    else:
        front_btn_click_count = 0

    # Handle mid button click
    if mid_btn.value() == 1:
        mid_led_state, mid_btn_click_count, mid_btn_last_click_time = handle_button_click(
            mid_btn, mid_led, mid_led_state, mid_btn_last_click_time, mid_btn_click_count)
    else:
        mid_btn_click_count = 0

    # Handle back button click
    if back_btn.value() == 1:
        back_led_state, back_btn_click_count, back_btn_last_click_time = handle_button_click(
            back_btn, back_led, back_led_state, back_btn_last_click_time, back_btn_click_count)
    else:
        back_btn_click_count = 0

    # Handle LED dimming
    if front_led_state == LED_DIMMING:
        dimm_timer += 1
        if dimm_timer >= 200:
            front_led_duty_cycle -= PWM_STEP
            if front_led_duty_cycle < 0:
                front_led_duty_cycle = 0
            elif front_led_duty_cycle > PWM_DUTY_CYCLE_MAX:
                front_led_duty_cycle = PWM_DUTY_CYCLE_MAX
            front_led.duty(front_led_duty_cycle)
            print("Front LED duty cycle:",front_led_duty_cycle)