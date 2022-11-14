import os
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORDS_DIR=os.path.join(BASE_DIR,"words")
IMAGES_DIR=os.path.join(BASE_DIR,"Images")
DATA_CSV=os.path.join(BASE_DIR,"data.csv")

if(not os.path.exists(IMAGES_DIR)):
    os.mkdir(IMAGES_DIR)
    
    
labels = ['বর্ষামুখর', 'দিন', 'শেষে', 'ঊর্দ্ধপানে', 'চেয়ে', 'যখন', 'আষাঢ়ে', 'গল্প', 'শোনাতে', 'বসে', 'ওসমান', 'ভুঁইঞা', 'ঈষান', 'কোণে', 'তখন', 'অন্ধকার', 'মেঘের', 'আড়ম্বর', 'সবুজে', 'ঋদ্ধ', 'বনভূমির', 'নির্জনতা', 'চিরে', 'থেকে', 'হতে', 'ঐরাবতের', 'ডাক', 'মাটির', 'উপর', 'শুকনো', 'পাতা', 'ঝরে', 'পড়ে', 'ঔদাসীন্যে', 'এবং', 'তারই', 'ফাঁকে', 'জমে', 'থাকা', 'ঢের', 'পুরোনো', 'গভীর', 'দুঃখ', 'হঠাৎ', 'যেন', 'বৃষ্টিতে', 'ধুয়ে', 'মুছে', 'ধূসর', 'জীবনে', 'রঙধনু', 'এনে', 'দেয়', 'হৃদয়ের', 'চঞ্চলতা', 'বন্ধে', 'ব্রতী', 'হলে', 'জীবন', 'পরিপূর্ণ', 'হবে', 'নানা', 'রঙের', 'ফুলে', 'কুজ্ঝটিকা', 'প্রভঞ্জন', 'শঙ্কার', 'কারণ', 'লণ্ডভণ্ড',
          'হয়ে', 'যায়', 'ধরার', 'অঙ্গন', 'ক্ষিপ্ত', 'হলে', 'সাঙ্গ', 'হবে', 'বিজ্ঞজনে', 'বলে', 'শান্ত', 'ভাবে', 'এ', 'ব্রহ্মাণ্ডে', 'বাঞ্ছিতফল', 'মেলে', 'শ্রাবনে', 'উত্তর', 'পূর্ব', 'দিকে', 'হঠাৎ', 'ঝড়', 'উঠে', 'গগন', 'মেঘেতে', 'ঢাকে', 'বৃষ্টি', 'নামে', 'মাঠে', 'ঊষার', 'আকাশে', 'সন্ধ্যার', 'ছায়া', 'ঐ', 'দেখো', 'থেমে', 'গেছে', 'পারাপারে', 'খেয়া', 'শরৎ', 'ঋতুতে', 'চাঁদ', 'আলোয়', 'অংশুমান', 'সুখ', 'দুঃখ', 'পাশাপাশি', 'সহ', 'অবস্থান', 'যে', 'জলেতে', 'ঈশ্বর', 'তৃষ্ণা', 'মেটায়', 'সেই', 'জলেতে', 'জীবকুলে', 'বিনাশ', 'ঘটায়', 'রোগ', 'যদি', 'দেহ', 'ছেড়ে', 'মনে', 'গিয়ে', 'ধরে', 'ঔষধের', 'সাধ্য', 'কী', 'বা', 'তারে', 'সুস্থ', 'করে']

labelDict=dict(zip(range(len(labels)),labels))

header = ['Id', 'Image_Name', 'Label']
# data = ['Afghanistan', 652090, 'AF', 'AFG']

with open(DATA_CSV, 'w', encoding='UTF8') as f:
    index=0
    writer = csv.writer(f)
    # writer.writerow(header)
    for dirs in os.listdir(WORDS_DIR):
        for imgs in os.listdir(os.path.join(WORDS_DIR,dirs)):
            writer.writerow([index,os.path.join(WORDS_DIR,dirs,imgs),labelDict.get(int(dirs),"null")])
            index=index+1

    # # write the header
    # writer.writerow(header)

    # # write the data
    # writer.writerow(data)