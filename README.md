# RC522 Card Reader Control SG90 Servo
 RFID Card Reader To Control A Servo.
Author: Jason Sikes AKA [The Tech Rancher](https://www.youtube.com/@TheTechRancher)

Version: 1.0

Date Coded: 10/02/2023

Description: This circuit reads data from the RFID RC522 Reads the position value of the SG90 Servo and displays either Locked or Unlocked status on the SSD1306 Display along with one of two LEDs will light up—red LED for Locked status or a Green LED status for Unlocked. The MC is a Raspberry Pi Pico W.

License: [MIT License](https://github.com/TechRancher/RFID_Servo/blob/main/LICENSE)

## Wiring Diagram
![Wire Diagram](wiringDiagram.jpg)

## Include Libraries
You will need to include Libraries:
ssd1306.py
mfrc522.py

These libraries will need to be stored on the Raspberry Pi Pico W. I stored mine under lib. Pico W will look by default in the lib for any added libraries that the main.py would have asked to import.

## Code You Must Change
In order for your reader to make the servo and LEDs work you must change the card numbers to match your card number.
Look at line 124:
``` Python
if str(card) == "60198054": # Looks for this card number.
``` 
The number in the " "needs to be changed to match your card numbers. You can get your card number from the print()
Line 119
```Python
print(str(card)) # Prints to Terminal the card bytes number
```
