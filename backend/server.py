from ast import arg
from crypt import methods
from sqlite3 import DatabaseError
from traceback import print_tb
from urllib import response
from flask import Flask, request, abort
import flask
from PIL import Image
import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import base64
import cv2 as cv2
import json
app = Flask(__name__)

# print(os.path.abspath(os.getcwd()))

BASE_DIR = os.path.join(os.path.abspath(os.getcwd()))

IMAGES_DIR = os.path.join(BASE_DIR, 'images')
DATA_DIR = os.path.join(BASE_DIR, 'data')


def data_contains(file):
    name = file.split(".")[0]
    json_file = os.path.join(DATA_DIR, name+'.json')
    val = False
    print(json_file)
    if (os.path.exists(json_file)):
        val = True
    return {'file': file, 'data': val}


def get_list():
    img_list = os.listdir(IMAGES_DIR)
    val = map(data_contains, img_list)
    return list(val)


def do_processing(path):
    image = cv2.imread(path)
    original = image.copy()
    # re_sized_img = cv2.resize(image, (800, 800), interpolation = cv2.INTER_AREA)
    re_sized_img = image
    gray = cv2.cvtColor(re_sized_img, cv2.COLOR_BGR2GRAY)
    ret, thresh_img = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = np.ones((5, 10), np.uint8)
    dilated = cv2.dilate(thresh_img, kernel, iterations=1)

    cnts = cv2.findContours(dilated, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    local_img = re_sized_img.copy()
    box_list = []
    for idx, c in enumerate(cnts):
        x, y, w, h = cv2.boundingRect(c)
        # print({'x':x,'y':y,'width':w,'height':h,'label':labels[idx] if idx<len(labels) else " "})
        box_list.append({'id': idx, 'x': x, 'y': y, 'w': w, 'h': h})
        cv2.rectangle(local_img, (x, y), (x + w, y + h), (0, 0, 255), 1)

    cv2.imwrite('./test.png', local_img)

    box_list = sorted(box_list, key=lambda a: (a['x'], a['y']))
    # print(box_list)
    return box_list


@app.route('/api/images', methods=['GET'])
def get_image_names():
    if request.method == 'GET':
        return flask.jsonify(get_list())


@app.route('/images/<image>', methods=['GET'])
def get_image(image):
    img_path = os.path.join(IMAGES_DIR, image)
    if (os.path.exists(img_path)):
        return flask.send_file(img_path)
        # with open(img_path, "rb") as f:
        #     # print(base64.b64encode(f.read()))
        #     return base64.b64encode(f.read())
    abort(500)


@app.route('/boxes/<image>', methods=['GET'])
def get_boxes(image):
    
    file_path=os.path.join(DATA_DIR,image.split('.')[0]+'.json')
    if(os.path.exists(file_path)):
        with open(file_path,'r') as readfile:
            json_data=json.load(readfile)
            return flask.jsonify({"list": json_data['boxes']})
            
    
    img_path = os.path.join(IMAGES_DIR, image)
    if (os.path.exists(img_path)):
        return flask.jsonify({"list": do_processing(img_path)})
    abort(500)


@app.route('/api/labels', methods=['GET'])
def get_labels():
    labels = ['বর্ষামুখর', 'দিন', 'শেষে', ',', 'ঊর্দ্ধপানে', 'চেয়ে', 'যখন', 'আষাঢ়ে', 'গল্প', 'শোনাতে', 'বসে', 'ওসমান', 'ভুঁইঞা', ',', 'ঈষান', 'কোণে', 'তখন', 'অন্ধকার', 'মেঘের', 'আড়ম্বর', ',', 'সবুজে', 'ঋদ্ধ', 'বনভূমির', 'নির্জনতা', 'চিরে', 'থেকে', 'হতে', 'ঐরাবতের', 'ডাক', ',', 'মাটির', 'উপর', 'শুকনো', 'পাতা', 'ঝরে', 'পড়ে', 'ঔদাসীন্যে', ',', 'এবং', 'তারই', 'ফাঁকে', 'জমে', 'থাকা', 'ঢের', 'পুরোনো', 'গভীর', 'দুঃখ', 'হঠাৎ', 'যেন', 'বৃষ্টিতে', 'ধুয়ে', 'মুছে', 'ধূসর', 'জীবনে', 'রঙধনু', 'এনে', 'দেয়', '।', 'হৃদয়ের', 'চঞ্চলতা', 'বন্ধে', 'ব্রতী', 'হলে', 'জীবন', 'পরিপূর্ণ', 'হবে', 'নানা', 'রঙের', 'ফুলে', '।', 'কুজ্ঝটিকা', 'প্রভঞ্জন', 'শঙ্কার', 'কারণ', 'লণ্ডভণ্ড',
              'হয়ে', 'যায়', 'ধরার', 'অঙ্গন', '।', 'ক্ষিপ্ত', 'হলে', 'সাঙ্গ', 'হবে', 'বিজ্ঞজনে', 'বলে', 'শান্ত', 'ভাবে', 'এ', 'ব্রহ্মাণ্ডে', 'বাঞ্ছিতফল', 'মেলে', '।', 'শ্রাবনে', 'উত্তর', 'পূর্ব', 'দিকে', '', 'হঠাৎ', 'ঝড়', 'উঠে', 'গগন', 'মেঘেতে', 'ঢাকে', 'বৃষ্টি', 'নামে', 'মাঠে', 'ঊষার', 'আকাশে', 'সন্ধ্যার', 'ছায়া', 'ঐ', 'দেখো', 'থেমে', 'গেছে', 'পারাপারে', 'খেয়া', '।', 'শরৎ', 'ঋতুতে', 'চাঁদ', 'আলোয়', 'অংশুমান', 'সুখ', 'দুঃখ', 'পাশাপাশি', 'সহ', 'অবস্থান', '।', 'যে', 'জলেতে', 'ঈশ্বর', 'তৃষ্ণা', 'মেটায়', 'সেই', 'জলেতে', 'জীবকুলে', 'বিনাশ', 'ঘটায়', '।', 'রোগ', 'যদি', 'দেহ', 'ছেড়ে', 'মনে', 'গিয়ে', 'ধরে', 'ঔষধের', 'সাধ্য', 'কী', 'বা', 'তারে', 'সুস্থ', 'করে', '?']
    return flask.jsonify(labels)


@app.route('/api/save/<image>', methods=['POST'])
def save_data(image):
    # print(request.get_json())
    # mydata = json.loads(request.get_data())
    file_name = image.split('.')[0]
    with open(os.path.join(DATA_DIR, file_name+'.json'),'w') as outfile:
        json.dump(request.get_json(), outfile, indent=4,sort_keys=True)
    return ('Saved',200)

@app.route('/api/delete/<image>', methods=['GET'])
def delete_data(image):
    # print(request.get_json())
    # mydata = json.loads(request.get_data())
    file_name = image.split('.')[0]
    # os.remove(os.path.join(DATA_DIR, file_name+'.json'))
    return ('Deleted',200)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
