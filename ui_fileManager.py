import os
import re
import shutil

absFilePath = os.path.abspath(__file__)
#print(absFilePath)
fileDir = os.path.dirname(os.path.abspath(__file__))
#print(fileDir)
parentDir = os.path.dirname(fileDir)
#print(parentDir)


def clean_name(the_string):
    bad_char = r'[^a-z^A-Z^0-9.]'
    return re.sub(bad_char,'_',the_string)


def make_new_dir_path(root_path, new_dir):
    path = os.path.split(root_path)[0]
    out_path = os.path.join(path,new_dir)
    return os.path.abspath(out_path)


def del_directory(root_path, new_dir):
    d_path = os.path.join(root_path, new_dir)
    if os.path.exists(d_path):
        shutil.rmtree(d_path)
        print("Deleting", d_path)
    else:
        print("Does not exist")


def get_image_files(path):
    the_files = []
    the_file_names = []
    for the_file in os.listdir(path):
        file_path = os.path.join(path,the_file)
        file_good = re.search( r'(.*)\.jpg|\.jpeg]\.png', the_file, re.I)
        if (os.path.isfile(file_path)) and file_good:
            the_files.append(file_path)
            the_file_names.append(os.path.split(file_path)[1])

    return the_files, the_file_names


def transfer_files(image_dir, the_date, new_dir_name ):
    # Delete existing dir
    del_directory(image_dir, new_dir_name)
    # Create new files
    for root, dirs, files in os.walk(image_dir):
        file_index = 0
        for name in files:
            name.lower()
            file_ext = re.search( r'(.*)\.jpg|\.jpeg]\.png', name, re.I)
            in_new_dir = re.search( new_dir_name, root, re.I)
            if file_ext and not in_new_dir:
                base_path = os.path.join(root, name)
                s_path = os.path.abspath(base_path) # doublecheck
                # Clean name
                name = clean_name(name)
                # Format name
                name = "{}_{}__{}".format(file_index,the_date,name)
                file_index += 1

                # Make destination
                d_path = make_new_dir_path(s_path, new_dir_name)
                new_file_path = os.path.join(d_path, name)
                if os.path.isfile(new_file_path):
                    print("EXISTS: ", new_file_path)
                else:
                    print("CREATING:", new_file_path)
                    if not os.path.exists(d_path):
                        os.makedirs(d_path)
                    try:
                        pass
                        shutil.copyfile(s_path,new_file_path)
                    except shutil.SameFileError as e:
                        print(e)
            else:
                print("bad file format.. skipping:", name)
