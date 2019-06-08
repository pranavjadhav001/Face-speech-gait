from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import ObjectProperty , StringProperty, ListProperty
from PIL import *
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.uix.screenmanager import FadeTransition 
import sys
from kivy.uix.textinput import TextInput
import sqlite3
from kivy.graphics import Color,Rectangle
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import datetime
import pyaudio
import wave
from kivy .clock import Clock
from kivy.animation import Animation
import time
import random
import gait
from database import database
from scipy.io.wavfile import read
import sklearn.mixture 
from speakerfeatures import extract_features
import string
from speech import speechy
import shutil
from face import face
import glob
import cv2
from imp_fns import keypairs,test_frame,train_frame,delete_files
import os
import json
import random
import numpy as np

punctuation=string.punctuation
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 3



global all_userids
all_userids=[]
global q
global event
global f
global trial_gait
global trai_speech
global trail_face

record = database()

class First(Screen):
    
    def done(self):
        App.get_running_app().stop()
        Window.close()

class Second(Screen):
    pass

class Delete(Screen):

    current_user=StringProperty()
    validity=StringProperty('**Credentials**')
    user_name=ObjectProperty()
    
    
    def text(self):
        self.validity='**Credentials**'
        self.user_name.text=''
          
    def compare(self,name):
        record.connection()
        data=record.get_profile()
        print('data is:',data)
        record.break_connection()
        names=[]
        
        for i in data:
            names.append(i[1])

        if str(name)=='' :
            self.validity='**Empty Details**'
            
            
        elif str(name) in names:
            self.current_user=self.user_name.text
            delete_files(name)
            self.validity='**Profile Deleted**'
            print(self.current_user)
            self.manager.current='second'
            self.user_name.text=''
            
           
        else:
            self.user_name.text=''
            
            self.validity='**Invalid Credentials**'
            

class User(Screen):
    userid=StringProperty()
    name_input=ObjectProperty()
    pin_input=ObjectProperty()
    check=StringProperty('**Enter Details**')
    
    def text(self):
        self.check='**Enter Details**'
        self.name_input.text=''
        self.pin_input.text=''
        
    def profile(self,name,pin):
        
        name=name.replace(' ','')
        pin=pin.replace(' ','')
        database_files = glob.glob('*.db')
        if len(database_files) > 0:
            condition=True
            record.connection()
            data=record.get_profile()
            user_names=[]
            for i in data:
                user_names.append(i[1])
            record.break_connection()
        else:
            user_names = []

        condition=True
        
        for i in str(name): 
            if i in punctuation:
                self.check='**Punctauations Not Allowed**'
                self.name_input.text=''
                self.pin_input.text=''
                condition=False
                break
            
        if len(name)<6 or len(name)>10:
            self.check='**User name must be 6-10 letters**'
            self.name_input.text=''
            self.pin_input.text=''
            condition=False
        elif str(pin).isalpha()==True:
            self.check='**Passcode must be digits**'
            self.pin_input.text=''
            condition=False
        elif str(name)=='' or str(pin)=='':
            self.check='**Empty Details**'
            condition=False
            
        elif len(pin)>4 or len(pin)<4:
            self.check='**Passcode must be 4 digits**'
            self.pin_input.text=''
            condition=False
            
        elif name in user_names:
            self.check='**Username Already Exist**'
            self.name_input.text=''
            self.pin_input.text=''
            condition=False
            
        elif name not in user_names and condition==True:
            record.connection()
            record.new_profile([name,pin])
            record.break_connection()
            self.userid=name
            print('userid:',self.userid)
            self.pop(self.name_input.text,self.pin_input.text)
        
        
    def pop(self,name,pin):
        name=name.replace(' ','')
        pin=pin.replace(' ','')
        
        n=BoxLayout(orientation='vertical',padding=10,spacing=10)
        box=Button(text='Close',font_size=25,size_hint=(0.5,0.4),pos_hint={'center_x':0.5})
        lb=Label(text='Profile Added!',font_size=25)
        lb1=Label(text='Your Passcode is: {}'.format(pin),font_size=25)
        popup = Popup(title='Finish', auto_dismiss=False,content=n, size_hint=(None, None), size=(400, 400))
        n.add_widget(lb)
        n.add_widget(lb1)
        n.add_widget(box)
        box.bind(on_press=popup.dismiss)
        def clear(self):
            self.name_input.text=''
            self.pin_input.text=''
        def screen_shift(self):
            self.manager.current='third'
        box.bind(on_release=lambda x:clear(self))
        box.bind(on_release=lambda x:screen_shift(self))
        popup.open()

