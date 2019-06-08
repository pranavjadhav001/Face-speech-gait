import numpy as np
import random
import glob
import os
import json
from database import database
from imp_fns import keypairs
from sklearn import svm
import pickle

#record = database()
def gait_train(dic):
    all_names = []
    for i in dic:
        all_names.append(i+'_1')
        all_names.append(i+'_2')
        all_names.append(i+'_3')
    data_dict = {}
    for i in all_names:
        data = glob.glob(os.path.join('C:\Python36\gui_project\openpose\json_output',i+'*.json'))
        #print(i)
        data_dict[i] = list()
        #print(len(data))
        if len(data) > 42:
            new = np.arange(0,len(data))
            new_list = random.sample(list(new),42)
            new_list.sort()
            for j in new_list:
                #print(j)
                if j//10 == 0:
                    path = os.path.join('C:\Python36\gui_project\openpose\json_output',i+'_00000000000'+str(j)+'_keypoints.json')
                elif j//10 == 1:
                    path = os.path.join('C:\Python36\gui_project\openpose\json_output',i+'_0000000000'+str(j)+'_keypoints.json')
                elif j//10 == 10:
                    path = os.path.join('C:\Python36\gui_project\openpose\json_output',i+'_000000000'+str(j)+'_keypoints.json')
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        datastore = json.load(f)
                        data_dict[i].append(datastore['people'][0]['pose_keypoints_2d'])
                    #print('yes')
                else: print('not found')
        else:
            print('insufficient frames')

    return data_dict
def prediction(file_name,profile_name,dicti):
    with open('model.pkl','rb') as f:
        clf = pickle.load(f)
    name = file_name.split('\\')[-1].split('.')[0]
    data_dict = list()
    data = glob.glob(os.path.join('C:\Python36\gui_project\openpose\output',name+'*.json'))
    print(len(data))
    if len(data) > 42:
        new = np.arange(0,len(data))
        new_list = random.sample(list(new),42)
        new_list.sort()
        for j in new_list:
            if j//10 == 0:
                path = os.path.join('C:\Python36\gui_project\openpose\output',name+'_00000000000'+str(j)+'_keypoints.json')
            elif j//10 == 1:
                path = os.path.join('C:\Python36\gui_project\openpose\output',name+'_0000000000'+str(j)+'_keypoints.json')
            elif j//10 == 10:
                path = os.path.join('C:\Python36\gui_project\openpose\output',name+'_000000000'+str(j)+'_keypoints.json')
            if os.path.exists(path):
                with open(path, 'r') as f:
                    datastore = json.load(f)
                    data_dict.append(datastore['people'][0]['pose_keypoints_2d'])
        y = np.array(data_dict).reshape(1,3150)
        print(y.shape)
        inv_map = {v:k for k,v in dicti.items()}
        print(inv_map)
        print(clf.predict(y))
    return inv_map[clf.predict(y)[0]]


def svm_train(x,y):
    clf = svm.SVC(kernel='linear')
    clf.fit(x,y)
    with open('model.pkl','wb') as f:
        pickle.dump(clf,f)
    print('training completed')
