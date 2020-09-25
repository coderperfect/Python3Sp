import zipfile

from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

# the rest is up to you!

import zipfile
import io

# create handle to zipfile
# get filenames from ziphandle.namelist()

# loop over the filenames: 
#     #extract file from zip in memory
#     get_img = ziphandle.read(name of image)
    
#     # then as a flie type handle
#     fh = io.BtyesIO(get_img)
#     img = Image.open(fh)
#     display(img)
    
    
images = {}

name_list = []

def unzip_images(zip_name):
    zf = zipfile.ZipFile(zip_name)
    
    for each in zf.infolist():
        images[each.filename] = [Image.open(zf.open(each.filename))]
        name_list.append(each.filename)
        
if __name__ == '__main__':
    unzip_images('readonly/images.zip')
    
    for name in name_list:
        img = images[name][0]
        
        images[name].append(pytesseract.image_to_string(img).replace('-\n',''))
        
        if 'Mark' in images[name][1]:
            print('Results found in file', name)
            
            try:
                faces = (face_cascade.detectMultiScale(np.array(img), 1.35, 4)).tolist()
                images[name].append(faces)
                
                faces_in_each = []
                
                for x,y,w,h in images[name][2]:
                    faces_in_each.append(img.crop((x,y,x+w,y+h)))
                    
                contact_sheet = Image.new(img.mode, (550,110*int(np.ceil(len(faces_in_each)/5))))
                x = 0
                y = 0
                
                for face in faces_in_each:
                    face.thumbnail((110, 110))
                    contact_sheet.paste(face, (x,y))
                    
                    if x+110 == contact_sheet.width:
                        x = 0
                        y = y+110
                    else:
                        x = x+110
                        
                display(contact_sheet)
            except:
                print('But there were no faces in that file!')