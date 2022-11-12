import shutil
import os

DIR=os.path.dirname(os.path.abspath(__file__))
DIR=os.path.join(DIR,'datasets','bangla')

IMG_DIR=os.path.join(DIR,'images')
DATA_DIR=os.path.join(DIR,'labels')

# print(os.listdir(IMG_DIR))
seed=5

for file in os.listdir(IMG_DIR):
    for i in range(seed):
        try:
            name,ext=file.split('.')
        except:
            print(file)
        shutil.copy(os.path.join(IMG_DIR,file),os.path.join(IMG_DIR,name)+f"copy_{i}.{ext}")
        
for file in os.listdir(DATA_DIR):
    for i in range(seed):
        try:
            name,ext=file.split('.')
        except:
            print(file)
        shutil.copy(os.path.join(DATA_DIR,file),os.path.join(DATA_DIR,name)+f"copy_{i}.{ext}")