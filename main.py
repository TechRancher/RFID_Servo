"""
    RFID Card Reader To Control A Servo.
    Author: Jason Sikes AKA The Tech Rancher
    Version: 1.0
    Date Coded: 10/02/2023
    Description: This circuit reads data from the RFID RC522 and Reads the position value of the SG90 Servo and displays either Locked or Unlocked status on the SSD1306 Display along with one of two LED's will light up. Red LED for Locked status or Green LED status for Unlocked. The MC is a Raspberry Pi Pico W.
    License: MIT License
"""
# Import Libraries
from micropython import const
from machine import Pin, PWM, SPI, I2C, soft_reset
from ssd1306 import SSD1306_I2C
from mfrc522 import MFRC522
import utime as time

# Variable
servo_Pin = const(15)
dsp_sda_Pin = const(4)
dsp_scl_Pin = const(5)
i2c_freq = const(400000)
dsp_Width = const(128)
dsp_Heigh = const(64)
rfid_sck_Pin = const(10)
rfid_mosi_Pin = const(11)
rfid_miso_Pin = const(12)
rfid_cs_Pin = const(13)
rfid_rst_Pin = const(0)
red_LED_Pin = const(14)
green_LED_Pin = const(9)
isLocked = True
Lock_State = 0

# Create Objects
i2c = I2C(0,scl=Pin(dsp_scl_Pin), sda=Pin(dsp_sda_Pin), freq=i2c_freq)
dsp = SSD1306_I2C(dsp_Width, dsp_Heigh, i2c) # This is the SSD display Object

servo = PWM(Pin(servo_Pin))
servo.freq(50)
servo.duty_u16()

reader = MFRC522(sck=rfid_sck_Pin, mosi=rfid_mosi_Pin, miso=rfid_miso_Pin,cs=rfid_cs_Pin, rst=rfid_rst_Pin, spi_id=1) # This is the RC522 Object

LED_Red = Pin(red_LED_Pin, Pin.OUT)
LED_Green = Pin(green_LED_Pin, Pin.OUT)

# Functions
def centerText(txt):
    """
        This will center text on the SSD1306
        Argument txt is the text that you want to be centered
    """
    text = (len(txt) *8) /2
    mid = 64 - text
    return int(mid)

def setLock(Locked):
    """
        Argument Locked - True or False - If True - run the block of code that will unlock and display data on SSD1306 along with LED status.
        If False - run the else block of code to lock servo and display the data on the SSD1306 along with LED status
    """
    global LED_Red
    global LED_Green
    if Locked:
        servo.duty_u16(1638)
        LED_Red.value(0)
        LED_Green.value(1)
        unlockMsg = f"Unlocked"
        dsp.text(unlockMsg,centerText(unlockMsg),16,1)
        dsp.show()
            
    else:
        servo.duty_u16(8191)
        LED_Red.value(1)
        LED_Green.value(0)
        lockMsg = f"Locked"
        dsp.text(lockMsg,centerText(lockMsg),16,1)
        dsp.show()

def LED_Status(servo_stat,redLED,greenLED):
    """
        Takes Arguments servo_stat, redLED, and greenLED.
        servo_stat - The object servo.duty_u16() data
        redLED - The Red LED object
        greenLED - The Green LED object
        On Start of the program the servo.duty_u16() value is read and based off the data the correct LED will be turned on.
    """
    redLED = LED_Red
    greenLED = LED_Green
    servo_stat = servo.duty_u16()
    if servo_stat == 8191:
        redLED.value(1)
        greenLED.value(0)
    else:  
        redLED.value(0)
        greenLED.value(1)

dsp.fill(0)
dsp.show() # This will clear anything on the SSD1306 Display

try:
    while True:
        reader.init() # Starts up the RC522

        LED_Status(servo,LED_Red,LED_Green) # Read the value from servo.duty_u16 to see if the servo is in lock or unlock to display LED lights

        lockStatusMsg = f"{'Locked' if servo.duty_u16() == 8191 else 'Unlocked'}"   # Displays if the servo is in lock or unlock position on start
        
        msg = f"Card To Reader"
        dsp.text(msg,centerText(msg),0,1)
        dsp.text(lockStatusMsg, centerText(lockStatusMsg),16,1)
        dsp.show() # Displays the message of Read Card and Lock status

        (stat, tag_type) = reader.request(reader.REQIDL) # Access the address to read the data on the card
        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN() # Read the data from the card to see if it matches the required card to use with RC522
            if stat == reader.OK:
                dsp.fill(0)
                card = int.from_bytes(bytes(uid), "little", False) # type: ignore
                # Takes the Hexadecimal and turns it into small "little" bytes to be used.
                print(str(card)) # Prints to Terminal the card bytes number
                msg1 = f"Card Id: {str(card)}"
                dsp.text(msg,centerText(msg),0,1)
                dsp.text(msg1,0,8,1)
                dsp.show() # Displays messages to the SSD1306

                if str(card) == "60198054": # Looks for this card number.
                    if servo.duty_u16() == 8191: # servo SG90 uses 8191 to be 180 degrees and 1638 to be 0 degrees
                        setLock(True)
                        time.sleep(2)
                    else:
                        setLock(False)
                        time.sleep(2)
                elif str(card) == "2166693146": # Change this if you want to read another card to control the servo
                    if servo.duty_u16() == 8191:
                        setLock(True)
                        time.sleep(2)
                    else:
                        setLock(False)
                        time.sleep(2)
        time.sleep_ms(500)
except KeyboardInterrupt:
    dsp.fill(0) # Clears the SSD1306 display
    dsp.show()
    LED_Green.off()
    LED_Red.off()
    soft_reset() # Resets the Pico W MC