class Third(Screen):
    pass

class Fourth(Screen):
    pass

class Portal(Screen):
    current_user=StringProperty()
    validity=StringProperty('**Credentials**')
    user_name=ObjectProperty()
    user_pin=ObjectProperty()
    
    def text(self):
        self.validity='**Credentials**'
        self.user_name.text=''
        self.user_pin.text=''
        
    def compare(self,name,pin):
        record.connection()
        data=record.get_profile()
        print('data is:',data)
        record.break_connection()
        pairs=[]
        
        for i in data:
            pairs.append((i[1],i[2]))

        if str(name)=='' or str(pin)=='':
            self.validity='**Empty Details**'
            
        elif str(pin).isalpha()==True:
            self.validity='**Passcode must be digits**'
            self.user_pin.text=''
            
            
        elif (str(name).lower(),int(pin)) in pairs:
            self.current_user=self.user_name.text
            self.validity='**Valid Credentials**'
            print(self.current_user)
            self.manager.current='tier1'
            self.user_name.text=''
            self.user_pin.text=''
           
        else:
            self.user_name.text=''
            self.user_pin.text=''
            self.validity='**Invalid Credentials**'
            


class Tier1(Screen):
    global trail_face
    trail_face=0
        
           
class Tier2(Screen):
    global trail_speech
    trail_speech=0

class Tier3(Screen):
    global trail_gait
    trail_gait=0


class Select(Screen):
    file=StringProperty()
    t=StringProperty('**Select File**')
    
    def text(self):
        self.t='**Select File**'
        
    def done(self,*args):
        try:
            self.file=args[1][0]
            self.t=self.file
        
        except: pass

    def filecheck(self):
        if self.file=='':
            self.t='No Slection'
        elif self.file.split('.')[-1].lower() not in ['mp4','mov','avi','flv','wmv']:
            self.t='Please select valid video File'
        else:
            self.manager.current='gait'
            self.t=("**Select File**")
            
class Select_2(Screen):
    audio=StringProperty()
    user_name=StringProperty()
    time=StringProperty('')
    time='Start Recording'
    
    def record(self):
        self.wat.text='**Recording**'
        WAVE_OUTPUT_FILENAME = "{}.wav".format(self.user_name)
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        
        
        print("***Recording!!!***")
        

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

            
        stream.stop_stream()
        stream.close()
        p.terminate()
        self.wat.text='**Done Recording**'
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        self.audio=WAVE_OUTPUT_FILENAME
        self.manager.current='speech'
        
    def text(self):
        self.wat.text='**Start Recording**'
    
class Step1(Screen):
    txt2=StringProperty('.................')
    user_name=StringProperty()
    def text(self):
        self.txt2='.................'
    
    def s(self):
        global trail_face
        print(trail_face)
        if trail_face==1:
            self.txt2=('.......Trail 2.......')

        img=face()
        record=database()
        record.connection()
        prediction=img.prediction(keypairs(record.get_profile()))
        print('prediction:',prediction)
        self.txt2='Done'
        print('user:',self.user_name)
        record.break_connection()
        while trail_face<=1:
            if prediction.lower()==self.user_name.lower():
                self.txt2='Authorized'
                trail_face=0
                self.manager.current='tier2'
                break
            else:
                self.txt2='Failed! Try Again'
                trail_face+=1
                self.manager.current='tier1'
                break

        if trail_face>1:
            trail_face=0
            self.txt2='**No Access**'
            self.manager.current='first'
            
