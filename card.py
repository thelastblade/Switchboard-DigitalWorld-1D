#Update RFID scanner reading to Firebase
import RPi.GPIO as GPIO
from libdw import pyrebase
from mfrc522 import SimpleMFRC522
from secrets import firebasesecrets
#would change for every table
tablenumber=1

#setup for firebase
url = firebasesecrets['url'] # URL to Firebase database
apikey = firebasesecrets['apikey'] # unique token used for authentication
config={
    "apiKey":apikey,
    "databaseURL":url,
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

#setup for RFID reader
reader = SimpleMFRC522()


try:
    while True:
        id, text = reader.read()
        #updates the card user's name to the corresponding table's value in Firebase
        db.child("name"+str(tablenumber)).set(text)
except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
