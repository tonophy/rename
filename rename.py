from PIL import Image
from PIL.ExifTags import TAGS
from pprint import pprint
import shutil
import os
import glob
import argparse

def get_exif(filename):
    """
    Extracts Exif metadata from a JPG image file.
    """
    with Image.open(filename) as image:
        exif = image._getexif()
        if exif is not None:
            exif_data = {}
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                exif_data[tag] = value
            return exif_data
        else:
            return None


def main(targetDir):

    outputDir = 'rename'
    if not os.path.isdir(os.path.join(targetDir,outputDir)):
        os.mkdir(os.path.join(targetDir,outputDir))

    extensions = [".jpg", ".JPG"]
    
    for extension in extensions:
        file_list = os.listdir(targetDir)
        file_list_jpg = [file for file in file_list if file.endswith(extension)]

        for file in file_list_jpg:
            src = os.path.join(targetDir,file)
            exif_data = get_exif(src)
            infoDate = exif_data['DateTime']
            outputFileName = infoDate.replace(':','').replace(' ','_')

            src = os.path.join(targetDir,file)
            dst = os.path.join(targetDir,outputDir,outputFileName+extension)
            if os.path.exists(dst):
                dst = dst.replace(extension,'(re)'+extension)
                print('(file exists) copying:', src, '>', dst)
            else:
                print('copying:', src, '>', dst)
            
            shutil.copy2(src,dst)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folderName")
    args = parser.parse_args()

    foloderName = args.folderName
    print('rename strat:', foloderName)
    main(foloderName)

