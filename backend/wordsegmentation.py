# coding=UTF-8
import os
from tqdm import tqdm
import json
import cv2
from PIL import Image
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, 'data')
IMAGES_DIR = os.path.join(BASE_DIR, 'images')
WODRS_DIR = os.path.join(BASE_DIR, 'words')


if(not os.path.exists(WODRS_DIR)):
    os.mkdir(WODRS_DIR)

labels = ['বর্ষামুখর', 'দিন', 'শেষে', 'ঊর্দ্ধপানে', 'চেয়ে', 'যখন', 'আষাঢ়ে', 'গল্প', 'শোনাতে', 'বসে', 'ওসমান', 'ভুঁইঞা', 'ঈষান', 'কোণে', 'তখন', 'অন্ধকার', 'মেঘের', 'আড়ম্বর', 'সবুজে', 'ঋদ্ধ', 'বনভূমির', 'নির্জনতা', 'চিরে', 'থেকে', 'হতে', 'ঐরাবতের', 'ডাক', 'মাটির', 'উপর', 'শুকনো', 'পাতা', 'ঝরে', 'পড়ে', 'ঔদাসীন্যে', 'এবং', 'তারই', 'ফাঁকে', 'জমে', 'থাকা', 'ঢের', 'পুরোনো', 'গভীর', 'দুঃখ', 'হঠাৎ', 'যেন', 'বৃষ্টিতে', 'ধুয়ে', 'মুছে', 'ধূসর', 'জীবনে', 'রঙধনু', 'এনে', 'দেয়', 'হৃদয়ের', 'চঞ্চলতা', 'বন্ধে', 'ব্রতী', 'হলে', 'জীবন', 'পরিপূর্ণ', 'হবে', 'নানা', 'রঙের', 'ফুলে', 'কুজ্ঝটিকা', 'প্রভঞ্জন', 'শঙ্কার', 'কারণ', 'লণ্ডভণ্ড',
          'হয়ে', 'যায়', 'ধরার', 'অঙ্গন', 'ক্ষিপ্ত', 'হলে', 'সাঙ্গ', 'হবে', 'বিজ্ঞজনে', 'বলে', 'শান্ত', 'ভাবে', 'এ', 'ব্রহ্মাণ্ডে', 'বাঞ্ছিতফল', 'মেলে', 'শ্রাবনে', 'উত্তর', 'পূর্ব', 'দিকে', 'হঠাৎ', 'ঝড়', 'উঠে', 'গগন', 'মেঘেতে', 'ঢাকে', 'বৃষ্টি', 'নামে', 'মাঠে', 'ঊষার', 'আকাশে', 'সন্ধ্যার', 'ছায়া', 'ঐ', 'দেখো', 'থেমে', 'গেছে', 'পারাপারে', 'খেয়া', 'শরৎ', 'ঋতুতে', 'চাঁদ', 'আলোয়', 'অংশুমান', 'সুখ', 'দুঃখ', 'পাশাপাশি', 'সহ', 'অবস্থান', 'যে', 'জলেতে', 'ঈশ্বর', 'তৃষ্ণা', 'মেটায়', 'সেই', 'জলেতে', 'জীবকুলে', 'বিনাশ', 'ঘটায়', 'রোগ', 'যদি', 'দেহ', 'ছেড়ে', 'মনে', 'গিয়ে', 'ধরে', 'ঔষধের', 'সাধ্য', 'কী', 'বা', 'তারে', 'সুস্থ', 'করে']

labelToIndexDict=dict(zip(labels,range(len(labels))))


for filePath in tqdm(os.listdir(JSON_DIR)):
    wordDict=dict({})
    [fileName,fileExt]=filePath.split('.')
    if fileExt != 'json':
        print(f"found a non json file: {filePath}")
        break
    with open(os.path.join(JSON_DIR,filePath),'r') as jfile:
        jsonData=json.load(jfile)
        imageFile=jsonData['file']
        imageObj = Image.open(os.path.join(IMAGES_DIR,imageFile))
        # print(imageObj.height)
        bboxes=[]
        for bbox in tqdm(jsonData['boxes']):
            if 'label' in bbox:
                box = np.array([bbox['x'],bbox['y'],bbox['w'],bbox['h']], dtype=np.float64)
                try:
                    # cls=getClassID(bbox['label'])
                    label=bbox['label']
                    label=labelToIndexDict.get(label,-1)
                    localFolder=os.path.join(WODRS_DIR,str(label))
                    if(not os.path.exists(localFolder) and not os.path.isdir(localFolder)):
                        os.mkdir(localFolder)
                    wordDict[label]=wordDict.get(label,-1)+1
                    im1 = imageObj.crop((box[0], box[1], box[0]+box[2], box[1]+box[3]))
                    im1.save(os.path.join(WODRS_DIR,localFolder,f"{fileName}{wordDict[label]}.png"))
                except:
                    continue



