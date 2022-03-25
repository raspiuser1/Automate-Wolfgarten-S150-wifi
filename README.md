# Automate-Wolfgarten-S150-wifi
Automate your wolfgarten S300 lawn mower with an arduino ESP8266 wifi module and Control it via google Agenda

Setup a google calender api: https://developers.google.com/calendar/api
and get your ID and credentials file.

Install Arduino sketch:
Set your ip and dns first if need in the INO file and Upload the arduino sketch esp8266.ino to your ESP8266, I used a NODE MCU 1.0.
The best is to set a static ip. In this example we are using 192.168.1.122 you can change it both in  esp8266.ino and robotmaaier_command.sh

How it works:
There is a webserver running at the arduino which controls 2 outputs.
1 output for the start knob and 1 for the stop button as there are only 2 buttons on the S315 wolfgarten.
The outputs are connected to a arduino relay board which is connected to the buttons.
This arduino will go into your lawn mower and simply press the buttons with the proper delay for it.

make a dir like: /script/google-kalender and upload all the files of this repo into it and run it via a crontab.
crontab line:
@reboot sleep 10 && /script/google-kalender/wakeup /script/google-kalender/robotmaaier.py

The wakeup file will always start the python script if it fails, the script will check the google calenderevery 60 seconds

from the google calender setup you received a credentials.json file which you have to put in the same directory as the script.
the token.pickle file will be created when the script is started the first time.
change the Calender ID in the script (line 59) according to your used calender, I made a new layer for this one so its seperated from my standard agenda.

how does it work?:
the script listens for the word START or STOP which must be set into your calender, so when you start an event with the word START at 12:00 the lawn mower will start at that point. for example set it for 5mins that will do so from 12:00 to 12:05, it will now do the standard mowing (2,5 hours) when the battery is fully charged.
when START or STOP is met the script will run the shell script robotmaaier_command.sh, which translates it to a command which is compatible with our arduino webserver.

why is there a seperated shell file?
that's because you can run it from home automation software or manually without the need of the google agenda.
you can find an example command in the shell file.



A video will be posted soon
