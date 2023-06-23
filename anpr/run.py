from flask import Flask, render_template, request
from PIL import Image
import pytesseract
import cv2
import re
import os
import xml.dom.minidom as dom

app = Flask(__name__)
'''result=""
NP="" '''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    result=""
    NP=[]
    text1=""
    if request.method == 'POST':
        upload_file = request.files['file']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], upload_file.filename)
        upload_file.save(file_path)
        if upload_file.filename.lower().endswith(('.mp4', '.avi')):
            
            #if request.method == 'POST':
                # Open the video file
                
                
                # Open the video file using cv2.VideoCapture()
                video = cv2.VideoCapture(file_path)
                
                while True:
                    # Read the frame from the video
                    ret, frame = video.read()
                    if not ret:
                        break

                    # Convert the image to grayscale
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    # Apply adaptive thresholding to binarize the image
                    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

                    # Find contours in the binary image
                    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    
                    '''
                    # Crop the image using the bounding box
                    crop = frame[y:y+h, x:x+w]
                    cv2.imshow('crop_img',crop)

                    # Save the cropped image
                    #cv2.imwrite('cropped_image.jpg', crop)
                    '''
                    for contour in contours:
                        x,y,w,h = cv2.boundingRect(contour)
                        if w*h > 10000: # set minimum area size threshold to avoid noise // 10000
                            crop_img = gray[y:y+h, x:x+w]
                            #cv2.imshow('crop',crop_img)
                            #cv2.waitKey(0)
                            temp=text=pytesseract.image_to_string(crop_img, lang ='eng',config ='--oem 3 --psm 6')
                            #print(temp)
                            if(len(temp)!=0):
                                result+=text.strip()+""

                video.release()
                
                NumberPlates=re.findall("[A-Z]{2}[0-9]{2}[A-Z][0-9]{4}|[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}|[A-Z]{2}[0-9]{2}[A-Z]{3}[0-9]{4}",result)
                #print(NumberPlates)
                for j in NumberPlates:
                    
                    if(j not in NP):
                        NP.append(j)
                for i in NP:
                    text1+=i+"\n"
                
        elif upload_file.filename.lower().endswith(('.jpg', '.jpeg','.png','.jfif','.JPG','.PNG')):
                #path='uploads/'+ upload_file.filename
                
                img = cv2.imread(file_path)
            
                # Convert the image to grayscale
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # Apply adaptive thresholding to binarize the image
                thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)


                # Find contours in the binary image
                contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


                # Crop the areas with text
                for contour in contours:
                    x,y,w,h = cv2.boundingRect(contour)
                    if w*h > 10000: # set minimum area size threshold to avoid noise
                        crop_img = gray[y:y+h, x:x+w]
                    
                        temp=text=pytesseract.image_to_string(crop_img,lang ='eng',config ='--oem 3 --psm 6')
                        #print(temp)
                        if(len(temp)!=0):
                            result+=text+"\n"
                        '''cv2.imshow('crop_img', crop_img)
                        cv2.waitKey(0)'''
                NumberPlates=re.findall("[A-Z]{2}[0-9]{2}[A-Z][0-9]{4}|[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}|[A-Z]{2}[0-9]{2}[A-Z]{3}[0-9]{4}",result)
                #print(NumberPlates)
                for j in NumberPlates:
                    
                    if(j not in NP):
                        NP.append(j)
                for i in NP:
                    text1+=i+"\n"
                
        
    return render_template('result.html', text=text1)

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = './uploads'
    app.run(debug=True)
