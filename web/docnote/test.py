from zipfile import *
import shutil
import os
my_dir = 'temp/uploads/'
myzip = ZipFile('hahah', 'w', ZIP_DEFLATED) 
for file_name in os.listdir(my_dir): 
    file_path = my_dir + file_name 
    print(file_path) 
    myzip.write(file_path,file_name) 
myzip.close() 

for file_name in os.listdir(my_dir):
    os.remove(my_dir+file_name)

shutil.copyfile('hahah','temp/uploads/haha2')
