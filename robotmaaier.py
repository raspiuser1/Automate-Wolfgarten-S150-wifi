#!/usr/bin/env python2
from __future__ import print_function
import datetime
import time
from time import gmtime, strftime, localtime
import pickle
import os
import commands
from datetime import datetime as dt
from dateutil.parser import parse as dtparse
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys

# If modifying these scopes, delete the file token.pickle.

temp1 = 2
tel = 0
def restart():
        print("argv was",sys.argv)
        print("sys.executable was", sys.executable)
        print("restart now")
        os.execv(sys.executable, ['python'] + sys.argv)
        
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
while SCOPES:
 try:   
  #def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('/script/google-kalender/token.pickle'):
        with open('/script/google-kalender/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/script/google-kalender/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('/script/google-kalender/token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    creds.refresh(Request())
    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #print('Getting the upcoming 10 events')
    #events_result = service.events().list(calendarId='primary', timeMin=now, #voor de standaard kalender
    #ID lampen kalender: 1hgvgpvv9rcqrb2nk42vvl653g@group.calendar.google.com
    #ID wakeuplight kabelnder: ifhi8jte80ead8ujjlq1nbb1ng@group.calendar.google.com
    events_result = service.events().list(calendarId='s0cmm0ukgqfptp4uhjadn0evc8@group.calendar.google.com', timeMin=now,
                                        maxResults=1, singleEvents=True,
                                        orderBy='startTime').execute()
    #events = events_result.get('items', [])
    events = events_result.get('items', [])

    for event in events:
        creds.refresh(Request()) 
        eventEndStr = event['end']['dateTime']
        eventstartStr = event['start']['dateTime']
    #Date section of the string
        dateStr = eventEndStr[:19]
        dateStr2 = eventstartStr[:19]
    #Offset section of the string
        offsetStr = eventEndStr[19:]
        offsetHours = int(offsetStr[1:3])
        offsetMinutes = int(offsetStr[4:])
        offsetSign = offsetStr[:1]

        offsetStr2 = eventstartStr[19:]
        offsetHours2 = int(offsetStr2[1:3])
        offsetMinutes2 = int(offsetStr2[4:])
        offsetSign2 = offsetStr2[:1]
    #Current date in UTC
        currentTime = datetime.datetime.utcnow()
        #currentTime = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    #Get end date in local time and offset
        endDate = datetime.datetime.strptime(dateStr, '%Y-%m-%dT%H:%M:%S')
        offset = datetime.timedelta(hours=offsetHours, minutes=offsetMinutes)

        StartDate = datetime.datetime.strptime(dateStr2, '%Y-%m-%dT%H:%M:%S')
        offset2 = datetime.timedelta(hours=offsetHours2, minutes=offsetMinutes2)
    #Condition to obtain the end date in UTC
        if offsetSign == "+":
            endDate = endDate - offset
        else:
            endDate = endDate + offset

        if offsetSign2 == "+":
            StartDate = StartDate - offset2
        else:
            StartDate = StartDate + offset2
    #Condition to check if the event is over
        naam = event['summary']

        if temp1 == 2:
            einddate = endDate#stel alleen in tijdens startup
            startdatum = StartDate
        print("Info maaitijden ----- start: " + str(StartDate) + " stop: " + str(endDate) + " tijd: " + str(currentTime) + " temp=" + str(temp1))
        
        
        if (currentTime > einddate  and currentTime < StartDate and temp1 == 1) or temp1 == 2:
            #print("Stop")
            if naam.upper() == "START":
                startdatum = StartDate
                einddate = endDate
                print("Datums maaien aangepast, start: " + str(StartDate) + " +2u - stop: " + str(endDate) + " +2u - tijd: " + str(currentTime) + " +2u")
            temp1 = 0  
        else:
            
            #print("Event is bezig")
            if (temp1 == 0 or temp1 == 2) and currentTime > startdatum:
                #os.system("/script/google-kalender/robotmaaier_command.py noodstop.home")
                print("Maai info:")
                print("------------------------------------------------")
                #text1 = os.system("/script/google-kalender/robotmaaier_command.py normale.maaibeurt")
                text1 = commands.getoutput("/script/google-kalender/robotmaaier_command.py normale.maaibeurt")
                print(text1)
                #kijk of er een exit foutmelding voorkomt want dan wordt er niet gemaaid
                if (text1.find("Exit") == -1):
                   temp1 = 1
                   print("Maaien gestart")
                   print("------------------------------------------------")
                else:
                   print("Er wordt niet gemaaid")
                   print("------------------------------------------------")
                  
            #print(StartDate)
        if (currentTime > einddate  and currentTime > startdatum ):
                startdatum = StartDate
                einddate = endDate
                print("Datums opnieuw aangepast, start: " + str(StartDate) + " +2u - stop: " + str(endDate) + " +2u - tijd: " + str(currentTime) + " +2u")
    #restart het script na een aantal minuten (zodat de kalender ververst word)
    if tel == 30:
        restart()    
    time.sleep(60)
    tel = tel + 1
 except:
    print("Error: 60sec wachten")
    time.sleep(60) 
