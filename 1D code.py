# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 13:25:54 2019

@author: ato
"""
#firebase
from libdw import pyrebase

#kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.clock import Clock
from secrets import *


Window.clearcolor=(1,1,1,1)

Builder.load_string("""
#:import Factory kivy.factory.Factory
#:import Clock kivy.clock.Clock

### Instructions on how to use the app
<MyPopup@Popup>:
    auto_dismiss: False
    title: "Instructions"
    title_size: 48
    Button:

        text: 'Check Availability >> Select Location: \
        \\n \
            \\n View availability of your room of choice and other possible locations\
            \\n \
        \\n Select button to change the availability of the table/room after you leave\
        \\n \\n \
        \\n Click anywhere to close'
        font_size: 20
        on_release: root.dismiss()

##Layout for menu screen with three buttons to check availability, instructions and quit
## Buttons will direct users to the respective screens
<Menu>:
    FloatLayout:
        Label:
            text: 'Menu'
            font_size: 48
            pos_hint: {'center_x': 0.5, 'center_y':0.9}
            size_hint: 0.3, 0.2
            color: 0.2,0.4,0.8,1 #Blue

        Button:
            text: 'Check availability'
            font_size: 25
            pos_hint: {'center_x':0.5, 'center_y': 0.7}
            size_hint: 0.5, 0.15
            on_press: root.manager.current = "location"

        Button:
            text: 'Help'
            on_release: Factory.MyPopup().open()
            font_size: 25
            pos_hint: {'center_x':0.5, 'center_y': 0.5}
            size_hint: 0.5, 0.15

        Button:
            text: 'Quit'
            font_size: 25
            pos_hint: {'center_x':0.5, 'center_y': 0.3}
            size_hint: 0.5, 0.15
            on_press: app.get_running_app().stop()

## Location screen for hostel blocks, backk button to return to menu screen
## Buttons direct users to the respective location screens.
## Only buttons for blk 55 and others would be directed in this case

<Location>:

    FloatLayout:
        Label:
            text: 'Select Location'
            font_size: 48
            pos_hint: {'center_x': 0.5, 'center_y':0.9}
            size_hint: 0.3, 0.2
            color: 0.2,0.4,0.8,1

        Button:
            text: 'Block 55'
            font_size: 25
            pos_hint: {'center_x':0.5, 'center_y': 0.7}
            size_hint: 0.5, 0.15
            on_press: root.manager.current = "blk55"

        Button:
            text: 'Block 57'
            font_size: 25
            pos_hint: {'center_x':0.5, 'center_y': 0.5}
            size_hint: 0.5, 0.15

        Button:
            text: 'Block 59'
            font_size: 25
            pos_hint: {'center_x':0.5, 'center_y': 0.3}
            size_hint: 0.5, 0.15

        Button:
            text: 'Others'
            font_size: 25
            pos_hint: {'center_x':0.5, 'center_y': 0.1}
            size_hint: 0.5, 0.15
            on_press: root.manager.current = "check_others"


        Button:
            text: '< Back'
            font_size: 25
            pos_hint: {'x':0, 'y': 0.9}
            size_hint: 0.2, 0.1
            background_color: (0,0,0,0.1)
            color: (0,0,0,1)
            on_press: root.manager.current = "menu"


