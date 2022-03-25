/*
 * 
out3 = stop knob
out2 = start knob
https://github.com/raspiuser1/Automate-Wolfgarten-S300-wifi/
set to static ip like: http://192.168.1.122
 */

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include "config.h"

ESP8266WebServer server(80);

void handleRoot() {
  server.send(200, "text/plain", "Robotmaaier");
}

#define MAX_DATA_LENGTH 100
#define MAX_DATA_LENGTH2 4
uint16_t signal_data[MAX_DATA_LENGTH];
int current_data_length = -1;
int current_data_length2 = -1;
String signal_data2[MAX_DATA_LENGTH2];
int slot = 0;

void readCSV(String s) {
  int numStart = 0;
  current_data_length = 0;
  current_data_length2 = 0;
 if (s.length() == 4 ) {  
  signal_data2[0] = s.toInt();
 }
  for (int i = 0; i <= s.length(); ++i) {
    if ( (s.charAt(i) == ',') || ( i == (s.length()) )) {
      signal_data[current_data_length++] = s.substring(numStart, i).toInt();
      numStart = i + 1;
    }
  }
}

void kinderslot(){
          digitalWrite(out3, LOW); 
          digitalWrite(out2, LOW); 
          delay(6000);
          digitalWrite(out3, HIGH);
          digitalWrite(out2, HIGH);
}

void handlePlay() {
  String response = "POSTED";
  response += server.arg("timings");
  readCSV(server.arg("timings"));
  //Serial.println(signal_data2[0]);
  if (signal_data2[0].length() == 4 ) {

    //out3 = go knop
    //out2 = stop/home knop
    // 4x 0 dus 0000 mag niet
      if (signal_data2[0] == "7777") {
          digitalWrite(out3, LOW); 
          delay(1000);
          digitalWrite(out3, HIGH);
          Serial.println("Normal mode"); 
      }
      if (signal_data2[0] == "1111") {
          digitalWrite(out3, LOW); 
          delay(500);
          digitalWrite(out3, HIGH);
          delay(300);
          digitalWrite(out3, LOW); 
          delay(500);
          digitalWrite(out3, HIGH);
          Serial.println("Short mowing (max 60min)"); 
      }      
      if (signal_data2[0] == "2222") {
          digitalWrite(out2, LOW); 
          delay(1000);
          digitalWrite(out2, HIGH);
          Serial.println("STOP and go to base"); 
      }
      if (signal_data2[0] == "3333") {
          digitalWrite(out3, LOW); 
          delay(2000);
          digitalWrite(out3, HIGH);
          Serial.println("turn off"); 
      }      
      if (signal_data2[0] == "4444") {
          if (slot == 0){
          // hier is het kinderslot uit
          kinderslot();
          // nu is het aan
          slot = 1;
          Serial.println("Childlock on"); 
         }
      }
      if (signal_data2[0] == "6666") {
          if (slot == 1){
          kinderslot();
          // nu is het uit
          slot = 0;
          Serial.println("Childlock off"); 
         }
      }
                
      if (signal_data2[0] == "5555" && slot == 1) {
          digitalWrite(out2, LOW); 
          delay(1000);
          digitalWrite(out3, LOW); 
          delay(1000);
          digitalWrite(out3, HIGH);
          digitalWrite(out2, HIGH);
          Serial.println("Start with childlock"); 
      }  
      
  for (int i = 0; i < current_data_length; ++i) {
      Serial.println(signal_data[i]);
      //Serial.println(signal_data2[i]);
   }
  }
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.send(200, "text/plain", response);
}




void handleNotFound(){
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET)?"GET":"POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i=0; i<server.args(); i++){
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
}

void setup(void){
  Serial.begin(115200);

  while (!Serial)  // Wait for the serial connection to be establised.
    delay(50);
  Serial.println();
  pinMode(out1, OUTPUT);
 pinMode(out2, OUTPUT);
  pinMode(out3, OUTPUT);
   pinMode(out4, OUTPUT);
    pinMode(out5, OUTPUT);
     pinMode(out6, OUTPUT);
     digitalWrite(out1, HIGH); 
     digitalWrite(out2, HIGH); 
     digitalWrite(out3, HIGH); 
     digitalWrite(out4, HIGH); 
     digitalWrite(out5, HIGH); 
     digitalWrite(out6, HIGH); 
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASSWORD);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(SSID);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("esp8266")) {
    Serial.println("MDNS responder started");
  }

  server.on("/", handleRoot);
  server.on("/play", HTTP_POST, handlePlay);

  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void){
  server.handleClient();
}
