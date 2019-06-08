import glob
import pickle
import numpy as np
from scipy.io.wavfile import read
import sklearn.mixture 
from speakerfeatures import extract_features
import warnings
import os
warnings.simplefilter("ignore")

class speechy:
    def __init__(self,audio_path='./audios'):
        self.audio_path = audio_path

    def train(self,samples=3):
        audio_paths = glob.glob(self.audio_path+'/*.wav')
        count = 1
        for path in audio_paths:
            user = path.split('\\')[-1].split('_')[0]
            print(user)
            
# Extracting features for each speaker (5 files per speakers)
            features = np.asarray(())
            print(path)
            sr,audio = read(path)
            # extract 40 dimensional MFCC & delta MFCC features
            vector   = extract_features(audio,sr)
            if features.size == 0:
                features = vector
            else:
                features = np.vstack((features, vector))
            if count == samples:    
                gmm = sklearn.mixture.GaussianMixture(n_components = 16, max_iter = 200, covariance_type='diag',n_init = 3)
                gmm.fit(features)
                # dumping the trained gaussian model
                picklefile = os.path.join(self.audio_path,user.split('.')[0]+".gmm")
                pickle.dump(gmm,open(picklefile,'wb'))
                print('modeling completed for speaker:',picklefile," with data point = ",features.shape)   
                features = np.asarray(())
                count = 0
            count = count + 1
                
            
    def predict(self,test_path):
        sr,audio = read(test_path)
        vector   = extract_features(audio,sr)
        gmms = glob.glob(os.path.join(self.audio_path,'*.gmm'))
        #print(gmms)
        scores = []
        for i in gmms:
            #print(i)
            user = pickle.load(open(i,'rb'))
            scores.append((i.split('\\')[-1].split('.')[0],user.score(vector)))
            #print(scores)
        print(scores)
        return sorted(scores, key=lambda x: x[1], reverse=True)[0][0]