##Viewing availability of dummy room to be used for demo purposes
<Check_others>:
    ## Updates the readings from the firebase every 3 seconds
    on_enter: Clock.schedule_interval(self.check_update,3)
    FloatLayout:

        Label:
            text:'Cohort Classroom 7'
            font_size: 48
            pos_hint: {'center_x': 0.5, 'center_y':0.9}
            size_hint: 0.3, 0.2
            color: 0,0,0,1

        Label:
            text: 'Mini Think Tank'
            font_size: 25
            pos_hint: {'center_x':0.2, 'center_y': 0.5}
            size_hint: 0.3, 0.2
            color: 0,0,0,1


        ## The availability of the rooms as displayed on the buttons are linked to name value in the firebase
        ## If there is a name being displayed in the firebase (User tapped card on RFID) or "unknown" is displayed,
        ## the table would be occupied. Otherwise, the table will be reflected as empty

        Button:
            id: others1
            text:"Empty" if root.db.child("name1").get().val() == "" else "Occupied"
            on_press: root.edit_others1()
            font_size: 25
            pos_hint: {'center_x':0.5, 'center_y': 0.5}
            size_hint: 0.295, 0.195
            background_normal: ''
            background_color: (0,0.9,0,0.8) if self.text == "Empty" else (0.9,0,0,0.8)

        Label:
            id: others1_name
            text: ("by " + root.db.child("name1").get().val()) if root.db.child("name1").get().val() != "" else ""
            font_size: 20
            pos_hint: {'center_x':0.57, 'center_y': 0.43}
            size_hint: 0.15, 0.1
            color: 0,0,0,1

        Button:
            id: others2
            text:"Empty" if root.db.child("name2").get().val() == "" else "Occupied"
            on_press: root.edit_others2()
            font_size: 25
            pos_hint: {'center_x':0.8, 'center_y': 0.5}
            size_hint: 0.295, 0.195
            background_normal: ''
            background_color: (0,0.9,0,0.8) if self.text == "Empty" else (0.9,0,0,0.8)

        Label:
            id: others2_name
            text: "" if root.db.child("name2").get().val() == "" else ("by " + root.db.child("name2").get().val())
            font_size: 20
            pos_hint: {'center_x':0.85, 'center_y': 0.43}
            size_hint: 0.15, 0.1
            color: 0,0,0,1

        Label:
            text: 'Table 1'
            font_size: 25
            pos_hint: {'center_x':0.41, 'center_y': 0.57}
            size_hint: 0.15, 0.1
            color: 0,0,0,1

        Label:
            text: 'Table 2'
            font_size: 25
            pos_hint: {'center_x':0.71, 'center_y': 0.57}
            size_hint: 0.15, 0.1
            color: 0,0,0,1

        Button:
            text: '< Back'
            font_size: 25
            pos_hint: {'x':0, 'y': 0.9}
            size_hint: 0.2, 0.1
            background_color: (0,0,0,0.1)
            color: (0,0,0,1)
            on_press: root.manager.current = "location"

## Screen for availability of common rooms in blk 55
## This screen is not dynamic and values are filled in for purposes of showing an example of a full layout
<Check_BLK55>:

    FloatLayout:

        Label:
            text:'Block 55'
            font_size: 40
            pos_hint: {'center_x': 0.5, 'center_y':0.95}
            size_hint: 0.3, 0.2
            color: 0,0,0,1

####### LVL 2 #############
        Label:
            text: 'Level 2 Meeting Room'
            font_size: 20
            pos_hint: {'center_x':0.2, 'center_y': 0.7}
            size_hint: 0.3, 0.1
            color: 0,0,0,1

        Button:
            id: lvl2MR
            text:"Empty" #Normally should be getting values from firebase
            font_size: 20
            pos_hint: {'center_x':0.65, 'center_y': 0.7}
            size_hint: 0.595, 0.095
            background_normal: ''
            background_color: (0,0.9,0,0.8) if self.text == "Empty" else (0.9,0,0,0.8)

        Label:
            id: lvl2MR_name
            text: ""
            font_size: 15
            pos_hint: {'center_x':0.85, 'center_y': 0.62}
            size_hint: 0.15, 0.1
            color: 0,0,0,1

####### LVL 4 #############
        Label:
            text: 'Level 4 Study Room'
            font_size: 20
            pos_hint: {'center_x':0.2, 'center_y': 0.6}
            size_hint: 0.3, 0.1
            color: 0,0,0,1

        Button:
            id: lvl4SR
            text:"Occupied" #Normally should be getting values from firebase
            font_size: 20
            pos_hint: {'center_x':0.65, 'center_y': 0.6}
            size_hint: 0.595, 0.095
            background_normal: ''
            background_color: (0,0.9,0,0.8) if self.text == "Empty" else (0.9,0,0,0.8)

        Label:
            id: lvl4SR_name
            text: "by "+"Unknown"
            font_size: 15
            pos_hint: {'center_x':0.85, 'center_y': 0.57}
            size_hint: 0.3, 0.1
            color: 0,0,0,1

        Label:
            text: 'Level 4 Recre Room'
            font_size: 20
            pos_hint: {'center_x':0.2, 'center_y': 0.5}
            size_hint: 0.3, 0.10
            color: 0,0,0,1

        Button:
            id: lvl4RR
            text:"Occupied" #Normally should be getting values from firebase
            font_size: 20
            pos_hint: {'center_x':0.65, 'center_y': 0.5}
            size_hint: 0.595, 0.095
            background_normal: ''
            background_color: (0,0.9,0,0.8) if self.text == "Empty" else (0.9,0,0,0.8)

        Label:
            id: lvl4RR_name
            text: "by " + "Bob"
            font_size: 15
            pos_hint: {'center_x':0.85, 'center_y': 0.47}
            size_hint: 0.3, 0.1
            color: 0,0,0,1

