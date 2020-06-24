import zipfile2 as zipfile

from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np

face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

# function that finds the faces and creates bounding boxes
def find_and_crop(image_file):
    ar_image = np.array(image_file)[:,:,::-1]
    ar_image2 = cv.cvtColor(ar_image, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(ar_image2, 1.3, minNeighbors = 4, minSize = (25, 25), maxSize = (270, 270), flags = cv.CASCADE_SCALE_IMAGE)
    return croptheface(image_file, faces)

# function that crops the faces out of the original image using bounding boxes
def croptheface(filename, faces):
    list_of_faces = []
    for x, y, w, h in faces:
        list_of_faces.append(filename.crop((x, y, x + w, y + h)))
    return list_of_faces

def thumbs_n_nails(pic):
    pic1 = pic.copy()
    pic1.thumbnail((100,100))
    return pic1

# input that will be used later
keyword = input('please enter a word you wish to find on a newspaper page, which will then output a contact sheet of cropped face images on the same page: ')
# creating a dictionary to store PIL.Image files, text strings and bounding boxes in
global_dict = {}
# accum through the list of file names in zip archive
accum = 0
# Unpacking the zip archive and saving PIL.Images into global_dict
with zipfile.ZipFile('small_img.zip', 'r') as archive:
    for image in archive.infolist():
        one_zip_img = archive.open(image)
        global_dict[f'{archive.namelist()[accum]}']= {}
        global_dict[f'{archive.namelist()[accum]}']['PIL'] = Image.open(one_zip_img)
        accum += 1


# Main code for the project - to loop through the keys in global_dict (they are the same as file names)
for page in global_dict:
    # converting image to grayscale first for text search
    paper = global_dict[page]['PIL'].convert('L')
    # creating an entry in the dictionary for the text in every picture, also connecting hyphenated words
    global_dict[page]['newspaper_text'] = pytesseract.image_to_string(paper).replace('-\n', '')
    if keyword in global_dict[page]['newspaper_text']:
        # ONLY cropping the faces out if the keyword IS on a particular page, otherwise the code will take AGES to run
        print(f'Results found in file {page}')
        # list of cropped faces
        cropped_list = find_and_crop(global_dict[page]['PIL'])
        # if list is not empty we are creating a contact sheet
        if len(cropped_list) >= 1:
            coord_x = 0
            coord_y = 0
            collage = Image.new('RGB', (500, 100))
            if len(cropped_list) > 5:
                # If there are more than 5 images, we will need a higher base image
                collage = Image.new('RGB', (500, 200))
            # looping through the faces, the rest is as per project on week 1
            for im in cropped_list:
                collage.paste(thumbs_n_nails(im), (coord_x, coord_y))
                if coord_x + 100 == collage.width:
                    coord_x = 0
                    coord_y = coord_y + 100
                else:
                    coord_x = coord_x + 100
            # creating an entry with a contact sheet of faces, and displaying it
            global_dict[page]['cropped_faces'] = collage
            global_dict[page]['cropped_faces'].show()
        # if list is empty, then printing out that there are no faces in the file.
        else:
            print('But there were no faces in that file !')

