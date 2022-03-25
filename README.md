# Automate Wolfgarten S150 robot lawn mower via wifi<br />
Link of this repo: https://github.com/raspiuser1/Automate-Wolfgarten-S150-wifi<br />
Automate your wolfgarten S300 Robot lawn mower with an arduino ESP8266 wifi module and Control it via google Agenda<br />

I bought this lawnmower in the summer of 2021 for about 250 euros, now at the time of writing its doubled in price...anyway a wifi version of wolfgarten was much more expensive so I decided to make it work via wifi in a cheaper way. <br />
First of all: make sure you have wifi in your garden :) <br />


## What hardware do you need?
- ESP8266 NODE MCU1.0<br />
https://www.amazon.com/ESP8266/s?k=ESP8266  <br />

- 5volt arduino relay module 2 channel (not solid state relay) <br />
https://www.amazon.com/s?k=arduino+relay+module+2+channel&crid=2APUU5MFMHU4O&sprefix=arduino+relay+module+2+channel%2Caps%2C155&ref=nb_sb_noss<br />

- voltage regulator for the ESP8266, the esp needs 5 volts like. voltage regulator like: <br />
https://www.amazon.com/Converter-DROK-Regulator-Inverter-Transformer/dp/B01NALDSJ0/ref=sr_1_9?crid=2CER2UD56BQ36&keywords=voltage+regulator+5v&qid=1648233451&sprefix=voltage+regulator+5%2Caps%2C169&sr=8-9<br />

connect D1 (out2 = start knob) and D6 (out3 = stop knob) to the relay board, and power the relay board with 5 volt<br />
next thing is to located the wires from both knobs on the mower, the video will show you. you have to connect the relays to the knobs to make it work.

## How it works
There is a webserver running at the arduino which controls 2 outputs.<br />
1 output for the start knob and 1 for the stop button as there are only 2 buttons on the wolfgarten s150.<br />
The outputs are connected to a arduino relay board which is connected to the buttons.<br />
This arduino will go into your lawn mower and simply press the buttons with the proper delay for it.<br />

## Setup a google calendar api
https://developers.google.com/calendar/api<br />
https://developers.google.com/calendar/api/quickstart/python<br />
and get your calendar ID and credentials.json file which i needed in this project.<br />
Change the Calendar ID in the script (line 59 robotmaaier.py) according to your used calendaer, I made a new layer for this one so its seperated from my standard agenda.<br />

## Arduino sketch
Set your ip and dns first in the arduino sketch esp8266.ino and change your wifi details in config.h, then Upload the sketch to your ESP8266.<br />
The best is to set a static ip, in this example we are using 192.168.1.122. If you are using another ip make the changes in both esp8266.ino and robotmaaier_command.sh<br />
I translated already some commands from dutch into english. you can change it to your own language (google translate).<br />


Make a folder like: /script/google-kalender and upload all the files of this repo into it and run it via a crontab. <br />
run command: sudo crontab -e<br />
and copy/paste the line below:<br />
@reboot sleep 10 && /script/google-kalender/wakeup /script/google-kalender/robotmaaier.py<br />
The wakeup file will always start the python script if it fails, the script robotmaaier.py will check the google calenderevery 60 seconds<br />
It should work with python2 or higher.<br />

from the google calender setup you received a credentials.json file which you have to put in the same directory as the script.<br />
the token.for the fist time you have to run the script manually like (sudo python2.8 robotmaaier.py) because you have to setup things first. a pickle file will be created after the setup which will be loaded into the script on reboot. If nothing goes wrong during the setup you can make the reboot and crontab will load the script automatically.<br />


##T he script
the script listens for the word START or STOP which must be set into your calender, so when you start an event with the word START at 12:00 the lawn mower will start<br /> at that point. for example set it for 5mins that will do so from 12:00 to 12:05, it will now do the standard mowing (2,5 hours) when the battery is fully charged.<br />
when START or STOP is met the script will run the shell script robotmaaier_command.sh, which translates it to a command which is compatible with our arduino webserver.<br />

## Why is there a seperated shell file
that's because you can run it from home automation software, a website or manually without the need of the google agenda. ofcourse google agenda needs this file to send the proper commands<br />

## Terminal commands
- stop and go to the base station:<br />
robotmaaier_command.sh noodstop.home<br />

- just stop and stay where you are:<br />
robotmaaier_command.sh grasmaaier.uit<br />

- normal mowing (2,5 hours)<br />
robotmaaier_command.sh normale.maaibeurt<br />

- short mowing (1 hour)<br />
robotmaaier_command.sh korte.maaibeurt<br />

- childlock on<br />
robotmaaier_command.sh kinderslot.aan<br />

- childlock off<br />
robotmaaier_command.sh kinderslot.uit<br />

- mowing when childlock on<br />
robotmaaier_command.sh maaien.met.kinderslot<br />



## A video will be posted soon