####### LVL 6 #############
        Label:
            text: 'Level 6 Study Room'
            font_size: 20
            pos_hint: {'center_x':0.2, 'center_y': 0.4}
            size_hint: 0.3, 0.1
            color: 0,0,0,1

        Button:
            id: lvl6SR1
            text:"Empty" #Normally should be getting values from firebase
            font_size: 20
            pos_hint: {'center_x':0.425, 'center_y': 0.4}
            size_hint: 0.145, 0.095
            background_normal: ''
            background_color: (0,0.9,0,0.8) if self.text == "Empty" else (0.9,0,0,0.8)

        Label:
            id: lvl6SR_name1
            text: ""
            font_size: 13
            pos_hint: {'center_x':0.46, 'center_y': 0.365}
            size_hint: 0.15, 0.1
            color: 0,0,0,1

        Button:
            id: lvl6SR2
            text:"Occupied"
            font_size: 20
            pos_hint: {'center_x':0.575, 'center_y': 0.4}
            size_hint: 0.1475, 0.095
            background_normal: ''
            background_color: (0,0.9,0,0.8) if self.text == "Empty" else (0.9,0,0,0.8)

        Label:
            id: lvl6SR_name2
            text: "by " + "Nicole"
            font_size: 13
            pos_hint: {'center_x':0.61, 'center_y': 0.365}
            size_hint: 0.15, 0.1
            color: 0,0,0,1

        Button:
            id: lvl6SR3
            text:"Empty"
            font_size: 20
            pos_hint: {'center_x':0.725, 'center_y': 0.4}
            size_hint: 0.1475, 0.095
            background_normal: ''
            background_color: (0,0.9,0,0.8) if self.text == "Empty" else (0.9,0,0,0.8)

        Label:
            id: lvl6SR_name3
            text: ""
            font_size: 13
            pos_hint: {'center_x':0.76, 'center_y': 0.365}
            size_hint: 0.15, 0.1
            color: 0,0,0,1

        Button:
            id: lvl6SR4
            text:"Occupied"
            font_size: 20
            pos_hint: {'center_x':0.875, 'center_y': 0.4}
            size_hint: 0.145, 0.095
            background_normal: ''
            background_color: (0,0.9,0,0.8) if self.text == "Empty" else (0.9,0,0,0.8)

        Label:
            id: lvl6SR_name4
            text: "by " + "Oliver"
            font_size: 13
            pos_hint: {'center_x':0.91, 'center_y': 0.365}
            size_hint: 0.15, 0.1
            color: 0,0,0,1

        Label:
            text: 'Table 1'
            font_size: 13
            pos_hint: {'center_x':0.385, 'center_y': 0.43}
            size_hint: 0.15, 0.1
            color: 0,0,0,1

        Label:
            text: 'Table 2'
            font_size: 13
            pos_hint: {'center_x':0.535, 'center_y': 0.43}
            size_hint: 0.15, 0.1
            color: 0,0,0,1

        Label:
            text: 'Table 3'
            font_size: 13
            pos_hint: {'center_x':0.685, 'center_y': 0.43}
            size_hint: 0.15, 0.1
            color: 0,0,0,1

        Label:
            text: 'Table 4'
            font_size: 13
            pos_hint: {'center_x':0.835, 'center_y': 0.43}
            size_hint: 0.15, 0.1
            color: 0,0,0,1

        Label:
            text: 'Level 6 Recre Room'
            font_size: 20
            pos_hint: {'center_x':0.2, 'center_y': 0.3}
            size_hint: 0.3, 0.1
            color: 0,0,0,1

        Button:
            id: lvl6RR
            text:"Occupied" #Normally should be getting values from firebase
            font_size: 20
            pos_hint: {'center_x':0.65, 'center_y': 0.3}
            size_hint: 0.595, 0.095
            background_normal: ''
            background_color: (0,0.9,0,0.8) if self.text == "Empty" else (0.9,0,0,0.8)

        Label:
            id: lvl6RR_name
            text: "by " + "Unknown"
            font_size: 15
            pos_hint: {'center_x':0.85, 'center_y': 0.27}
            size_hint: 0.15, 0.1
            color: 0,0,0,1

####### LVL 7 #############
        Label:
            text: 'Level 7 Meeting Room'
            font_size: 20
            pos_hint: {'center_x':0.2, 'center_y': 0.2}
            size_hint: 0.3, 0.1
            color: 0,0,0,1

        Button:
            id: lvl7MR1
            text:"Occupied"
            font_size: 20
            pos_hint: {'center_x':0.5, 'center_y': 0.2}
            size_hint: 0.295, 0.095
            background_normal: ''
            background_color: (0,0.9,0,0.8) if self.text == "Empty" else (0.9,0,0,0.8)

        Label:
            id: lvl7MR_name1
            text: "by " + "Taylor"
            font_size: 15
            pos_hint: {'center_x':0.6, 'center_y': 0.17}
            size_hint: 0.15, 0.1
            color: 0,0,0,1

        Button:
            id: lvl7MR2
            text: "Empty"
            font_size: 20
            pos_hint: {'center_x':0.8, 'center_y': 0.2}
            size_hint: 0.295, 0.095
            background_normal: ''
            background_color: (0,0.9,0,0.8) if self.text == "Empty" else (0.9,0,0,0.8)

        Label:
            id: lvl7MR_name2
            text: ""
            font_size: 15
            pos_hint: {'center_x':0.9, 'center_y': 0.17}
            size_hint: 0.15, 0.1
            color: 0,0,0,1


