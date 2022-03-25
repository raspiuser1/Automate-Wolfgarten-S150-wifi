# Automate-Wolfgarten-S150-wifi
Automate your wolfgarten S300 lawn mower with an arduino ESP8266 wifi module and Control it via google Agenda

Setup a google calender api: https://developers.google.com/calendar/api
and get your ID and credentials file.

Install Arduino sketch:
Set your ip and dns first if need in the INO file and Upload the arduino sketch esp8266.ino to your ESP8266, I used a NODE MCU 1.0.
The best is to set a static ip. In this example we are using 192.168.1.122 you can change it both in  esp8266.ino and robotmaaier_command.py 

How it works:
There is a webserver running at the arduino which controls 2 outputs.
1 output for the start knob and 1 for the stop button as there are only 2 buttons on the S315 wolfgarten.
The outputs are connected to a arduino relay board which is connected to the buttons.
This arduino will go into your lawn mower and simply press the buttons with the proper delay for it.

make a dir like: /script/google-kalender and upload the robotmaaier.py and wakeup file to your raspi or ubuntu system and run it via a crontab (change paths).
crontab line:
@reboot sleep 10 && /script/google-kalender/wakeup /script/google-kalender/robotmaaier.py
The wakeup file will always start the python script if it fails, the script will check the google calenderevery 60 seconds

from the google calender setup you received a credentials.json file which you have to put in the same directory as the script.
change the Calender ID in the script (line 59) according to your used calender, I made a new layer for this one.


A video will be posted soon
