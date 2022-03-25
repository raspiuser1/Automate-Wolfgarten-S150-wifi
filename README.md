# Automate-Wolfgarten-S150-wifi
Automate your wolfgarten S300 lawn mower with an arduino ESP8266 wifi module and Control it via google Agenda

Ïnstall Arduino sketch:
Set your ip and dns first if need in the INO file and Upload the arduino sketch esp8266.ino to your ESP8266, I used a NODE MCU 1.0.
The best is to set a static ip.

How it works:
There is a webserver running at the arduino which controls 2 outputs.
1 output for the start knob and 1 for the stop button as there are only 2 buttons on the S315 wolfgarten.
The outputs are connected to a arduino relay board which is connected to the buttons.
This arduino will go into your lawn mower and simply press the buttons with the proper delay for it.
