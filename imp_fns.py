import cv2
import os
import glob
from database import database
def keypairs(profiles):
    dicti ={}
    for i in profiles:
        dicti[i[1]] = i[0]
    return dicti
        
def test_frame():
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("test")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            #img_name = "opencv_frame_{}.png".format(img_counter)
            #cv2.imwrite(img_name, frame)
            print("image taken")
            img_counter += 1
            break 
    cam.release()

    cv2.destroyAllWindows()
    return frame

def train_frame(name):
    cam = cv2.VideoCapture(0)
    #cv2.namedWindow('train')
    img_counter = 1
    while True:
        ret,frame = cam.read()
        cv2.imshow('train',frame)
        if not ret:
            break
        k = cv2.waitKey(1)
        if k%256 == 27:
            print('Esc pressed ,closing')
        elif k%256 == 32:
            img_name = './images/'+"{}_{}.jpg".format(name,img_counter)
            cv2.imwrite(img_name, frame)
            print('image taken')
            img_counter += 1
            if img_counter >= 6:
                break
    cam.release()
    cv2.destroyAllWindows()
    

def delete_files(u_name):
        u_name=u_name.lower()
        u_name.replace(' ','')
        record=database()
        record.connection()
        record.delete_profile(u_name)
        record.break_connection()
        images = glob.glob('./images/'+str(u_name)+'*.jpg')
        for i in images:
            os.remove(i)
        videos = glob.glob('./openpose/trimmed_videos/'+str(u_name)+'*.mp4')
        print(videos)
        for i in videos:
            os.remove(i)
        audios = glob.glob('./audios/'+str(u_name)+'*.wav')
        print(audios)
        for i in audios:
            os.remove(i)
        audios = glob.glob('./audios/'+str(u_name)+'*.gmm')
        print(audios)
        for i in audios:
            os.remove(i)
        print('deleted')
