from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Frame, Button,Style
from PIL import Image,ImageTk
import os, time
import logic, outputHTML, getFrame, webbrowser
script_dir=os.path.dirname(__file__)

windowWidth=1200
windowHeight=700
panelWidth=200
panelHeight=400
buttonSize=30
srtIsLoaded=False
mp4IsLoaded=False
executed=False
srtPath=""
mp4Path=""
title=""

def go():
    global srtPath, mp4Path, executed, title, app
    executed=True
    print("eggecute!")

    logic.integrate(srtPath)
    app.statusText.set("srt file analyzed")
    app.statusLabel.update()

    num=logic.arrange()
    app.statusText.set("srt file parsed into sentences")
    app.statusLabel.update()


    logic.summarize(summaryRatio=9, fileName="fancy")
    logic.summarize(summaryRatio=3, fileName="summary1")
    logic.summarize(summaryRatio=7, fileName="summary2")
    logic.summarize(summaryRatio=10, fileName="summary3")
    app.statusText.set("summary created")
    app.statusLabel.update()

    getFrame.getFrame(mp4Path,"fancy")
    getFrame.getFrame(mp4Path,"summary1")
    getFrame.getFrame(mp4Path,"summary2")
    getFrame.getFrame(mp4Path,"summary3")
    app.statusText.set("images loaded")
    app.statusLabel.update()


    fancy_HTML_Path=outputHTML.outputHTML("fancy", title)
    sum1_HTML_Path=outputHTML.outputHTML("summary1", title)
    sum2_HTML_Path=outputHTML.outputHTML("summary2", title)
    sum3_HTML_Path=outputHTML.outputHTML("summary3", title)

    app.statusText.set("generating fancy summary......")
    app.statusLabel.update()
    logic.html2image(htmlPath=fancy_HTML_Path, type="fancy")
    app.statusText.set("generating 33 %% summary......")
    app.statusLabel.update()
    logic.html2image(htmlPath=sum1_HTML_Path, type="summary1")
    app.statusText.set("generating 66 %% summary......")
    app.statusLabel.update()
    logic.html2image(htmlPath=sum2_HTML_Path, type="summary2")
    app.statusText.set("generating 100 %% summary......")
    app.statusLabel.update()
    logic.html2image(htmlPath=sum3_HTML_Path, type="summary3")
    app.statusText.set("finished!")
    app.statusLabel.update()
    time.sleep(0.5)
    app.statusText.set("")
    app.statusLabel.update()
    app.selectButton.place_forget()
    app.selectButton.update()

def search(searchword):
    global mp4Path
    app.statusText.set("searching for "+searchword+"......")
    app.statusLabel.update()
    logic.search(searchword)
    getFrame.getFrame(mp4Path, "search")
    path=outputHTML.outputHTML("search", title)
    logic.html2image(htmlPath=path, type="search")
    app.statusText.set("")
    app.statusLabel.update()


def chooseFile():
    global srtIsLoaded, mp4IsLoaded, srtPath, mp4Path, title
    if (not srtIsLoaded) or (not mp4IsLoaded):
        path=filedialog.askopenfilename()
    if path[-3:]=="srt":
        srtIsLoaded=True
        srtPath=path
        base=os.path.basename(srtPath)
        title=os.path.splitext(base)[0]
        mp4Path=os.path.join(os.path.dirname(srtPath),(title+".mp4"))
        if os.path.isfile(mp4Path):
            mp4IsLoaded=True
    if path[-3:]=="mp4":
        mp4IsLoaded=True
        mp4Path=path
        base=os.path.basename(mp4Path)
        title=os.path.splitext(base)[0]
        srtPath=os.path.join(os.path.dirname(mp4Path),(title+".srt"))
        if os.path.isfile(srtPath):
            srtIsLoaded=True
