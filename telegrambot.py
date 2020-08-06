import time
import random
import datetime
import telepot
from telepot.loop import MessageLoop
from libdw import pyrebase

#secrets is a python file containing all the credentials of Firebase and Telegram
from secrets import *

#setup for firebase
#URL to Firebase database
url = firebasesecrets['url']
#unique token used for authentication
apikey = firebasesecrets['apikey']
config={
    "apiKey":apikey,
    "databaseURL":url,
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()


#to handle the different commands coming to the telegram bot
def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    alert='Got Command '+command

    print (alert)
    #initialize the application
    if command=='/start':
        Message='Hi,welcome to table checker. You can type /help for some help.'

    #instructions on how to use the application
    elif command=='/help':
         Message='Looks like you need some help. You can check the status of table 1 using /table1 and table 2 using /table2. You can also use /alltables to get an update on all tables available.'

    #displays the availabilities for all tables from Firebase database
    elif command=='/alltables':
        name1=db.child('name1').get().val()
        name2=db.child('name2').get().val()
        if name1 != '':

            #if name for table1 is not empty, table is occupied
            submessage1='Table 1 is Occupied by '+name1

        else:

            #if name for table1 is empty, table is empty
            submessage1='Table 1 is Empty'
        if name2 !="":

            #if name for table2 is not empty, table is occupied
            submessage2='Table 2 is Occupied by '+name2

        else:

            #if name for table2 is empty, table is empty
            submessage2='Table 2 is Empty'

        Message=submessage1+' and '+submessage2

    #if application user wants to check availability of table1
    elif command == '/table1':

        #retrieves information from Firebase under key 'name1'
        name1=db.child('name1').get().val()
        if name1 != '':

            #if name for table1 is not empty, table is occupied
            Message='Table 1 is Occupied by '+name1

        else:

            #if name for table1 is empty, table is empty
            Message='Table 1 is Empty'

    #if application user wants to check availability of table2
    elif command == '/table2':

        #retrieves information from Firebase under key 'name2'
        name2=db.child('name2').get().val()
        if name2 != '':

            #if name for table2 is not empty, table is occupied
            Message='Table 2 is Occupied by '+name2

        else:

            #if name for table2 is empty, table is empty
            Message='Table 2 is Empty'
    else:

        #if application user sends other commands, it will return an error message
        Message="wrong command, use /help for help."

    #display message in SUTDROOMbot
    bot.sendMessage(chat_id, str(Message))

#Token references a string in secrets for the telegram API key
bot = telepot.Bot(TOKEN)

#standard telepot setup
MessageLoop(bot, handle).run_as_thread()
print ('I am listening ...')

while 1:
    time.sleep(10)
