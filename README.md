# Automate Wolfgarten S150 robot lawn mower via wifi<br />
Link of this repo: https://github.com/raspiuser1/Automate-Wolfgarten-S150-wifi<br />
Automate your wolfgarten S300 Robot lawn mower with an arduino ESP8266 wifi module and Control it via google Agenda<br />

Setup a google calender api: <br />
https://developers.google.com/calendar/api<br />
https://developers.google.com/calendar/api/quickstart/python<br />
and get your calender ID and credentials.json file which i needed in this project.<br />

Install Arduino sketch:<br />
Set your ip and dns first if need in the INO file and Upload the arduino sketch esp8266.ino to your ESP8266, I used a NODE MCU 1.0.<br />
The best is to set a static ip. In this example we are using 192.168.1.122 you can change it both in  esp8266.ino and robotmaaier_command.sh<br />
I translated already some commands from dutch into english. you can change it to your own language.<br />

How it works:<br />
There is a webserver running at the arduino which controls 2 outputs.<br />
1 output for the start knob and 1 for the stop button as there are only 2 buttons on the S315 wolfgarten.<br />
The outputs are connected to a arduino relay board which is connected to the buttons.<br />
This arduino will go into your lawn mower and simply press the buttons with the proper delay for it.<br />

make a dir like: /script/google-kalender and upload all the files of this repo into it and run it via a crontab. <br />
run command: sudo crontab -e<br />
and copy/paste the line below:<br />
@reboot sleep 10 && /script/google-kalender/wakeup /script/google-kalender/robotmaaier.py<br />
The wakeup file will always start the python script if it fails, the script will check the google calenderevery 60 seconds<br />

from the google calender setup you received a credentials.json file which you have to put in the same directory as the script.<br />
the token.pickle file will be created when the script is started the first time.<br />
change the Calender ID in the script (line 59) according to your used calender, I made a new layer for this one so its seperated from my standard agenda.<br />

how does it work?:<br />
the script listens for the word START or STOP which must be set into your calender, so when you start an event with the word START at 12:00 the lawn mower will start<br /> at that point. for example set it for 5mins that will do so from 12:00 to 12:05, it will now do the standard mowing (2,5 hours) when the battery is fully charged.<br />
when START or STOP is met the script will run the shell script robotmaaier_command.sh, which translates it to a command which is compatible with our arduino webserver.<br />

why is there a seperated shell file?<br />
that's because you can run it from home automation software, a website or manually without the need of the google agenda.<br />

Terminal commands are: <br />
#stop and go to the base station:<br />
robotmaaier_command.sh noodstop.home<br />

#just stop and stay where you are:<br />
robotmaaier_command.sh grasmaaier.uit<br />

#normal mowing (2,5 hours)<br />
robotmaaier_command.sh normale.maaibeurt<br />

#short mowing (1 hour)<br />
robotmaaier_command.sh korte.maaibeurt<br />

#childlock on<br />
robotmaaier_command.sh kinderslot.aan<br />

#childlock off<br />
robotmaaier_command.sh kinderslot.uit<br />

#mowing when childlock on<br />
robotmaaier_command.sh maaien.met.kinderslot<br />



A video will be posted soon<br />