class FrameWindow:
    def __init__(self, parent):
        global panelWidth, panelHeight, windowHeight, windowWidth, buttonSize
        frame=Frame(parent)
        frame.pack(fill=BOTH, expand=1)
        frame.style=Style()
        frame.style.theme_use("default")

        #I should place contentFrame before panelFrame, since panelFrame comes on top?
        contentFrame=Frame(frame, width=windowWidth, height=windowHeight)
        contentFrame.place(x=0, y=0)

        panelFrame=Frame(frame, width=panelWidth, height=panelHeight, relief=RIDGE, borderwidth=1)
        panelFrame.place(x=20,y=windowHeight-panelHeight-20)

#######################panel frame#######################
        self.compassSize=panelWidth-50
        self.compassImage=Image.open(os.path.join(script_dir,"resource/compass.gif"))
        self.compassImage=self.compassImage.resize((self.compassSize, self.compassSize), Image.ANTIALIAS)
        image1=self.compassImage.rotate(0)
        image2=ImageTk.PhotoImage(image1)
        self.compass=Label(panelFrame)
        self.rotateCompass(0)

        #button for first summary
        image1=Image.open(os.path.join(script_dir,"resource/1.png"))
        image1=image1.resize((buttonSize, buttonSize), Image.ANTIALIAS)
        image2=ImageTk.PhotoImage(image1)
#I want to remove the button border...
        self.button1=Button(panelFrame, image=image2, command=lambda: self._chooseCompass(1))
        self.button1.image=image2
        self.button1.place(x=25,y=panelHeight-self.compassSize-50)

        #button for second summary
        image1=Image.open(os.path.join(script_dir,"resource/2.png"))
        image1=image1.resize((buttonSize, buttonSize), Image.ANTIALIAS)
        image2=ImageTk.PhotoImage(image1)
        self.button2=Button(panelFrame, image=image2, command=lambda: self._chooseCompass(2))
        self.button2.image=image2
        self.button2.place(x=25+self.compassSize-buttonSize,y=panelHeight-self.compassSize-50 )

        image1=Image.open(os.path.join(script_dir,"resource/4.png"))
        image1=image1.resize((buttonSize, buttonSize), Image.ANTIALIAS)
        image2=ImageTk.PhotoImage(image1)
        self.button4=Button(panelFrame, image=image2, command=lambda: self._chooseCompass(4))
        self.button4.image=image2
        self.button4.place(x=25,y=panelHeight-50-buttonSize )

        image1=Image.open(os.path.join(script_dir,"resource/3.png"))
        image1=image1.resize((buttonSize, buttonSize), Image.ANTIALIAS)
        image2=ImageTk.PhotoImage(image1)
        self.button3=Button(panelFrame, image=image2, command=lambda: self._chooseCompass(3))
        self.button3.image=image2
        self.button3.place(x=25+self.compassSize-buttonSize,y=panelHeight-50-buttonSize )

        #label for title
        #might be better to use Text()
        self.titleText=StringVar()
        titleLabel=Label(panelFrame, textvariable=self.titleText, wraplength=panelWidth-10, anchor=CENTER, font=("Helvetica", "20"))
        self.titleText.set(" ")
        titleLabel.place(x=5, y=20)

        #search bar
        searchFrame=Frame(panelFrame)
        searchFrame.place(x=5, y=100)
        self.searchBar=Entry(searchFrame, width=17)
        self.searchBar.pack(side=LEFT)
        image1=Image.open(os.path.join(script_dir,"resource/search.gif"))
        image1=image1.resize((20, 20), Image.ANTIALIAS)
        image2=ImageTk.PhotoImage(image1)
        searchButton=Button(searchFrame, image=image2, command=self._search)
        searchButton.image=image2
        searchButton.pack(side=LEFT)

        #reset Button
        reset=Button(panelFrame, text="new", command=self.reset)
        reset.place(x=0, y=panelHeight-30)

        #reset Button
        share=Button(panelFrame, text="share", command=self.share)
        share.place(x=int(panelWidth/2), y=panelHeight-30)

