# from __future__ import absolute_import
# from __future__ import division, print_function, unicode_literals

import os, subprocess

from nltk.tokenize import sent_tokenize

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

script_dir = os.path.dirname(__file__)
beginMarker="AA"
endMarker="BB"

##integrate(1).py###############################
def extractTime(line):
    millis=int(line[3:5])*60*1000+int(line[6:8])*1000+int(line[9:12])
    print("time info found")
    return millis
def addsecond(subtitle, timeCode):
    global beginMarker, endMarker
    start = timeCode[0:12]
    end = timeCode[17:29]
    start = str(extractTime(start))
    end = str(extractTime(end))
    return beginMarker+start+endMarker+subtitle+beginMarker+end+endMarker

def integrate(subtitlePath):
    global script_dir
    subtitleTxt = open(subtitlePath)
    outputTxt = open(os.path.join(script_dir,"txt1.txt"),"w")
    lineNumber = 0
    for line in subtitleTxt:
        lineNumber+=1
        print(line)
        if lineNumber > 200:
              break
        line = line.replace('\n',' ')
        if True:

            timecode = subtitleTxt.readline()
            timecode = timecode.replace('\n',' ')
            subtitle = ""
            for line in subtitleTxt:
                if line == '\n':
                    break
                subtitle +=line
                subtitle = subtitle.replace('\n',' ')
            string = addsecond(subtitle,timecode)
            string = string.replace('\n',' ')
            outputTxt.write(string)
    subtitleTxt.close()
    outputTxt.close()

#arrange.py###############################
def arrange():
    global script_dir, beginMarker, endMarker
    subtitleTxt = open(os.path.join(script_dir,"txt1.txt"))
    outputTxt = open(os.path.join(script_dir,"txt2.txt"),"w")
    sent = sent_tokenize(subtitleTxt.readline())
    sentenceNum=0
    for seent in sent:
        newseent = ""
        searchhead = 0

        a = seent.find(beginMarker,searchhead)
        if a == -1:
            #if there is not time information for that sentence, it is IGNORED.
            print("no time info found")
            continue
        sentenceNum+=1
        b = seent.find(endMarker,searchhead)

        time = seent[a+len(beginMarker):b]
        newseent = newseent+seent[searchhead:a]

        while True:
            a = seent.find(beginMarker,searchhead)
            if a == -1:
                break
            b = seent.find(endMarker,searchhead)
            newseent = newseent+seent[searchhead:a]
            searchhead = b+len(endMarker)

        newseent = newseent + seent[searchhead:]
        newseent = "("+time+")" + newseent

        outputTxt.write(newseent+"\n")
        print("written")

    subtitleTxt.close()
    outputTxt.close()
    return sentenceNum

##summarize.py##################################
#input ratio of summarized sentences and the name of the output file(probably summary1 or summary2)
def summarize(summaryRatio=5, fileName="summary1"):
    global script_dir
    subtitleTxt=open(os.path.join(script_dir,"txt2.txt"))
    outputTxt = open(os.path.join(script_dir,(fileName+".txt")),"w")

    LANGUAGE = "english"
    SENTENCES_COUNT = summaryRatio
    parser = PlaintextParser.from_file(os.path.join(script_dir, "txt2.txt"), Tokenizer(LANGUAGE))

    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    for sentence in summarizer(parser.document, SENTENCES_COUNT):
      outputTxt.write(str(sentence)+"\n")

    subtitleTxt.close()
    outputTxt.close()

###search.py##################################
def search(searchword="life"):
    global script_dir
    subtitleTxt = open(os.path.join(script_dir,"txt2.txt"))
    outputTxt = open(os.path.join(script_dir,"search.txt"),"w")
    for line in subtitleTxt:
        x = line.find(searchword)
        if x == -1:
            continue
        else:
            outputTxt.write(line)
    subtitleTxt.close()
    outputTxt.close()

###html2image.py##################################
#outputs as img/search-thumb.png
def html2image(htmlPath="/Users/yasunori/summary.html", type="search"):
    global script_dir
    subprocess.run(["webkit2png","-F", "-D", os.path.join(script_dir,"img"),"-o",type, htmlPath])

# integrate("/Users/yasunori/GoogleDrive/hack day 2017/Hackday 共有/videos/Alien Ocean- NASA’s Mission to Europa.srt")
# arrange()
# summarize(summaryRatio=5, fileName="hello")
# summarize(summaryRatio=100, fileName="hi_again")
# summarize(summaryRatio=1, fileName="hi")
# search("water")
# html2image()
