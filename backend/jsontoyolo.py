import os
from tqdm import tqdm
import json
import cv2
from PIL import Image
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, 'data')
IMAGES_DIR = os.path.join(BASE_DIR, 'images')
YOLO_DIR = os.path.join(BASE_DIR, 'yolov5')

labels = ['বর্ষামুখর', 'দিন', 'শেষে', 'ঊর্দ্ধপানে', 'চেয়ে', 'যখন', 'আষাঢ়ে', 'গল্প', 'শোনাতে', 'বসে', 'ওসমান', 'ভুঁইঞা', 'ঈষান', 'কোণে', 'তখন', 'অন্ধকার', 'মেঘের', 'আড়ম্বর', 'সবুজে', 'ঋদ্ধ', 'বনভূমির', 'নির্জনতা', 'চিরে', 'থেকে', 'হতে', 'ঐরাবতের', 'ডাক', 'মাটির', 'উপর', 'শুকনো', 'পাতা', 'ঝরে', 'পড়ে', 'ঔদাসীন্যে', 'এবং', 'তারই', 'ফাঁকে', 'জমে', 'থাকা', 'ঢের', 'পুরোনো', 'গভীর', 'দুঃখ', 'হঠাৎ', 'যেন', 'বৃষ্টিতে', 'ধুয়ে', 'মুছে', 'ধূসর', 'জীবনে', 'রঙধনু', 'এনে', 'দেয়', 'হৃদয়ের', 'চঞ্চলতা', 'বন্ধে', 'ব্রতী', 'হলে', 'জীবন', 'পরিপূর্ণ', 'হবে', 'নানা', 'রঙের', 'ফুলে', 'কুজ্ঝটিকা', 'প্রভঞ্জন', 'শঙ্কার', 'কারণ', 'লণ্ডভণ্ড',
          'হয়ে', 'যায়', 'ধরার', 'অঙ্গন', 'ক্ষিপ্ত', 'হলে', 'সাঙ্গ', 'হবে', 'বিজ্ঞজনে', 'বলে', 'শান্ত', 'ভাবে', 'এ', 'ব্রহ্মাণ্ডে', 'বাঞ্ছিতফল', 'মেলে', 'শ্রাবনে', 'উত্তর', 'পূর্ব', 'দিকে', 'হঠাৎ', 'ঝড়', 'উঠে', 'গগন', 'মেঘেতে', 'ঢাকে', 'বৃষ্টি', 'নামে', 'মাঠে', 'ঊষার', 'আকাশে', 'সন্ধ্যার', 'ছায়া', 'ঐ', 'দেখো', 'থেমে', 'গেছে', 'পারাপারে', 'খেয়া', 'শরৎ', 'ঋতুতে', 'চাঁদ', 'আলোয়', 'অংশুমান', 'সুখ', 'দুঃখ', 'পাশাপাশি', 'সহ', 'অবস্থান', 'যে', 'জলেতে', 'ঈশ্বর', 'তৃষ্ণা', 'মেটায়', 'সেই', 'জলেতে', 'জীবকুলে', 'বিনাশ', 'ঘটায়', 'রোগ', 'যদি', 'দেহ', 'ছেড়ে', 'মনে', 'গিয়ে', 'ধরে', 'ঔষধের', 'সাধ্য', 'কী', 'বা', 'তারে', 'সুস্থ', 'করে']

categoriesDict =dict(zip(range(len(labels)),labels))
with open(os.path.join(BASE_DIR,'classes.txt'),'w') as f:
    for k,v in categoriesDict.items():
        f.write(f"{k}: {v}\n")
# print(categoriesDict)

def getClassID(val):
    for key, value in categoriesDict.items():
        if val == value:
            return key
 
    raise Exception(f"Key not found for : {val}")

for filePath in tqdm(os.listdir(JSON_DIR)):
    [fileName,fileExt]=filePath.split('.')
    if fileExt != 'json':
        print(f"found a non json file: {filePath}")
        break
    with open(os.path.join(JSON_DIR,filePath),'r') as jfile:
        jsonData=json.load(jfile)
        imageFile=jsonData['file']
        imageObj=cv2.imread(os.path.join(IMAGES_DIR,imageFile))
        # print(imageObj.height)
        bboxes=[]
        for bbox in tqdm(jsonData['boxes']):
            if 'label' in bbox:
                box = np.array([bbox['x'],bbox['y'],bbox['w'],bbox['h']], dtype=np.float64)
                box[:2] += box[2:] / 2  # xy top-left corner to center
                box[[0, 2]] /= imageObj.shape[1]  # normalize x
                box[[1, 3]] /= imageObj.shape[0]  # normalize y
                if box[2] <= 0 or box[3] <= 0:  # if w <= 0 and h <= 0
                    continue
                
                try:
                    cls=getClassID(bbox['label'])
                except:
                    continue
                # cv2.rectangle(imageObj, (box[0]-box[2], box[1]+box[3]), (box[0]+box[2], box[1]-box[3]), (0, 0, 255), 1)
                box = [cls] + box.tolist()
                if box not in bboxes:
                    bboxes.append(box)
                # [x,y,w,h,label]=[box['x'],box['y'],box['w'],box['h'],box['label']]
                # try:
                #     id = getClassID(label)
                # except:
                #     continue
                # h=int(h)
                # x=int(x)
                # y=int(y)
                # w=int(w)
                # print(f"{id} {type(x)} {type(y)} {type(w)} {type(h)}")
                # cv2.rectangle(imageObj, (x, y), (x + w, y + h), (0, 0, 255), 1)
            # print(box['x'])
        # cv2.imwrite(os.path.join(YOLO_DIR,imageFile), imageObj)
        with open((os.path.join(YOLO_DIR,fileName+'.txt')), 'w') as file:
            for box in bboxes:
                file.write(f"{box[0]} {box[1]} {box[2]} {box[3]} {box[4]}\n")
