import RPi.GPIO as GPIO
import time
from libdw import pyrebase

#secret is a python file containing all the credentials of Firebase
from secrets import firebasesecrets

from libdw import sm

#tablenumer changes accordingly with the different table numbers
tablenumber=1

#setup for ultrasonic sensor
#distancelimit is set to 100cm
distancelimit=100
GPIO.setmode(GPIO.BCM)
TRIG = 13
ECHO = 19
GPIO.setup(TRIG,GPIO.OUT) #Trig pin of Ultrasonic setup
GPIO.setup(ECHO,GPIO.IN) #GPIO 19 -> Echo as input

#setup for ir sensor
IR=20
GPIO.setup(IR,GPIO.IN) #GPIO 13 -> IR sensor as input

#standard setup for firebaseio
#firebase secrets is a dictionary in secrets
url = firebasesecrets['url'] #URL to Firebase database
apikey = firebasesecrets['apikey'] #unique token used for authentication
config={
    "apiKey":apikey,
    "databaseURL":url,
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

#setup for sensor state machine
class Sensors(sm.SM):

    #sets initial state to be 'empty'
    start_state = 'Empty'

    def start(self):
        self.state = self.start_state
    def get_next_values(self, state, inp):
            dist = distance()
            iroutput=GPIO.input(IR)
            if state=='Empty':

                #when distance between ultrasonicsensor and object decreases, it shows that there is an object or person on the path of the pulse
                #when infrared sensor detects change in heat energy, it shows that there is a human presence/movement
                #if either one of the conditions is met, table is assumed as occupied
                #state of machine updated to 'occupied'
                if dist<distancelimit or iroutput==True:
                    next_state='Occupied'
                    db.child("table"+str(tablenumber)).set(next_state)

                #if no change in initial distance limit and infrared radiation level in table surroundings, table is assumed as empty
                else:
                    state=state
            else:

                #when state is 'occupied'
                ##when distance between ultrasonicsensor and object increases beyond distancelimit, it shows that there is nothing along the path of pulse
                #when infrared sensor doesn't detects change in heat energy, it shows that there is a lack of human presence/movement
                #if both of the above conditions are met, table is assumed as empty
                if dist>distancelimit and iroutput==False:
                    next_state='Empty'
                    db.child('table'+str(tablenumber)).set(next_state)

                #if distance between ultrasonic sensor and object is still below distancelimit or the infrared sensor still detects infrared radiation change, table is assumed occupied
                else:
                    next_state=state

            return next_state,next_state




def distance():
    #set Trigger to HIGH
    GPIO.output(TRIG, True)

    #set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    #define the starting and stopping time
    StartTime = time.time()
    StopTime = time.time()

    #saving the starting time as the time when ultrasonic pulse is sent out
    while GPIO.input(ECHO) == 0:
        StartTime = time.time()

    #saving the stopping time as the time when ultrasonic pulse is received back
    while GPIO.input(ECHO) == 1:
        StopTime = time.time()

    #time taken for pulse to be sent and reflected back and received
    TimeElapsed = StopTime - StartTime

    #multiply with the sonic speed (34300 cm/s) to get the distance travelled by the pulse
    #since distance travelled is twice of distance between sensor and object, divide by 2.
    distance = (TimeElapsed * 34300) / 2

    return distance

#initialize sensors state machine
sensor=Sensors()
sensor.start()
next_state='Empty'


try:
        while True:
            dist = distance()
            next_state=sensor.step(next_state)
            #reading taken at 1 second intervals
            time.sleep(1)
#reset by pressing CTRL + C
except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
