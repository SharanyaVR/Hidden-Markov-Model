import json
import math

wordemissioncount = {}
tagtransitioncount = {}
taglist = []
totalemissioncount = {}

def main():
    with open("./docs/catalan_corpus_train_tagged.txt","r") as traindata:
        for line in traindata.readlines():
            wordsinline = line.split()
            numberofwords = len(wordsinline)
            if(numberofwords == 0):
                continue
            addTransitionCount("start", wordsinline[0].rsplit('/', 1)[1])
            for i in range(0, numberofwords):
                wordplustag = wordsinline[i]
                wordandtag = wordplustag.rsplit('/', 1)

                word = wordandtag[0]
                tag = wordandtag[1]

                #adding unique tags to the list
                if tag not in taglist:
                    taglist.append(tag)

                #creating wordemission count dict
                if word in wordemissioncount:
                    if tag in wordemissioncount[word]:
                        wordemissioncount[word][tag] += 1
                    else:
                        wordemissioncount[word][tag] = 1
                else:
                    wordemissioncount[word] = {}
                    wordemissioncount[word][tag] = 1

                if tag in totalemissioncount:
                    totalemissioncount[tag] += 1
                else:
                    totalemissioncount[tag] = 1

                #finding tag and nextag for transition probabilities
                if(i+1 == numberofwords):
                    continue;
                nexttag = wordsinline[i+1].rsplit("/", 1)[1]
                addTransitionCount(tag, nexttag)

        # print tagtransitioncount
        # print wordemissioncount
        # print taglist
        # print len(taglist)
        #wordemissioncount[word][tag] = 1
        # finding emissioncount for each tag

        # print len(wordemissioncount)
        # print len(tagtransitioncount)
        #createmodel
        createPOSModel()
        # print tagtransitioncount
        # print wordemissioncount

def createPOSModel():
    # print "length of first level"
    #calculate probabilities for tagtransitions
    for tag in tagtransitioncount:
        for nexttag in tagtransitioncount[tag]:
            if nexttag != "count":
                tagtransitioncount[tag][nexttag] = math.log(float(tagtransitioncount[tag][nexttag]+1)) - math.log(float(tagtransitioncount[tag]["count"]+len(taglist)))
        for uniquetag in taglist:
            if uniquetag not in tagtransitioncount[tag]:
                tagtransitioncount[tag][uniquetag] = math.log(float(1)) - math.log(float(tagtransitioncount[tag]["count"]+len(taglist)))
    #calculate probabilities for emission
    for word in wordemissioncount:
        for tag in wordemissioncount[word]:
            wordemissioncount[word][tag] = math.log(float(wordemissioncount[word][tag])) - math.log(float(totalemissioncount[tag]))


    with open("docs/POSModel.txt", "w") as modelfile:
        for i in taglist:
            modelfile.write(i+" ")
        modelfile.write("\n")
        json.dump(tagtransitioncount, modelfile)
        modelfile.write("\n")
        json.dump(wordemissioncount, modelfile)
        modelfile.write("\n")

def addTransitionCount(tag, nexttag):
    if tag in tagtransitioncount:
        if nexttag in tagtransitioncount[tag]:
            tagtransitioncount[tag][nexttag] += 1
        else:
            tagtransitioncount[tag][nexttag] = {}
            tagtransitioncount[tag][nexttag] = 1
    else:
        tagtransitioncount[tag] = {}
        tagtransitioncount[tag][nexttag] = 1

    if 'count' in tagtransitioncount[tag].keys():

        tagtransitioncount[tag]['count'] += 1
    else:
        tagtransitioncount[tag]["count"] = 1

main()







