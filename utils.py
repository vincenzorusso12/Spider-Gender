import os,shutil,csv
from zipfile import ZipFile
from numpy import loadtxt
from numpy import savetxt
import numpy as np
import random

def makedir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def unzip(zip,dest):
    with ZipFile(zip, 'r') as zipObj:
        if len(os.listdir(dest)) == 0:
            zipObj.extractall(dest)


#Fa il merge di entrambi oppure solo di CelebA (path UTKFace None)
def merge_datasets(path_images_celeba2,path_images_utkface2,path_celeba_csv2,dest_path,dest_path_oldnew_csv):
    # Merging parte di CelebA
    # Copia le immagini in merged_dataset\images e crea un file csv dove mappo oldname_newname

    with open(path_celeba_csv2) as csv_file, \
            open(os.path.join(dest_path_oldnew_csv, "oldname_newname.csv"), mode='w', newline="") as name_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        name_writer = csv.writer(name_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                name_writer.writerow(['Old_Name', 'New_Name'])
            else:
                line_count += 1
                if (row[21] == "1"):
                    new_file_name = '%06d_1.jpg' % (line_count - 1,)  # Caso Uomo
                else:
                    new_file_name = '%06d_0.jpg' % (line_count - 1,)  # Caso Donna
                shutil.copy(os.path.join(path_images_celeba2, row[0]), os.path.join(dest_path, new_file_name))
                name_writer.writerow([row[0], new_file_name])

                # Merging parte UTKFace
        if path_images_utkface2 is not None:
            for filename in os.listdir(path_images_utkface2):
                items = filename.split('_')
                line_count += 1
                if (items[1] == "0"):  # in UTKFace 0 è uomo
                    new_file_name = '%06d_1.jpg' % (line_count - 1,)
                else:
                    new_file_name = '%06d_0.jpg' % (line_count - 1,)
                shutil.copy(os.path.join(path_images_utkface2, filename), os.path.join(dest_path, new_file_name))
                name_writer.writerow([filename, new_file_name])
    # Parte di UTKFace vedere cosa scegliere attento al nome dei file


#Fa solo merging di UTK FACE
def merge_utk_only(path_images_utkface2,dest_path_oldnew_csv,dest_path):
    with open(os.path.join(dest_path_oldnew_csv, "oldname_newname.csv"), mode='w', newline="") as name_file:
        name_writer = csv.writer(name_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        line_count = 0

        if path_images_utkface2 is not None:
            for filename in os.listdir(path_images_utkface2):
                items = filename.split('_')
                line_count += 1
                if (items[1] == "0"):  # in UTKFace 0 è uomo
                    new_file_name = '%06d_1.jpg' % (line_count - 1,)
                else:
                    new_file_name = '%06d_0.jpg' % (line_count - 1,)
                shutil.copy(os.path.join(path_images_utkface2, filename), os.path.join(dest_path, new_file_name))
                name_writer.writerow([filename, new_file_name])

def extract_male(path_male_female_csv,dest):
    male_female= loadtxt(path_male_female_csv,delimiter=',')
    print(type(male_female))
    #print(male_female)
    print(male_female.shape)
    x_new = male_female[male_female[:,0]==1.]#Male
    savetxt(dest,x_new,fmt='%i',delimiter=',')

def extract_female(path_male_female_csv,dest):
    male_female= loadtxt(path_male_female_csv,delimiter=',')
    print(type(male_female))
    #print(male_female)
    print(male_female.shape)
    x_new = male_female[male_female[:,0]==0.]#Female
    savetxt(dest,x_new,fmt='%i',delimiter=',')

def balance_datasets_random_50_50(path_male,path_female,path_dest):
    male = loadtxt(path_male, delimiter=',')
    female = loadtxt(path_female, delimiter=',')
    n_row_m = np.shape(male)[0]
    n_row_f = np.shape(female)[0]

    if n_row_f > n_row_m:
        idx = random.sample(range(n_row_f), n_row_m)
        female = female[idx, :]
    else:
        idx = random.sample(range(n_row_m), n_row_f)
        male = male[idx, :]
    n_row_m = np.shape(male)[0]
    n_row_f = np.shape(female)[0]
    print(n_row_m)
    print(n_row_f)
    total = np.vstack((female, male))
    print(np.shape(total))
    savetxt(path_dest, total, fmt='%i', delimiter=',')

