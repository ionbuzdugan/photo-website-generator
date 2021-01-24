import json
import os

DIR = 'images/originals/'

def main():
    jsonList = {}
    jsonList=[]
    dirList =[]
    currentRef = json.load(open('photo_ref.json'))

    for tDir in currentRef:
        if tDir['name'] not in dirList:
            dirList.append(tDir['name'])
            dirList.append(tDir['date'])

    for r,d,f in os.walk(DIR):
        for dir in d:
            date = 'DATE'
            if dir in dirList:
                for i in range(0,len(dirList)):
                    if dirList[i] == dir:
                        date = dirList[i+1]
            else:
                while True:
                    date = input("Enter the date for " + dir + ": ")
                    dirList.append(dir)
                    dirList.append(date)
                    if input('Correct date? ')=="y" or input('Correct date? ')=="Y" :
                        break
            folder={}
            folder['name'] = dir
            folder['text'] = dir.replace("_"," ").title()
            folder['date'] = date
            folder['link'] = "pages/" + dir + ".html"
            folder['photos']=[]
            for r1,d2,f2 in os.walk(os.path.join(DIR,str(dir))):
                for file in f2:
                    photo={}
                    photo['link-small']=str(os.path.join(DIR,dir,file)).replace("\\","/").replace('originals','smalls')
                    photo['link-original']=str(os.path.join(DIR,dir,file)).replace("\\","/")
                    folder['photos'].append(photo)
            jsonList.append(folder)
    with open('photo_ref.json','w') as f:
        json.dump(jsonList,f,indent=4)