####### LVL 9 #############
        Label:
            text: 'Level 9 Meeting Room'
            font_size: 20
            pos_hint: {'center_x':0.2, 'center_y': 0.1}
            size_hint: 0.3, 0.1
            color: 0,0,0,1

        Button:
            id: lvl9MR
            text:"Empty" #Normally should be getting values from firebase
            font_size: 20
            pos_hint: {'center_x':0.65, 'center_y': 0.1}
            size_hint: 0.595, 0.095
            background_normal: ''
            background_color: (0,0.9,0,0.8) if self.text == "Empty" else (0.9,0,0,0.8)

        Label:
            id: lvl9MR_name
            text: ""
            font_size: 15
            pos_hint: {'center_x':0.85, 'center_y': 0.07}
            size_hint: 0.15, 0.1
            color: 0,0,0,1


        Button:
            text: '< Back'
            font_size: 20
            pos_hint: {'x':0, 'y': 0.9}
            size_hint: 0.2, 0.1
            background_color: (0,0,0,0.1)
            color: (0,0,0,1)
            on_press: root.manager.current = "location"





""")

## define new classes for each screen, there is no functions within the classes for Menu and Location
class Menu(Screen):
#    def to_location(self,instance):
#        self.root.current = "location"
    pass

class Location(Screen):
    pass

# the Check_others screen involves getting data from the firebase, code is written to set up firebase
class Check_others(Screen):
    url = firebasesecrets['url'] # URL to Firebase database
    apikey = firebasesecrets['apikey'] # unique token used for authentication

    config={
            "apiKey":apikey,
            "databaseURL":url,
            }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

# edit_others functions changes the occupancy of the tables in the room when the user presses the button
# The room occupancy should be updated both on the firebase and the app

    def edit_others1(self):
        if self.ids.others1.text == "Occupied":
            self.ids.others1.text = "Empty"
            self.ids.others1_name.text = "ended"

        else:
            self.ids.others1.text = "Occupied"
            self.ids.others1_name.text = self.db.child("name1").get().val()

        self.db.child("table1").set(self.ids.others1.text)
        self.db.child("name1").set(self.ids.others1_name.text)

    def edit_others2(self):
        if self.ids.others2.text == "Occupied":
            self.ids.others2.text = "Empty"
            self.ids.others2_name.text = "ended"

        else:
            self.ids.others2.text = "Occupied"
            self.ids.others2_name.text = "Unknown"

        self.db.child("table2").set(self.ids.others2.text)
        self.db.child("name2").set(self.ids.others2_name.text)

# check_update updates the values of the app from firebase data at 3 seconds intervals
# The occupancy of the tables should similarly be derived from the name values

    def check_update(self,*args):
        #self.ids.others1.text = self.db.child("table1").get().val()
        self.ids.others1_name.text = self.db.child("name1").get().val()

        if self.ids.others1_name.text == "":
            self.ids.others1.text = "Empty"
        else:
            self.ids.others1.text = "Occupied"
            self.ids.others1_name.text = "by " + self.ids.others1_name.text

        self.ids.others2_name.text = self.db.child("name2").get().val()
        if self.ids.others2_name.text == "":
            self.ids.others2.text = "Empty"
        else:
            self.ids.others2.text = "Occupied"
            self.ids.others2_name.text = "by " + self.ids.others2_name.text

# No firebase data is linked to the blk 55 layout for this demostration
# For actual execution,each table would have a code similar to that in Check_others
class Check_BLK55(Screen):
    pass


#Creating the class for the main app. Includes linking the screens and starting at menu

class KivyApp (App):

    def build(self):
        #creating screen manager
        sm = ScreenManager()
        sm.add_widget(Menu(name='menu'))
        sm.add_widget(Location(name='location'))
        sm.add_widget(Check_others(name='check_others'))
        sm.add_widget(Check_BLK55(name='blk55'))
        sm.current = 'menu' #changes first screen for testing
        return sm


if __name__=='__main__':
    KivyApp().run()
