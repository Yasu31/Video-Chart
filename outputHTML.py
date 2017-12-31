import os
script_dir=os.path.dirname(__file__)

#I'm a *bit* unconfortable with handing the whole template info each time I call findTags, but TO THE HELL WITH PROPER MEMORY MANAGEMENT!
def findTags(beginTag, endTag, template):
    beginTag="<!--"+str(beginTag)+"-->"
    endTag="<!--"+str(endTag)+"-->"
    beginPosition=template.find(beginTag)
    print("beginning tag "+beginTag+"found at "+str(beginPosition))
    endPosition=template.find(endTag)
    print("end tag "+endTag+"found at "+str(endPosition))
    return template[beginPosition+len(beginTag):endPosition]

def outputHTML(name, title):
    fileName=name
    if name[:7]=="summary" or name=="search":
        fileName="simple"
    else:
        if not name=="fancy":
            print("file name error!")
            return
    templateFile=open(os.path.join(script_dir,("template_"+fileName+".html")))
    dataFile=open(os.path.join(script_dir,(name+".txt")))
    outputFilePath=os.path.join(script_dir,(name+".html"))
    outputFile=open(outputFilePath,"w")
    templateText=""
    for line in templateFile:
        templateText+=line
    templateFile.close()
    if name=="fancy":
        #code for fancy template
        outputFile.write(findTags(0,4,templateText))
        outputFile.write(title)
        outputFile.write(findTags(4,5,templateText))
        outputFile.write(dataFile.readline())
        outputFile.write(findTags(5,6,templateText))
        outputFile.write(dataFile.readline())
        outputFile.write(findTags(6,7,templateText))
        outputFile.write(dataFile.readline())
        outputFile.write(findTags(7,8,templateText))
        outputFile.write(dataFile.readline())
        outputFile.write(findTags(8,9,templateText))
        outputFile.write(dataFile.readline())
        outputFile.write(findTags(9,10,templateText))
        outputFile.write(dataFile.readline())
        outputFile.write(findTags(10,11,templateText))
    else:
        #for simple formats
        outputFile.write(findTags(0,1,templateText))
        outputFile.write(title)
        outputFile.write(findTags(1.3,2,templateText))
        outputFile.write(title)
        outputFile.write(findTags(2.5,3,templateText))
        image1=findTags(3,4,templateText)
        image2=findTags(5,6,templateText)
        image3=findTags(7,8,templateText)
        index=0
        for line in dataFile:
            outputFile.write(image1)
            outputFile.write('<img src="img/'+name+"_"+str(index)+'.png">')
            outputFile.write(image2)
            outputFile.write(line)
            outputFile.write(image3)
            index+=1
        outputFile.write(findTags(9,10,templateText))
    outputFile.close()
    return outputFilePath

# outputHTML("summary1")
