import json
import sys
tagtransitioncount = {}
wordemissioncount = {}
statetransitionlist = []
taglist = []
alllinetags = []

def main():
    global tagtransitioncount
    global wordemissioncount
    global statetransitionlist
    global taglist

    with open("./docs/POSModel.txt","r") as modelfile:
        content = modelfile.readlines()
        taglist = [i for i in content[0].split()]
        tagtransitioncount = json.loads(content[1])
        wordemissioncount = json.loads(content[2])

        # print (tagtransitioncount)
    # tagsforalllines = []
    f = open("./docs/hmmoutput.txt", "w")
    with open("./docs/SharanyaTest.txt","r") as testdatafile:
        for line in testdatafile.readlines():
            wordsinline = line.split()
            numberofwordsinline = len(wordsinline)
            statetransitionlist = []
            for i in range(0,numberofwordsinline):
                #print wordsinline[i]
                tempdict = {}
                currentword = wordsinline[i]
                if currentword in wordemissioncount:
                    #print str(i)+"first if"
                    for tag in wordemissioncount[currentword]:
                        #prevtagwithmaxvalue = "--"
                        emisprob = wordemissioncount[currentword][tag]
                        maxvalue = float("-inf")
                        if i == 0:
                            #print str(i)+"second if"
                            transprob = tagtransitioncount["start"][tag]
                            tempdict[tag]=["start",transprob + emisprob]
                        else:
                            for tagofprevword in statetransitionlist[i-1]:
                                transprob = tagtransitioncount[tagofprevword][tag]
                                overallprob = transprob + emisprob + statetransitionlist[i-1][tagofprevword][1]
                                if maxvalue < overallprob:
                                    maxvalue = overallprob
                                    prevtagwithmaxvalue = tagofprevword
                            #print "tag = "+tag +"prevtagwithmaxvalue" + prevtagwithmaxvalue +"overal prob" +str(overallprob)
                            tempdict[tag] = [prevtagwithmaxvalue, overallprob]
                    statetransitionlist.insert(i,tempdict)
                else:
                    if(currentword[0].isupper()):
                        maxvalue = float("-inf")
                        if i == 0:
                            transprob = tagtransitioncount["start"]["NP"]
                            tempdict["NP"] = ["start", transprob]
                        else:
                            for tagofprevword in statetransitionlist[i - 1].keys():
                                transprob = tagtransitioncount[tagofprevword]["NP"]
                                overallprob = transprob + statetransitionlist[i - 1][tagofprevword][1]
                                if maxvalue < overallprob:
                                    maxvalue = overallprob
                                    prevtagwithmaxvalue = tagofprevword
                            tempdict["NP"] = [prevtagwithmaxvalue, overallprob]

                    elif hasNumbers(currentword):
                        maxvalue = float("-inf")
                        if i == 0:
                            transprob = tagtransitioncount["start"]["ZZ"]
                            tempdict["ZZ"] = ["start", transprob]
                        else:
                            for tagofprevword in statetransitionlist[i - 1].keys():
                                transprob = tagtransitioncount[tagofprevword]["ZZ"]
                                overallprob = transprob + statetransitionlist[i - 1][tagofprevword][1]
                                if maxvalue < overallprob:
                                    maxvalue = overallprob
                                    prevtagwithmaxvalue = tagofprevword
                            tempdict["ZZ"] = [prevtagwithmaxvalue, overallprob]
                    else:
                        for tag in taglist:
                            maxvalue = float("-inf")
                            #prevtagwithmaxvalue = "--"
                            if i == 0:
                                transprob = tagtransitioncount["start"][tag]
                                tempdict[tag] = ["start", transprob]
                            else:
                                for tagofprevword in statetransitionlist[i - 1].keys():
                                    transprob = tagtransitioncount[tagofprevword][tag]
                                    overallprob = transprob + statetransitionlist[i - 1][tagofprevword][1]
                                    if maxvalue < overallprob:
                                        maxvalue = overallprob
                                        prevtagwithmaxvalue = tagofprevword
                                tempdict[tag] = [prevtagwithmaxvalue, overallprob]
                    #print tempdict
                    statetransitionlist.insert(i, tempdict)




            maxvalue1 = float("-inf")
            tagoflastwordinline=""
            counter1 = numberofwordsinline - 1
            for key in statetransitionlist[counter1]:
                if maxvalue1 < statetransitionlist[counter1][key][1]:
                    maxvalue1 = statetransitionlist[counter1][key][1]
                    tagoflastwordinline = key
                    tagoflastbutoneword = statetransitionlist[counter1][key][0]
                    #print tagoflastbutoneword
                    #print counter1

            tagsofaline = []
            counter2 = 2
            tagsofaline = [tagoflastwordinline]
            tempprevtag = tagoflastbutoneword
            tagsofaline = [tagoflastbutoneword] + tagsofaline
            while numberofwordsinline-counter2 >= 0:
                tempprevtag = statetransitionlist[numberofwordsinline-counter2][tempprevtag][0]
                counter2 = counter2 + 1
                tagsofaline = [tempprevtag] + tagsofaline
            temp = zip(wordsinline,tagsofaline[1:])
            # import pdb; pdb.set_trace()
            for t in temp:
                # print t[0]
                f.write(t[0])
                f.write('/')
                f.write(t[1])
                f.write(' ')
            f.write('\n')
        f.close()


def hasNumbers(inputString):
   return any(char.isdigit() for char in inputString)

main()