class Step2(Screen):
    txt2=StringProperty('.................')
    f=StringProperty()
    user_name=StringProperty()
    def text(self):
        self.txt2='.................'
    

    def s(self):
        global trail_speech
        if trail_speech==1:
            self.txt2=('.......Trail 2.......')

        audio=speechy()
        record=database()
        record.connection()
        print(self.f)
        prediction=audio.predict(self.f)
        print('prediction:',prediction)
        self.txt2='Done'
        print('user:',self.user_name)
        while trail_speech<=1:
            if prediction.lower()==self.user_name.lower():
                self.txt2='Authorized'
                trail_speech=0
                self.manager.current='tier3'
                break
            else:
                self.txt2='Failed! Try Again'
                trail_speech+=1
                self.manager.current='tier2'
                break
            
               

        if trail_speech>1:
            trail_speech=0
            self.txt2='**No Access**'
            self.manager.current='first'

            
class Step3(Screen):
    txt1=StringProperty('.................')
    f=StringProperty()
    user_name=StringProperty()
    def text(self):
        self.txt2='.................'
    
    
    def g(self):
        global trail_gait
        #video = gait()
        record = database()
        record.connection()
        record.get_profile()
        os.chdir('./openpose')
        os.system('bin\OpenPoseDemo.exe --video '+self.f+' --net_resolution 176x320 --output_resolution 300x600 --write_json output/')
        os.chdir('..')
        names = keypairs(record.get_profile())
        if len(names) > 1:
            prediction=gait.prediction(self.f,self.user_name,names)
        elif len(names) ==1:
            prediction = list(names.keys())[0]
        print('prediction:',prediction)
        self.txt1='Done'
        print('user:',self.user_name)
        while trail_gait<=1:
            if prediction.lower()==self.user_name.lower():
                self.txt1='Authorized'
                self.manager.current='done'
                break
            else:
                self.txt1='Failed! Try Again'
                trail_gait+=1
                self.manager.current='select'
                break
        if trail_gait==1:
            self.txt1=('.......Trail 2.......')        

        if trail_gait>1:
            trail_gait = 0
            self.txt1='**No Access**'
            self.manager.current='first'
                
class Done(Screen):
    pass

    

        
class Fifth(Screen):
    time=StringProperty('')
    info=StringProperty('')
    time='Welcome'

    global a 
    a=0
    

    

    def record(self,user):
        global a 
        
        
        
        WAVE_OUTPUT_FILENAME = "{}_{}.wav".format(self.info,a)

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        
        
        print("***Recording!!!***")
        

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            
            data = stream.read(CHUNK)
            frames.append(data)

            
        if a==0:
            print("***Sample 1 Recording Done***")
            self.watch.text="Sample 1 Recording Done"
        if a==1:
            print("***Sample 2 Recording Done***")
            self.watch.text="Sample 2 Recording Done"
        if a==2:
            print("***Sample 3 Recording Done***")
            self.watch.text="Sample 3 Recording Done"
            
        

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        source=WAVE_OUTPUT_FILENAME
        destination="./audios"
        shutil.move(source,destination)
        
        if a==0:
            self.wat.text='Press Record Button For Sample 2'
        if a==1:
            self.wat.text='Press Record Button For Sample 3'
       
        if a==2:
            self.wat.text='Thank You'
            self.manager.current='third'

        a+=1
        
global count

