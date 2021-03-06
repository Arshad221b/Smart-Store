import cv2
import numpy as np
from keras.models import load_model
from skimage.transform import resize, pyramid_reduce
import PIL
from PIL import Image
import time

model = load_model('Facemodel.h5')

face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_alt.xml')


def prediction(pred):
    if pred == 0:
        return('Angry')
    elif pred == 1:
        return('Disgust')
    elif pred == 2:
        return('Fear')
    elif pred == 3:
        return('Happy')
    elif pred == 4:
        return('Sad')
    elif pred == 5:
        return('Surprise')
    elif pred == 6:
        return('Neutral')
    


def keras_predict(model, image):
    data = np.asarray( image, dtype="int32" )
    
    pred_probab = model.predict(data)[0]
    pred_class = list(pred_probab).index(max(pred_probab))
    return max(pred_probab), pred_class

def keras_process_image(img):
    
    image_x = 28
    image_y = 28
    img = cv2.resize(img, (1,28,28), interpolation = cv2.INTER_AREA)
  
    return img
 

def crop_image(image, x, y, width, height):
    return image[y:y + height, x:x + width]

def main():
    l = []
    
    while True:
        
        cam_capture = cv2.VideoCapture(0)
        _, image_frame = cam_capture.read()  
    # Select ROI
        faces = face_cascade.detectMultiScale(image_frame, 1.5, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(image_frame, (x,y),(x+w,y+h),(0,0,255),2)
        
            im2 = crop_image(image_frame, x,y,x+w,y+h)
            image_grayscale = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
    
            #image_grayscale_blurred = cv2.GaussianBlur(image_grayscale, (15,15), 0)
            #im3 = cv2.resize(image_grayscale_blurred, (48,48), interpolation = cv2.INTER_AREA)


    
            im4 = np.resize(im2, (48, 48, 1))
            im5 = np.expand_dims(im4, axis=0)
    

            pred_probab, pred_class = keras_predict(model, im5)
            prob = str(pred_probab)
            curr = prediction(pred_class)
          
            cv2.putText(image_frame, curr, (x, y), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 255), lineType=cv2.LINE_AA)
            #cv2.putText(image_frame, prob, (x - 100, y), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 255), lineType=cv2.LINE_AA)
            
    
 
    # Display cropped image
        #sscv2.rectangle(image_frame, (300, 300), (600, 600), (255, 255, 00), 3)
        cv2.imshow("frame",image_frame)
        
        
    #cv2.imshow("Image4",resized_img)
        #cv2.imshow("Image3",image_grayscale_blurred)

        if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
#.......................................................................



if __name__ == '__main__':
    main()

cam_capture.release()
cv2.destroyAllWindows()
