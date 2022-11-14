import os
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORDS_DIR=os.path.join(BASE_DIR,"words")
IMAGES_DIR=os.path.join(BASE_DIR,"Images")
DATA_CSV=os.path.join(BASE_DIR,"data.csv")

if(not os.path.exists(IMAGES_DIR)):
    os.mkdir(IMAGES_DIR)
    
    

    
  

header = ['Id', 'Image_Name', 'Label']
# data = ['Afghanistan', 652090, 'AF', 'AFG']

with open(DATA_CSV, 'w', encoding='UTF8') as f:
    index=0
    writer = csv.writer(f)
    # writer.writerow(header)
    for dirs in os.listdir(WORDS_DIR):
        for imgs in os.listdir(os.path.join(WORDS_DIR,dirs)):
            writer.writerow([index,os.path.join(WORDS_DIR,dirs,imgs),dirs])
            index=index+1

    # # write the header
    # writer.writerow(header)

    # # write the data
    # writer.writerow(data)