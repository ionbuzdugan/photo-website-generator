import shutil
import os
from PIL import Image
from bs4 import BeautifulSoup, NavigableString
import json
from create_ref_json import main as create_ref_json
import time

IMAGE_MAX = 500
ORIGINAL_FOLDER = 'images/originals/'
SMALL_FOLDER = 'images/smalls/'
PAGES_FOLDER = 'pages/'
INDEX_TEMPLATE = open('templates/index_template.txt')
PAGE_TEMPLATE = open('templates/page_template.txt')

# Copy source folder into images/ directory
def reset_library(symlinks=False, ignore=None):
    # Delete all files in destination
    if os.path.isdir(PAGES_FOLDER):
        shutil.rmtree(PAGES_FOLDER)
    os.mkdir(PAGES_FOLDER)
    print ('Reset PAGES', flush=True)
    if os.path.isdir(SMALL_FOLDER):
        shutil.rmtree(SMALL_FOLDER)
    os.mkdir(SMALL_FOLDER)
    print ('Reset SMALLS', flush=True)

    # Copy all files and folders into smalls folder
    for item in os.listdir(ORIGINAL_FOLDER):
        s = os.path.join(ORIGINAL_FOLDER, item)
        d = os.path.join(SMALL_FOLDER, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
    print ('Photos COPIED', flush=True)

# Resize and saved photo passed contained din pPath argument
def smallify_photo(pPath):
    img = Image.open(pPath)
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
    img.save(pPath)

# Walk through photo directory and resize photos
def convert_photos():
    for r,d,f in os.walk(SMALL_FOLDER):
        for file in f:
            fullPath= os.path.join(r,file)
            if 'png' in fullPath or 'jpg' in fullPath or 'jpeg' in fullPath:
                smallify_photo(fullPath)

# Add photo page link to index.html 
def add_links_to_index():
    with open("index.html","w") as fIndex:
        for line in INDEX_TEMPLATE:
            if 'END LINKS HERE' in line:
                fIndex.write('\t<p>\n')
                i=0
                for page in PHOTO_LIB:
                    if i==0:
                        s = '\t\t<a href='+page['link']+'>'+page['text']+' | '+page['date']+'</a>\n'
                    else:
                        s = '\t\t<br><a href='+page['link']+'>'+page['text']+' | '+page['date']+'</a>\n'
                    fIndex.write(s)
                    i+=1
                fIndex.write('\t</p>\n')
            fIndex.write(line)

# Add photo page link to index.html 
def add_gallery_pages():
    for page in PHOTO_LIB:
        print ('Creating ',page['name'], ' page', flush=True)
        with open(page['link'],"w") as gOut:
            PAGE_TEMPLATE = open('templates/page_template.txt')
            for line in PAGE_TEMPLATE:
                if 'END IMAGES HERE' in line:
                    photos=page['photos']
                    gOut.write('\t\t<div class=row>\n')
                    i=0
                    for photo in photos:
                        if i>0 and i%3 ==0:
                            gOut.write('\t\t</div>\n')
                            gOut.write('\t\t<div class=row>\n')
                        s='\t\t\t<a class=\"four columns\" href=../'+photo['link-original']+' target=_blank><img src=../'+photo['link-small']+'></a>\n'
                        gOut.write(s)
                        i+=1
                    gOut.write('\t\t</div>\n')
                elif 'HEADER HERE' in line:
                    s="\t\t\t\t\t\t<h3><font color=white>"+page['text']+"</font> | <font color=white>"+page['date']+'</font></h3>\n'
                    gOut.write(s)

                elif 'TITLE HERE' in line:
                    s='<title>Ion Buzdugan - '+page['text']+'</title>\n'
                    gOut.write(s)
                gOut.write(line)
        


if __name__ == "__main__":
    create_ref_json()
    PHOTO_LIB = json.load(open('photo_ref.json'))
    reset_library()
    convert_photos()
    add_links_to_index()
    add_gallery_pages()