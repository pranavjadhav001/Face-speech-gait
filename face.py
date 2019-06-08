import glob
from sklearn.svm import SVC
import pickle
import os
import cv2
from embed import embedding,predictor
from database import database
import numpy as np
from imp_fns import test_frame
def keypairs(profiles):
    dicti ={}
    for i in profiles:
        dicti[i[1]] = i[0]
    return dicti

class face:
    def __init__(self,face_path ='./images'):
        self.face_path = face_path
        
    def labeler(self,list):
        label_dict={}
        cnt=1
        for i in list:
            if i not in label_dict:
                label_dict[i] = cnt
                cnt+=1
            else:
                pass
        return label_dict
    
    def train(self,keypairs=None):
        image_path = glob.glob(os.path.join(self.face_path,'*.jpg'))
        print(len(image_path))
        X=[]
        labels=[]
        Y_train = []
        for i in image_path:
            labels.append(i.split('\\')[-1].split('_')[0])
            image = cv2.imread(i)
            X.append(image)
        print(len(X))
        embeddings = embedding(X)
        if keypairs == None:
            keypairs = self.labeler(labels)
        for i in labels:
            if i in keypairs:
                Y_train.append(keypairs[i])
            else:
                print('key not found')
        return embeddings, Y_train

    def train2(self,keypairs=None):
        if len(keypairs) > 1:
            x,y = embedding(self.face_path,keypairs)
            #print(x.shape,y.shape)
            self.svm_train(x,y)
            return x,y
        elif len(keypairs) == 1:
            print('only 1 profile')
            return 
            
            
            

    def svm_train(self,x,y):
        clf = SVC(kernel='linear')
        clf.fit(x,y)
        with open(os.path.join(self.face_path,'face_model.pkl'),'wb') as f:
            pickle.dump(clf,f)
        print('training completed')

    def prediction(self,keypairs,model_path=None):
        if model_path == None:
            model_path = os.path.join(self.face_path,'face_model.pkl')
        if os.path.exists(model_path):
            with open(model_path,'rb') as f:
                clf = pickle.load(f)
            inv_map = {v:k for k,v in keypairs.items()}
            test_image = test_frame()
            output = predictor(test_image)
            return inv_map[clf.predict(output)[0]]
        else:
            if len(keypairs)== 1:
                print('only 1 profile')
                test_image = test_frame()
                return list(keypairs.keys())[0]
                
                
if __name__=='__main__':
    database = database()
    database.connection()
    face = face()
    #face.prediction('./images/pranav.36.jpg',keypairs(database.get_profile()))
