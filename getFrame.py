import os, cv2
script_dir=os.path.dirname(__file__)

#analyze string, extract time(in milliseconds) & sentence
#returns false if no time info found
def extractTime(line):
    if line[0]!="(":
        print("no time info")
        return False,"0"
    millis=int(line[line.find("(")+1:line.find(")")])
    sentence=line[14:]
    print("time info found")
    return millis, sentence

#reads txt file and gets snapshots for each sentence.
#output format is
#([milliseconds])[sentence]
#images are saved from name_0.png~
#sentences with no time info are ignored
def getFrame(videoPath, name):
    read_file=open(os.path.join(script_dir,(name+".txt")))
    videoObject=cv2.VideoCapture(videoPath)
    if not videoObject.isOpened():
        print("error! cannot open video file")
        return
    index=0
    for line in read_file:
        millis, sentence=extractTime(line)
        if millis==0:
            continue
        videoObject.set(0,millis)
        ret, image=videoObject.read()
        filename="img/"+name+"_"+str(index)+".png"
        cv2.imwrite(os.path.join(script_dir,filename),image)
        index+=1


    read_file.close()
    videoObject.release()


# getFrame("/Users/yasunori/GoogleDrive/hack day 2017/Hackday 共有/videos/Alien Ocean NASA’s Mission to Europa-HD.mp4", "summary1")
