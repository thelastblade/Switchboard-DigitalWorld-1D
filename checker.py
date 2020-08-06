from libdw import pyrebase
from libdw import sm
import datetime
#secrets is a python file containing all the credentials of firebase and telegrambot.
from secrets import *

import gspread
from oauth2client.service_account import ServiceAccountCredentials
#setup for google spreadsheet
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

#add header for google spreadsheets
sheet = client.open("Room Data").sheet1
row = ['Time','state']
index = 1
sheet.insert_row(row, index)

#create a function to add subsequent lines for google spreadsheets
def update_next_row(state,n):

    #n is the row in which the data is added to.
    row = [str(datetime.datetime.now()),str(state)]
    sheet.insert_row(row, n)

#how long the the room needs to be empty before it resets to empty,this is in minutes.
blocktime=1

#buffer time to check if the room is still being used.this is in minutes
#will increase the end time of the sessions by blocktime minutes if motion is detected between
#block buffer time and end of session.
blockbuffertime=0.5

#state machine for the system to check the firebase data.
class tableSM(sm.SM):
    def __init__(self):
        #inital state
        self.state = 'all clear'

        #initial line to add google data to.
        self.count=2

    def get_next_values(self, state, inp):
            #get values of table from firebase
            table1val= db.child("table1").get().val()
            table2val= db.child("table2").get().val()
            name1=db.child('name1').get().val()
            name2=db.child('name2').get().val()

            #set the timenow to a value.
            timenow=datetime.datetime.now()

            #get timings from previous inp
            table1time,table2time=inp


            if state=='all clear':
                #if table 1 becomes occupied
                if table1val=='Occupied':

                    next_state='table 1 occupied'
                    #sets a time with the blocktime added so that the room will be occupied by blocktime minutes
                    table1time = datetime.datetime.now()
                    table1time = table1time + datetime.timedelta(minutes = blocktime)

                    #stores time on firebase
                    db.child('table1time').set(str(table1time))

                    #uses function to add next row onto google spreadsheets
                    update_next_row(next_state,self.count)

                    #ensure adding to next row of data.
                    self.count+=1

                #if table 2 is occupied
                elif table2val=='Occupied':
                    next_state='table 2 occupied'
                    table2time = datetime.datetime.now()
                    #sets a time with the blocktime added so that the room will be occupied by blocktime minutes
                    table2time = table2time + datetime.timedelta(minutes = blocktime)

                    #adds time to firebase
                    db.child('table2time').set(str(table2time))

                    #update data to google spreadsheet
                    update_next_row(next_state,self.count)

                    self.count+=1

                else:
                    next_state=state

            #when the state machine is in the table 1 occupied state
            elif state=='table 1 occupied':
                if name1 =='ended':
                    next_state='all clear'
                    db.child("name1").set('')
                    db.child('table1time').set('Empty')
                    #updates on spreadsheet
                    update_next_row(next_state,self.count)
                    self.count+=1
                else:

                    #if the time is still within the blocked out time of table 1
                    if timenow.time()<table1time.time():

                        #sets name as unknown if name is unknown
                        if name1=='':
                            db.child("name1").set('Unknown')
                        #buffer time is the minutes
                        table1timebuffer = table1time - datetime.timedelta(minutes = blockbuffertime)
                        if timenow.time()<table1timebuffer.time():
                            #so if it is within the buffer time it starts checking if the room is occupied again.
                            if table1val=="Occupied":
                                #if occupied adds blocktime to end of time.
                                    table1time = datetime.datetime.now()
                                    table1time = table1time + datetime.timedelta(minutes = blocktime)
                                    db.child('table1time').set(str(table1time))

                    #if table 2 becomes occupied
                        if table2val=='Occupied':
                            next_state='all tables occupied'
                            table2time = datetime.datetime.now()
                            #adds blocktime to table2time which is the time till the room is booked for
                            table2time = table2time + datetime.timedelta(minutes = blocktime)

                            db.child('table2time').set(str(table2time))

                            #add state to google spreadsheet.
                            update_next_row(next_state,self.count)
                            self.count+=1


                        else:
                            #state does not change otherwise
                            next_state=state


                    #out of block time and is not occupied within buffer time hence it is assumed as empty.
                    else:
                        next_state='all clear'
                        db.child("name1").set('')
                        db.child('table1time').set('Empty')
                        #updates on spreadsheet
                        update_next_row(next_state,self.count)
                        self.count+=1


            #state if only table 2 is occupied
            elif state=='table 2 occupied':
                if name2=='ended':
                    #if time limit for table 2 has passed and no movement in buffer time
                    #resets table.
                    next_state='all clear'
                    db.child("name2").set('')
                    db.child('table2time').set("Empty")
                    update_next_row(next_state,self.count)
                    self.count+=1
                else:
                    #if still within the time in which table 2 is blocked out for.
                    if timenow.time()<table2time.time():
                        #sets name as unknown if no card is used.
                        if name2=='':
                            db.child("name2").set('Unknown')
                        table2timebuffer = table2time - datetime.timedelta(minutes = blockbuffertime)

                        #if within the buffer time
                        if timenow.time()<table2timebuffer.time():
                            #if the value from firebase is occupied
                            if table2val=='Occupied':
                                #increases time by blocktime
                                table2time = datetime.datetime.now()
                                table2time = table2time + datetime.timedelta(minutes = blocktime)
                                db.child('table2time').set(str(table2time))

                        #If table 1 is occupied
                        if table1val=='Occupied':
                            next_state='all tables occupied'
                            #sets the table1time as the time plus how long the room is blocked out for.
                            table1time = datetime.datetime.now()
                            table1time = table1time + datetime.timedelta(minutes = blocktime)

                            db.child('table1time').set(str(table1time))

                            #adds to google spreadsheet
                            update_next_row(next_state,self.count)
                            self.count+=1

                        #else continues with current state.
                        else:
                            next_state=state
                    else:
                        #if time limit for table 2 has passed and no movement in buffer time
                        #resets table.
                        next_state='all clear'
                        db.child("name2").set('')
                        db.child('table2time').set("Empty")
                        update_next_row(next_state,self.count)
                        self.count+=1

            #state is in all tables occupied
            elif state=='all tables occupied':
                if name1=='ended':
                    next_state='table 2 occupied'
                    db.child('table1time').set("Empty")
                    db.child("name1").set('')
                    update_next_row(next_state,self.count)
                    self.count+=1
                elif name2=='ended':
                    next_state='table 1 occupied'
                    db.child('table2time').set("Empty")
                    db.child("name2").set('')
                    update_next_row(next_state,self.count)
                    self.count+=1
                else:
                    #checks if there is no name attached to the room sets it as unknown.
                    if name1=='':
                        db.child("name1").set('Unknown')
                    if name2=='':
                        db.child("name2").set('Unknown')

                    #creates buffer time
                    table1timebuffer = table1time - datetime.timedelta(minutes = blockbuffertime)
                    table2timebuffer = table2time - datetime.timedelta(minutes = blockbuffertime)

                    #if within buffer time check if the rooms are occupied, increases booked time by blocktime if it is.
                    if timenow.time()<table2timebuffer.time():
                        if table2val=="Occupied":
                                table2time = datetime.datetime.now()
                                table2time = table2time + datetime.timedelta(minutes = blocktime)
                                db.child('table2time').set(str(table2time))

                    if timenow.time()<table1timebuffer.time():
                        if table1val=='Occupied':
                                table1time = datetime.datetime.now()
                                table1time = table1time + datetime.timedelta(minutes = blocktime)
                                db.child('table1time').set(str(table1time))
                    #changes state if time for table 2 expires.
                    if timenow.time()>table2time.time():
                        next_state='table 1 occupied'
                        db.child('table2time').set("Empty")
                        db.child("name2").set('')
                        update_next_row(next_state,self.count)
                        self.count+=1

                    #changes state if time for table 1 expires.
                    elif timenow.time()>table1time.time():
                        next_state='table 2 occupied'
                        db.child('table1time').set("Empty")
                        db.child("name1").set('')
                        update_next_row(next_state,self.count)
                        self.count+=1

                    #else keeps current state
                    else:
                        next_state=state
            #passes on the next_state as next state and table1time and table 2 time as inputs
            return next_state,(table1time,table2time)

#standard firebase setup
# URL to Firebase database
url = firebasesecrets['url']

# unique token used for authentication
apikey = firebasesecrets['apikey']
config={
    "apiKey":apikey,
    "databaseURL":url,
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

#setup for state machine
tablesm=tableSM()

#initialises a time for initial state machine inputs
table1time=datetime.datetime.now()
table2time=datetime.datetime.now()

#continually runs state machine with inputs from past outputs.
while 1:
    (table1time,table2time)=tablesm.step((table1time,table2time))
