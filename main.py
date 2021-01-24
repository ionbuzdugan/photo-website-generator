# ONLY WORKS ON JPG

import os
import datetime
from PIL import Image
import shutil

DIR = './site/photos/'
DIR_SOURCE = './PLACE_PHOTOS_HERE/'
DIR_ORIGINALS = './site/photos/originals/'
DIR_THUMBS = './site/photos/thumbs/'
IMAGE_MAX = 500
PAGE_TEMPLATE = open('./templates/index_template.txt')
DIR_INDEX = './site/index.html'

# Reset names of photos in dir
def reset_names (dir,photosList):
    for i in range(0,len(photosList)):
        os.rename(dir + str(photosList[i]), dir + str(i) + '.jpg')

# Resize and save photo contained in pPath argument
def smallify_photo(path_orignal, path_thumb):
    img = Image.open(path_orignal)
    oWidth, oHeight = img.size

    # Make minimum dimension IMAGE_MAX
    if oHeight/oWidth > 1:
        scaleFactor = IMAGE_MAX/oWidth
    else:
        scaleFactor = IMAGE_MAX/oHeight
    nHeight = int(oHeight*scaleFactor)
    nWidth = int(oWidth*scaleFactor)
    img = img.resize((nWidth,nHeight), Image.ANTIALIAS)

    cropHorizontal = (nWidth-IMAGE_MAX)/2
    cropVertical = (nHeight-IMAGE_MAX)/2
    img = img.crop((cropHorizontal,cropVertical,cropHorizontal+IMAGE_MAX,cropVertical+IMAGE_MAX))
    img.save(path_thumb)

if __name__ == "__main__":
    photosList = os.listdir(DIR_SOURCE)
    shutil.rmtree(DIR_ORIGINALS)
    shutil.rmtree(DIR_THUMBS)
    os.makedirs(DIR_ORIGINALS)
    os.makedirs(DIR_THUMBS)

    date = datetime.datetime.now()
    MONTH = date.month
    DAY = date.day
    YEAR = date.year
    NAME_SUFFIX = str(MONTH) + '_' + str(DAY) + '_' + str(YEAR)

    # Step through and process each photo
    names = []
    paths_originals = []
    paths_thumbs = []
    # reset_names(DIR_ORIGINALS,photosList)
    photosList = os.listdir(DIR_SOURCE)
    for i in range(0,len(photosList)):
        # Rename to No-NUMBER-MONTH_DAY_YEAR
        names.append(str('No-' + str(i+1) + '-' + NAME_SUFFIX +'.jpg'))
        paths_originals.append(str(DIR_ORIGINALS + str(names[i])))
        paths_thumbs.append(str(DIR_THUMBS +str(names[i])))
        shutil.copy(DIR_SOURCE + str(photosList[i]),paths_originals[i])
        # Resize and save in thumbs
        smallify_photo(str(paths_originals[i]),str(paths_thumbs[i]))
        print(names[i])
    # Add links to build index.html
    with open(DIR_INDEX,'w') as fOut:
        fOut.truncate(0)
        for line in PAGE_TEMPLATE:
            if 'END IMAGES HERE' in line:
                fOut.write('\t\t<div class=row>\n')
                for i in range(0,len(names)):
                    if i>0 and i%3 ==0:
                        fOut.write('\t\t</div>\n')
                        fOut.write('\t\t<div class=row>\n')
                    print (paths_originals[i])
                    s='\t\t\t<a class=\"four columns\" href=' + str(paths_originals[i]).replace('site/','') + ' target=_blank><img src=' + str(paths_thumbs[i]).replace('site/','') + '></a>\n'
                    fOut.write(s)
                fOut.write('\t\t</div>\n')
            fOut.write(line)