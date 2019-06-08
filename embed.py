import tensorflow as tf
from tensorflow.python.platform import gfile
from tensorflow.core.protobuf import saved_model_pb2
from tensorflow.python.util import compat
import dlib
import cv2
import openface
import numpy as np
import glob
import os

meta_graph = './impstuff/inception model/20170512-110547/model-20170512-110547.meta'
sess_path = './impstuff/inception model/20170512-110547/model-20170512-110547.ckpt-250000'
predictor_model = "./impstuff/shape_predictor_68_face_landmarks.dat"
face_detector = dlib.get_frontal_face_detector()
face_pose_predictor = dlib.shape_predictor(predictor_model)
face_aligner = openface.AlignDlib(predictor_model)

def prewhiten(x):
            mean = np.mean(x)
            std = np.std(x)
            std_adj = np.maximum(std, 1.0/np.sqrt(x.size))
            y = np.multiply(np.subtract(x, mean), 1/std_adj)
            return y
        
def labeler(list):
        label_dict={}
        cnt=1
        for i in list:
            if i not in label_dict:
                label_dict[i] = cnt
                cnt+=1
            else:
                pass
        return label_dict
    
def embedding(face_path,keypairs=None):
    X=[]
    labels=[]
    if keypairs == None:
        keypairs = labeler(labels)
    image_path = glob.glob(os.path.join(face_path,'*.jpg'))
    with tf.Graph().as_default():
        with tf.Session() as sess:
            saver = tf.train.import_meta_graph(meta_graph)
            saver.restore(tf.get_default_session(), sess_path)
            for j in image_path:
                image = cv2.imread(j)
                detected_faces = face_detector(image, 1)
                #print(len(detected_faces))
                if len(detected_faces)>0:
                    labels.append(keypairs[j.split('\\')[-1].split('_')[0]])
                    for i, face_rect in enumerate(detected_faces):
                        pose_landmarks = face_pose_predictor(image, face_rect)
                        alignedFace = face_aligner.align(160, image, face_rect, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
                        alignedFace = prewhiten(alignedFace)
                        #img1 = cv2.rectangle(image,(face_rect.left(),face_rect.bottom()),(face_rect.right(),face_rect.top()),(255,0,0),2)
                        images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
                        embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
                        phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
                        alignedFace = alignedFace.reshape(-1,160,160,3)
                        output = sess.run(embeddings,feed_dict={images_placeholder:alignedFace,phase_train_placeholder: False})
                        X.append(output)
            print(np.array(X).shape)
    return np.squeeze(np.array(X),axis=1),np.array(labels)
    
def predictor(image):
    #image = cv2.imread(image_path)
    if type(image).__name__ == 'ndarray':
        with tf.Graph().as_default():
            with tf.Session() as sess:
                saver = tf.train.import_meta_graph(meta_graph)
                saver.restore(tf.get_default_session(), sess_path)
                detected_faces = face_detector(image, 1)
                if len(detected_faces)>0:
                    for i, face_rect in enumerate(detected_faces):
                        pose_landmarks = face_pose_predictor(image, face_rect)
                        alignedFace = face_aligner.align(160, image, face_rect, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
                        alignedFace = prewhiten(alignedFace)
                        #img1 = cv2.rectangle(image,(face_rect.left(),face_rect.bottom()),(face_rect.right(),face_rect.top()),(255,0,0),2)
                        images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
                        embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
                        phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
                        alignedFace = alignedFace.reshape(-1,160,160,3)
                        output = sess.run(embeddings,feed_dict={images_placeholder:alignedFace,phase_train_placeholder: False})
                else:
                    output = []
    return output