#######################content frame#######################

        image1=Image.open(os.path.join(script_dir,"resource/back.png"))
        image1=image1.resize((windowWidth,windowHeight), Image.ANTIALIAS)
        image2=ImageTk.PhotoImage(image1)
        bgImage=Label(contentFrame,image=image2)
        bgImage.place(x=0,y=0)
        bgImage.image=image2

        self.contentImage=Label(contentFrame)

        self.statusText=StringVar()
        self.statusLabel=Label(contentFrame, textvariable=self.statusText, anchor=CENTER, font=("Helvetica", "30"))
        self.statusText.set("select video and subtitle")
        self.statusLabel.place(x=panelWidth+50, y=50)

        image1=Image.open(os.path.join(script_dir,"resource/import.gif"))
        image1=image1.resize((200,200), Image.ANTIALIAS)
        self.importImage=ImageTk.PhotoImage(image1)
        image1=Image.open(os.path.join(script_dir,"resource/check.gif"))
        image1=image1.resize((200,200), Image.ANTIALIAS)
        self.checkImage=ImageTk.PhotoImage(image1)

        self.selectButton=Button(contentFrame, command=chooseFile)
        self.selectButton.place(x=20, y=20)

    def rotateCompass(self, rotation):
        self.compass.place_forget()
        image1=self.compassImage.rotate(rotation)
        image2=ImageTk.PhotoImage(image1)
        self.compass.configure(image=image2)
        self.compass.image=image2
        self.compass.place(x=25,y=panelHeight-self.compassSize-50)
        self.compass.update()
    def updateUI(self):
        global srtIsLoaded, mp4IsLoaded, executed, title
        if not executed:
            self.contentImage.place_forget()
            self.titleText.set("")
        if executed:
            self.titleText.set(title)
        if (not srtIsLoaded) or (not mp4IsLoaded):
            self.selectButton.configure(image=self.importImage)
            self.selectButton.image=self.importImage
            self.selectButton.place(x=20, y=20)
            self.selectButton.update()
        elif srtIsLoaded and mp4IsLoaded and (not executed):
            self.selectButton.configure(image=self.checkImage)
            self.selectButton.image=self.checkImage
            self.selectButton.place(x=20, y=20)
            self.selectButton.update()
            self.statusText.set("Files loaded!")
            self.statusLabel.update()
            time.sleep(0.5)
            go()
        else:
            pass

    def _chooseCompass(self, choice):
        self.type=""
        if choice==1:
            self.rotateCompass(40)
            self.type="summary1"
        elif choice==2:
            self.rotateCompass(-40)
            self.type="summary2"
        elif choice==3:
            self.rotateCompass(-140)
            self.type="summary3"
        elif choice==4:
            self.rotateCompass(140)
            self.type="fancy"
        self.setPhoto(self.type)
    def _search(self):
        if executed:
            searchword=self.searchBar.get()
            search(searchword)
            self.setPhoto("search")
    def setPhoto(self, type):
        global windowWidth, panelWidth
        image1=Image.open(os.path.join(script_dir,"img/"+type+"-full.png"))
        w,h=image1.size
        W=windowWidth-panelWidth-20
        H=int(W*h/w)
        image1=image1.resize((W,H), Image.ANTIALIAS)
        image2=ImageTk.PhotoImage(image1)
        self.contentImage.configure(image=image2)
        self.contentImage.image=image2
        self.contentImage.place_forget()
        self.contentImage.place(x=panelWidth-10,y=10)
    def reset(self):
        global srtIsLoaded, mp4IsLoaded, executed
        srtIsLoaded=False
        mp4IsLoaded=False
        executed=False
    def share(self):
        global script_dir
        if self.type=="search" or self.type=="summary3" or self.type=="summary2" or self.type=="summary1" or self.type=="fancy":
            webbrowser.open("file://"+os.path.join(script_dir, "img", (self.type+"-full.png")))


root=Tk()
root.geometry(str(windowWidth)+"x"+str(windowHeight)+"+0+0")
app=FrameWindow(root)
def update():
    global count
    app.updateUI()
    root.after(500, update)
update()
root.mainloop()