class Sixth(Screen):
    
    
    file=StringProperty()
    t=StringProperty('**Select First File For Profile**')
    user=StringProperty()
        
    def text(self):
        global count
        self.t='**Select First File For Profile**'
        count=1
        
    def done(self,*args):
        try:
            self.file=args[1][0]
            self.t=self.file
        
        except: pass

    def filecheck(self):
        global count
        
        if self.file=='':
            self.t='No Selection'
        elif self.file.split('.')[-1].lower() not in ['mp4','mov']:
            self.t='Please select valid video File'
        else:
            os.chdir('./openpose')
            shutil.copy(self.file,"./trimmed_videos")
            print(self.file)
            os.rename('./trimmed_videos/{}'.format(self.file.split('\\')[-1])
                      ,'./trimmed_videos/{}'.format(self.user+'_'+str(count)+'.'+self.file.split('\\')[-1].split('.')[-1]))
            count+=1
            os.chdir('..')
            self.t='**Select Second File For Profile**'
            if count==3:
                self.t='**Select Third File For Profile**'
            if count==4:
                os.chdir('./openpose')
                for j in glob.glob('./trimmed_videos/'+self.user+'*.mp4'):
                    print(j)
                    os.system('bin\OpenPoseDemo.exe --video '+j+' --net_resolution 176x320 --output_resolution 300x600 --write_json json_output/')
                os.chdir('..')
                count=1
                self.manager.current='third'
                self.t=("**Thank You**")
           # self.manager.current='third'
            #self.t=("**Thank You**")
            
class Select3(Screen):
    file=StringProperty()
    t=StringProperty('**Select File**')
    user=StringProperty()
    def text(self):
        self.t='**Select File**'
        
    def done(self,*args):
        try:
            self.file=args[1][0]
            self.t=self.file
        
        except: pass
    def frames(self,path):
        img=[]
        su=1
        vid=cv2.VideoCapture(path)
        while su:
            su,imgy=vid.read()
            img.append(imgy)
        img.pop()
        list1 = []
        c=0
        for j in range(0,len(img),int(len(img)/5)):
            c += 1
            if c <= 5:
                list1.append(img[j])
        for i in range(len(list1)):
            cv2.imwrite("./images/{}_{}.jpg".format(self.user,i+1),list1[i])
            
    
    def filecheck(self):
        if self.file=='':
            self.t='No Slection'
        elif self.file.split('.')[-1].lower() not in ['mp4','mov','avi','flv','wmv']:
            self.t='Please select valid Video File'
        else:
            self.t=("**Thank You**")

            self.frames(self.file)
            self.manager.current='third'
            
            
class Webcam_Profile(Screen):
    label=StringProperty('**Please Press Space To Capture Photo**')
    count=StringProperty('**Count**')
    def text(self):
        self.label='**Please Press Space To Capture Photo**'
    user_name=StringProperty()
    def training_frame(self):
        train_frame(self.user_name)
        self.manager.current='third'

    
class Training(Screen):
    label=StringProperty('**Select Training Option**')
    
class Speech_Training(Screen):
    label=StringProperty("**Training....**")
    def text(self):
        self.label="**Training....**"
    def train(self):
        s=speechy()
        s.train()
        self.label='**Training Completed**'
        self.manager.current='training'
    def cancel(self):
        pass
    
class Gait_Training(Screen):
    label=StringProperty("**Training....**")
    def text(self):
        self.label="**Training....**"
    def train(self):
        record = database()
        record.connection()
        record.get_profile()
        names_dict = keypairs(record.get_profile())
        if len(names_dict)>1:
            
            data_dict = gait.gait_train(names_dict)
            x_train = []
            y_train = []
            for i,j in data_dict.items():
                if len(j) > 0 :
                    x_train.append(np.array(j).flatten())
                    y_train.append(names_dict[i.split('_')[0]])
            print(y_train)
            if len(np.unique(y_train)) > 0:
                print('training')
                gait.svm_train(x_train,y_train)
        elif len(names_dict) == 1:
            print('only 1 profile')
            

        self.label='**Training Completed**'
        self.manager.current='training'
    def cancel(self):
        pass

                         
            
class Face_Training(Screen):
    label=StringProperty("**Training....**")
    def text(self):
        self.label="**Training....**"
    def train(self):
        s=face()
        record.connection()
        s.train2(keypairs(record.get_profile()))
        self.label='**Training Completed**'
        self.manager.current='training'
        
    def cancel(self):
        pass
    
class Manager(ScreenManager):
    pass

class Crank(App):
    def build(self):
        #return root
        pass

    
Crank().run()
