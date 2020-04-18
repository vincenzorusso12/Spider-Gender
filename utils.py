import os,shutil,csv
from zipfile import ZipFile

def makedir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def unzip(zip,dest):
    with ZipFile(zip, 'r') as zipObj:
        if len(os.listdir(dest)) == 0:
            zipObj.extractall(dest)


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


def create_once(dir):
    created = False
    if not os.path.exists(dir) and not created:
        os.makedirs(dir)
        created = True

