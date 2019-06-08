# Face-speech-gait
A 3-stage bio-metric app, that checks a person on all 3 levels.
## Prerequisites
- Tensorflow == 1.12
- Dlib == 19.8.1
- sklearn == 0.20.2
- kivy == 1.10.1
- openface
- OpenCv == 4.0.0
- sqlite3
- numpy
- pillow
- wave
- python_speech_features
- scipy
- Download dlib shape predictor dat file and place it in impstuff folder
- Download facenet pretrained model and place it in impstuff folder
link:https://github.com/davidsandberg/facenet
- Download openpose.exe binary from https://github.com/CMU-Perceptual-Computing-Lab/openpose/releases and unzip it.
## Concept Used 
#### Face recognition
- Captures 5 images of new profile and saves it in the database.
- Using facenet's pretrained model , get 128 embeddings for each face and use svm to classify.
- During predicting, It predicts from the various profiles in the app.
- To capture a frame, opencv is used, to detect a face dlib is used, to align the face in the centre, openface is used.
#### Speech Recognition
- When a new profile comes, he/she has to record and save 3 audio files of 2 sec each with same phrase ,i.e. characteristic to the profile.
- Using python_speech_features , get mfcc features of each audio files and also their derivative, concatenate all 3 files into 1 for each profile.
- Use gmm as a probalistic model, to get create gmm models.
- During prediction, the score of the audio file is compared with all gmm files of profiles, if the one with highest score, is the same profile, True , otherwise , give one more chance.
#### Gait Recognition
- Select 3 videos of a person , video length not more than 2 secs, openpose.exe will compute the keypoints of the person walking in frame and save output as .json file for each frame.
- choose predefined no. of frames(say 50) , since all videos don't have equal frames , and pick 50 frames from each video at equal distance.
- These keypoints will be the features and the labels will be the person walking in the frame.
- Train a classifier like svm and predict.
## Screens
1. <img src="https://github.com/pranavjadhav001/Face-speech-gait/blob/master/screenshots/Capture1.PNG" width="400" height="400">
2. <img src="https://github.com/pranavjadhav001/Face-speech-gait/blob/master/screenshots/Capture2.PNG" width="400" height="400">
3. <img src="https://github.com/pranavjadhav001/Face-speech-gait/blob/master/screenshots/Capture3.PNG" width="400" height="400">
4. <img src="https://github.com/pranavjadhav001/Face-speech-gait/blob/master/screenshots/Capture4.PNG" width="400" height="400">
5. <img src="https://github.com/pranavjadhav001/Face-speech-gait/blob/master/screenshots/Capture5.PNG" width="400" height="400">
6. <img src="https://github.com/pranavjadhav001/Face-speech-gait/blob/master/screenshots/Capture6.PNG" width="400" height="400">
7. <img src="https://github.com/pranavjadhav001/Face-speech-gait/blob/master/screenshots/Capture7.PNG" width="400" height="400">
8. <img src="https://github.com/pranavjadhav001/Face-speech-gait/blob/master/screenshots/Capture8.PNG" width="400" height="400">
9. <img src="https://github.com/pranavjadhav001/Face-speech-gait/blob/master/screenshots/Capture9.PNG" width="400" height="400">
10. <img src="https://github.com/pranavjadhav001/Face-speech-gait/blob/master/screenshots/Capture10.PNG" width="400" height="400">
11. <img src="https://github.com/pranavjadhav001/Face-speech-gait/blob/master/screenshots/Capture11.PNG" width="400" height="400">
12. <img src="https://github.com/pranavjadhav001/Face-speech-gait/blob/master/screenshots/Capture12.PNG" width="400" height="400">
13. <img src="https://github.com/pranavjadhav001/Face-speech-gait/blob/master/screenshots/Capture13.PNG" width="400" height="400">
