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
                    localFolder=os.path.join(WODRS_DIR,label)
                    if(not os.path.exists(localFolder) and not os.path.isdir(localFolder)):
                        os.mkdir(localFolder)
                    wordDict[label]=wordDict.get(label,-1)+1
                    im1 = imageObj.crop((box[0], box[1], box[0]+box[2], box[1]+box[3]))
                    im1.save(os.path.join(WODRS_DIR,localFolder,f"{fileName}{wordDict[label]}.png"))
                except:
                    continue
                
                

