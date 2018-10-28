import json
import os
import linecache


'''
Simplify data for each tweet, which only take the useful data

To use:
o0Simplify(one tweet data)
'''
def o0Simplify(item):
    info = dict()
    info["tweet_id"] = item["doc"]["id_str"]
    info["user_id"] = item["doc"]["user"]["id_str"]
    info["user_name"] = item["doc"]["user"]["name"]
    info["post_text"] = item["doc"]["text"]
    info["followers"] = item["doc"]["user"]["followers_count"]
    info["followees"] = item["doc"]["user"]["friends_count"]
    if item["doc"]["place"]:
        info["location"] = item["doc"]["place"]["name"]
        info["location_fullname"] = item["doc"]["place"]["full_name"]
    if item["doc"]["coordinates"]:
        info["coodinates"] = item["doc"]["coordinates"]
    info["post_time"] = item["doc"]["created_at"]
    if "retweeted_status" in item["doc"]:
        info['retweet_id'] = item["doc"]["retweeted_status"]["id_str"]
        info['retweet_user_id'] = item["doc"]["retweeted_status"]["user"]["id_str"]
    return info
       
'''
Add a tweet data structure to the structure tree

To use:
buildStructureTree(structure tree, tweet data, if print error)
''' 
def buildStructureTree(tree,item, printError):
    for key in item:
        if not isinstance(item[key],dict):
            if not tree.has_key(key):
                tree[key] = 'data'
            elif isinstance(tree[key],dict):
                if printError:
                    print 'error: exist dict type, but non-dict here: '+key
                tree[key] = 'data'
                continue
        else:
            if not tree.has_key(key):
                tree[key] = dict()
            elif not isinstance(tree[key],dict):
                if printError:
                    print 'error: exist non-dict, but dict here: '+key
                continue
            buildStructureTree(tree[key], item[key], printError)
              
'''
Traverse a certain amount of tweet data and generate a structure tree

To use:
processStructureTree(tweet data filename/path,structure tree filename/path, error and log filename/path, start index of tweet data, end index of tweet data)
''' 
def processStructureTree(fromFileNames,toFileName,errorFileName, fromIndex, toIndex):#include from exclude to
    errorFile = open(errorFileName, 'w')
    errorFile.seek(0)
    errorFile.truncate()
    errorFile.close()
    
    structureTree = dict()
    
    counter = -1
    for fromFileName in fromFileNames:
        fromFile = open(fromFileName)
        for each_row in fromFile:
            counter +=1
            if counter < fromIndex:
                continue
            elif counter >= toIndex:
                break
            if counter % 2000 is 0:
                print counter
            
            item = None
            for i in range(1,4):
                try:
                    item = json.loads(each_row[:-i])
                    break
                except:
                    continue
            if item == None:
                #print (each_row)+'\n'
                errorFile = open(errorFileName, 'a+')
                errorFile.write(each_row + '\n')  
                errorFile.close()
            else:
                buildStructureTree(structureTree, item, False)
    result = json.dumps(structureTree)
    toFile = open(toFileName, 'w')
    toFile.write(result)
    toFile.close()
    print result+'\n'
#processStructureTree(['/vol1/twitter_0301_0701.json'],'/vol1/o0StructureTree.json','/vol1/o0StructureTreeError.json',0,20000)

            
'''
Delete everything in the file

To use:
o0ClearFile(fileName/path)
''' 
def o0ClearFile(fileName):
    file = open(fileName, 'w')
    file.seek(0)
    file.truncate()
    file.close()
    
                 
'''
Append log the the file

To use:
o0Log(log filename/path, log content, if print to screen)
''' 
def o0Log(fileName,log, display):
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
        
    errorFile = open(fileName, 'a+')
    errorFile.write(log) 
    errorFile.write('\n')  
    errorFile.close()
    if display:
        print log
 
'''
Simplify tweets in all files, which only take the useful data. And divided data into multiple json files

To use:
simplifyFiles(array of original tweet filenames/paths, simplified tweet data filename/path, start index of simplified tweet data file, simplified tweet data file suffix, capacity of each simplified tweet data file, error and log filename/path, start row index of original tweet, end row index of original tweet, if print log to screen)

e.g.
simplifyFiles(['/vol2/twitter_17_0228.json','/vol1/twitter_0301_0701.json'],'/vol1/o0Combine/o0ComData',5,'.json',-1,'/vol1/o0Combine/o0ComData5.log',0,10,True)
simplifyFiles(['/vol2/twitter_17_0228.json','/vol1/twitter_0301_0701.json'],'/vol1/o0Data/o0Data',0,'.json',1000000,'/vol1/o0DataError.json',0,-1,True)
simplifyFiles(['/vol2/twitter_17_0228.json','/vol1/twitter_0301_0701.json'],'/vol1/o0Data2/o0Data',0,'.json',1000000,'/vol1/o0Data2/o0DataLog.json',0,2000000,True)
'''
def simplifyFiles(fromFileNames,toFileName,toFileIndex,toFileSuffix,toFileCapacity,errorFileName, fromRowIndex, toRowIndex, displayLog):#include from exclude to
    errorFile = open(errorFileName, 'w')
    errorFile.seek(0)
    errorFile.truncate()
    errorFile.close()
    
    toFileCounter = toFileCapacity -1
    toFile = None

    counter = -1
    for fromFileName in fromFileNames:
        fromFile = open(fromFileName)
        #fromFile.seek(8192)
        for line in fromFile:
            counter +=1
            if counter < fromRowIndex:
                continue
            elif toRowIndex is not -1 and counter >= toRowIndex:
                break
            if counter % 10000 is 0:
                o0Log(errorFileName,'Process: '+fromFileName+': ' + str(counter),displayLog)
            #print fromFile.tell()
            #print line
            
            item = None
            for i in range(1,4):
                try:
                    item = json.loads(line[:-i])
                    break
                except:
                    continue
            if item == None:
                o0Log(errorFileName,'Unsolvable data: '+line,displayLog)
            else:
                toFileCounter += 1
                if (toFileCapacity is not -1 or toFile is None) and toFileCounter >= toFileCapacity:
                    toFileCounter = 0
                    if toFile is not None:
                        toFile.seek(-2,os.SEEK_END)
                        toFile.truncate()
                        toFile.write('] ')
                        toFile.close()
                    toFile = open(toFileName+str(toFileIndex)+toFileSuffix, 'w')
                    o0Log(errorFileName,'Create file: '+toFileName+str(toFileIndex)+toFileSuffix,displayLog)
                    toFile.write('[\n')
                    toFileIndex+=1
                toFile.write(json.dumps(o0Simplify(item))+',\n')
    if toFile is not None:
        toFile.seek(-2,os.SEEK_END)
        toFile.truncate()
        toFile.write('] ')
        toFile.close()     
#simplifyFiles(['/vol2/twitter_17_0228.json','/vol1/twitter_0301_0701.json'],'/vol1/o0Combine/o0ComData',5,'.json',-1,'/vol1/o0Combine/o0ComData5.log',0,10,True)
#simplifyFiles(['/vol2/twitter_17_0228.json','/vol1/twitter_0301_0701.json'],'/vol1/o0Data/o0Data',0,'.json',1000000,'/vol1/o0DataError.json',0,-1,True)
#simplifyFiles(['/vol2/twitter_17_0228.json','/vol1/twitter_0301_0701.json'],'/vol1/o0Data2/o0Data',0,'.json',1000000,'/vol1/o0Data2/o0DataLog.json',0,2000000,True)
  
'''
Combine multi json files to one json file

To use:
combine(original json filename/path without index and suffix, start index of original json file, suffix of original json file, combined json filename/path, error and log filename/path, if print log to screen)

e.g.
combine('/vol1/o0Data/o0Data',range(26),'.json','/vol1/o0Combine/o0ComData2.json','/vol1/o0Combine/o0ComDateLog.json',True)
'''
def combine(fromFileName,fromFileIndexes,fromFileSuffix,toFileName,logFileName,displayLog):
    o0ClearFile(logFileName)
    
    toFile = open(toFileName, 'w')
    toFile.write('[\n')
    counter = -1
    for fromFileIndex in fromFileIndexes:
        fromFile = open(fromFileName+str(fromFileIndex)+fromFileSuffix)
        for line in fromFile:
            counter +=1
            if counter % 10000 is 0:
                o0Log(logFileName,'Process: '+fromFileName+str(fromFileIndex)+fromFileSuffix+': ' + str(counter),displayLog)
            if line[0] is not '{':
                continue
            elif line[-1] is ']':
                line = line[:-1]
            elif line[-2] is ',' or line[-2] is ']':
                line = line[:-2]
            toFile.write(line+',\n')
    toFile.seek(-2,os.SEEK_END)
    toFile.truncate()
    toFile.write('] ')
    toFile.close()

#combine('/vol1/o0Data/o0Data',range(26),'.json','/vol1/o0Combine/o0ComData2.json','/vol1/o0Combine/o0ComDateLog.json',True)

'''
Print several rows of target file

To use:
displayFile(filename/path to print, number of rows to print)

e.g.
displayFile('/vol1/o0DictData/o0Data0.json',10) 
'''
def displayFile(fileName,count):
    fromFile = open(fileName)
    for line in fromFile:
        count-=1
        print line
        if count is 0:
            break
#displayFile('/vol1/o0DictData/o0Data0.json',10) 

'''
Test if each row in file is one json element in json array.

To use:
testJson(filename/path to print, error and log filename/path)

e.g.
testJson('/vol1/o0DictData/o0Data13.json','/vol1/o0DictData/o0TestLog.txt')
'''
def testJson(fileName,logFileName):
    fromFile = open(fileName)
    counter = -1
    for line in fromFile:
        counter +=1
        if counter % 10000 is 0:
            o0Log(logFileName,'Process: '+fileName+': ' + str(counter),True)
        if line[-2] is '[':
            continue
        elif line[-1] is ']':
            line = line[:-1]
        elif line[-2] is ',' or line[-2] is ']':
            line = line[:-2]
            
        try:
            item = json.loads(line)
        except:
            print line
#testJson('/vol1/o0DictData/o0Data13.json','/vol1/o0DictData/o0TestLog.txt') 

'''
Transfer json array to json dictionary

To use:
JsonArrayToDict(json array filename/path, json dictionary filename/path, error and log filename/path, if print log to screen)

e.g.
JsonArrayToDict('/vol1/o0Combine/o0ComData2.json','/vol1/o0Combine/o0ComData3.json','/vol1/o0Combine/o0ArrayToDictLog.json',True)
'''
def JsonArrayToDict(fromFileName,toFileName,logFileName,displayLog):
    fromFile = open(fromFileName)
    toFile = open(toFileName, 'w')
    toFile.write('{"rows":[\n')
    counter = -1
    for line in fromFile:
        counter +=1
        if counter % 10000 is 0:
            o0Log(logFileName,'Process: '+fromFileName+': ' + str(counter),displayLog)
        if line[-2] is '[':
            continue
        elif line[-1] is ']':
            line = line[:-1]
        elif line[-2] is ',' or line[-2] is ']':
            line = line[:-2]
        toFile.write(line+',\n')
    toFile.seek(-2,os.SEEK_END)
    toFile.truncate()
    toFile.write(']}')
    toFile.close()
    o0Log(logFileName,'Finished: '+fromFileName+': ' + str(counter),displayLog)
   
'''
Transfer multi json array to json dictionary

To use:
JsonArrayToDict(json array filename/path, json dictionary filename/path, error and log filename/path, array of files indexes, files suffix, if print log to screen)

e.g.
MultiJsonArrayToDict('/vol1/o0Data/o0Data','/vol1/o0DictData/o0Data',range(26),'.json','/vol1/o0DictData/o0DateLog.json',True)
'''
def MultiJsonArrayToDict(fromFileName,toFileName,indexRange,suffix,logFileName,displayLog):
    for i in indexRange:
        JsonArrayToDict(fromFileName+str(i)+suffix,toFileName+str(i)+suffix,logFileName,displayLog)
     
#MultiJsonArrayToDict('/vol1/o0Data/o0Data','/vol1/o0DictData/o0Data',range(26),'.json','/vol1/o0DictData/o0DateLog.json',True)
#JsonArrayToDict('/vol1/o0Combine/o0ComData2.json','/vol1/o0Combine/o0ComData3.json','/vol1/o0Combine/o0ArrayToDictLog.json',True)

'''
Read coord_fixed file, and print for generating graphs

e.g.
coord_fixed('/vol1/coord_fixed.json')
'''
def coord_fixed(fromFileName):
    import json
    import random
    print 0
    text = open(fromFileName).read()
    print 1
    js = json.loads(text)
    
    #print 'user name, x, y'
    
    for item in js["Key_suspect_bot_fixed_coord_list"]:
        print item["user_name"]
        #print item["user_name"]+', '+str(random.random()-0.5)+', '+str(random.random()-0.5)
    #print counter 
#coord_fixed('/vol1/coord_fixed.json');

'''
Read follow_criterion file, and print for generating graphs

e.g.
follow_criterion('/vol1/follow_criterion.json')
'''
def follow_criterion(fromFileName):
    import json
    import random
    print 0
    text = open(fromFileName).read()
    print 1
    js = json.loads(text)
    for item in js["suspect_bot_list"]:
        print item["user_name"]
#follow_criterion('/vol1/follow_criterion.json');

'''
Read follow_RT_count file, and print for generating graphs

e.g.
follow_RT_count('/vol1/follow_RT_count.json')
'''
def follow_RT_count(fromFileName):
    import json
    import random
    print 0
    text = open(fromFileName).read()
    print 1
    js = json.loads(text)
    for item in js["suspect_bot_list"]:
        print item
#follow_RT_count('/vol1/follow_RT_count.json');

'''
Read RT_analysis file, and print for generating graphs

e.g.
RT_analysis_words('/vol1/RT_analysis.json')
'''
def RT_analysis_words(fromFileName):
    import json
    text = open(fromFileName).read()
    print 'words, count'
    js = json.loads(text)
    for key in js["top_10_words"]:
        print key+', '+str(js["top_10_words"][key])
#RT_analysis_words('/vol1/RT_analysis.json');

'''
Read RT_analysis file, and print for generating graphs

e.g.
RT_analysis_words2('/vol1/RT_analysis.json');
'''
def RT_analysis_words2(fromFileName):
    import json
    text = open(fromFileName).read()
    print 'words, count'
    js = json.loads(text)
    for key in js["top_10_words with @"]:
        print key+', '+str(js["top_10_words with @"][key])
#RT_analysis_words2('/vol1/RT_analysis.json');

'''
Read RT_analysis file, and print for generating graphs

e.g.
RT_analysis_words3('/vol1/RT_analysis.json')
'''
def RT_analysis_words3(fromFileName):
    import json
    text = open(fromFileName).read()
    print 'words, count'
    js = json.loads(text)
    for key in js["top_10_words with #"]:
        print key+', '+str(js["top_10_words with #"][key])
#RT_analysis_words3('/vol1/RT_analysis.json');

'''
Read follow_RT_analysis file, and print for generating graphs

e.g.
follow_RT_analysis_words('/vol1/RT_analysis.json')
'''
def follow_RT_analysis_words(fromFileName):
    import json
    text = open(fromFileName).read()
    print 'words, count'
    js = json.loads(text)
    for key in js["top_10_words"]:
        print key+', '+str(js["top_10_words"][key])
#follow_RT_analysis_words('/vol1/RT_analysis.json');

'''
Read follow_RT_analysis file, and print for generating graphs

e.g.
follow_RT_analysis_words2('/vol1/RT_analysis.json')
'''
def follow_RT_analysis_words2(fromFileName):
    import json
    text = open(fromFileName).read()
    print 'words, count'
    js = json.loads(text)
    for key in js["top_10_words with @"]:
        print key+', '+str(js["top_10_words with @"][key])
#follow_RT_analysis_words2('/vol1/RT_analysis.json');

'''
Read follow_RT_analysis file, and print for generating graphs

e.g.
follow_RT_analysis_words3('/vol1/RT_analysis.json')
'''
def follow_RT_analysis_words3(fromFileName):
    import json
    text = open(fromFileName).read()
    print 'words, count'
    js = json.loads(text)
    for key in js["top_10_words with #"]:
        print key+', '+str(js["top_10_words with #"][key])
#follow_RT_analysis_words3('/vol1/RT_analysis.json');

'''
calculate percentage

To use:
o0Percent(number, cardinal number, round to)

e.g.
o0Percent(5,100,2)
'''
def o0Percent(x,all,roundTo):
    print ''+str(round(float(x)/all*100*pow(10,roundTo))/pow(10,roundTo))+'% '+str(x)

'''
calculate percentage, as well as print the other part's percentage

To use:
o0Percent(number, cardinal number, round to)

e.g.
o0PercentWithOthers(5,100,2)
'''
def o0PercentWithOthers(x,all,roundTo):
    o0Percent(x,all,roundTo)
    o0Percent(all-x,all,roundTo)

#o0PercentWithOthers(89+99+1769-4,3124958,3)


'''
save large dictionary to json list

To use:
saveLargeDictJsonToList(json listfilename/path, dictionary)
'''
def saveLargeDictJsonToList(toFileName, TDict):
    toFile = open(toFileName, 'w')
    counter = -1
    toFile.write('[\n')
    for key in TDict:
        item = TDict[key]
        
        counter = counter+1
        if counter%10000 is 0:
            print counter
            
        toFile.write(json.dumps(item)+',\n')
    toFile.seek(-2,os.SEEK_END)
    toFile.truncate()
    toFile.write('] ')
    toFile.close()


'''
create dictionary for each user in tweet data, each dictionary element is one user.

To use:
createDict(tweet json filename/path, dictionary filename/path)

e.g.
createDict('/vol1/o0Combine/o0ComData4.json','/vol1/o0Combine/o0RTDict.json')
'''
def createDict(fromFileName,toFileName):
    import json
    fromFile = open(fromFileName)
    toFile = open(toFileName, 'w')
    
    TDict = dict()
    
    counter = -1
    for line in fromFile:
        try:
            jsonLine = json.loads(line[:-2])
        except:
            print line
            continue
        counter = counter+1
        if counter%10000 is 0:
            print counter
        '''
        if counter > 10000:
            break#'''
            
        if jsonLine["user_id"] not in TDict:
            TDict[jsonLine["user_id"]] = dict()
            user = TDict[jsonLine["user_id"]]
            user['user_id'] = jsonLine["user_id"]
            user['T'] = []
            user['RT'] = []
        else:
            user = TDict[jsonLine["user_id"]]
            
        if "retweet_id" not in jsonLine:
            user['T'].append(jsonLine["tweet_id"])
        else:
            user['RT'].append({"tweet_id": jsonLine["tweet_id"],"retweet_id": jsonLine["retweet_id"],"retweet_user_id": jsonLine["retweet_user_id"]})
            
    counter = -1
    toFile.write('[\n')
    for key in TDict:
        item = TDict[key]
        
        counter = counter+1
        if counter%10000 is 0:
            print counter
            
        toFile.write(json.dumps(item)+',\n')
    toFile.seek(-2,os.SEEK_END)
    toFile.truncate()
    toFile.write('] ')
    toFile.close()
#createDict('/vol1/o0Combine/o0ComData4.json','/vol1/o0Combine/o0RTDict.json')
   
'''
Calculate more data based on dictionary of Twitter users

To use:
processDict(dictionary filename/path, new dictionary filename/path)

e.g.
processDict('/vol1/o0Combine/o0RTDict.json','/vol1/o0Combine/o0RTDict2.json')
''' 
def processDict(fromFileName,toFileName):
    import json
    fromFile = open(fromFileName)
    toFile = open(toFileName, 'w')
    toFile.write('[\n')
    
    counter = -1
    for line in fromFile:
        try:
            jsonLine = json.loads(line[:-2])
        except:
            print line
            continue
        counter = counter+1
        if counter%10000 is 0:
            print counter
        '''
        if counter > 10000:
            break#'''
            
        user = dict()
        user['user_id'] = jsonLine["user_id"]
        user['T'] = jsonLine["T"]
        user['RT'] = jsonLine["RT"]
        user['TC'] = len(jsonLine["T"])
        user['RTT'] = dict()
        user['RTU'] = dict()
        for item in jsonLine["RT"]:
            if item['retweet_id'] not in user['RTT']:
                user['RTT'][item['retweet_id']] = 1
            else:
                user['RTT'][item['retweet_id']] = user['RTT'][item['retweet_id']] + 1
            if item['retweet_user_id'] not in user['RTU']:
                user['RTU'][item['retweet_user_id']] = 1
            else:
                user['RTU'][item['retweet_user_id']] = user['RTU'][item['retweet_user_id']] + 1
        
        user['RTTH'] = 0
        for key in user['RTT']:
            if user['RTTH'] < user['RTT'][key]:
                user['RTTH'] = user['RTT'][key]
        user['RTUH'] = 0
        for key in user['RTU']:
            if user['RTUH'] < user['RTU'][key]:
                user['RTUH'] = user['RTU'][key]
                
        strUser = json.dumps(user)
        '''
        if user['RTTH'] > 3:
            print 'RTTH; '+str(user['RTTH'])+'; '+user['user_id']
        if user['RTUH'] > 10:
            print 'RTUH; '+str(user['RTUH'])+'; '+user['user_id']#'''
        
        toFile.write(strUser+',\n')
        
    print counter
    toFile.seek(-2,os.SEEK_END)
    toFile.truncate()
    toFile.write('] ')
    toFile.close()
#processDict('/vol1/o0Combine/o0RTDict.json','/vol1/o0Combine/o0RTDict2.json')  
     
'''
Apply criterions to every user in dictionary

To use:
processDict(dictionary filename/path, new dictionary filename/path)

e.g.
filterDict('/vol1/o0Combine/o0RTDict2.json','/vol1/o0Combine/o0RTFilter1.json')
''' 
def filterDict(fromFileName,toFileName):
    import json
    fromFile = open(fromFileName)
    toFile = open(toFileName, 'w')
    toFile.write('[\n')
    
    counter = 0
    for line in fromFile:
        try:
            jsonLine = json.loads(line[:-2])
        except:
            print line
            continue
            
        '''
        if counter > 10000:
            break#'''
           
        numFol = len(jsonLine['RTU'])
        orig = len(jsonLine["T"])
            
        if not (jsonLine['RTUH'] > 50 and numFol < 3 and orig < 10):
            continue#'''
            
        counter = counter+1
        if counter%10000 is 0:
            print counter
            
        #print 'RTTH:'+str(jsonLine['RTTH'])+'; RTUH:'+str(jsonLine['RTUH'])+'; '+jsonLine['user_id']+'; orig:'+str(orig)+'; numFol:'+str(numFol)#'''
        
        toFile.write(json.dumps(jsonLine)+',\n')
        
    print counter
    toFile.seek(-2,os.SEEK_END)
    toFile.truncate()
    toFile.write('] ')
    toFile.close()
#filterDict('/vol1/o0Combine/o0RTDict2.json','/vol1/o0Combine/o0RTFilter1.json')
      
       
'''
Get user's all tweets by user/s name

To use:
getUsersByName(output filename/path, user/s name)
'''    
def getUsersByName(toFileName,users):
    import json
    fromFile = open('/vol1/o0Combine/o0ComData4.json')
    
    counter = -1
    for line in fromFile:
        try:
            jsonLine = json.loads(line[:-2])
        except:
            print line
            continue
            
        counter = counter+1
        
        if counter%10000 is 0:
            print counter#'''
        for user in users:
            if cmp(user,jsonLine["user_name"]) is 0:
                if 'retweet_id' not in jsonLine:
                    o0Log(toFileName+user,'tweet_id:'+jsonLine["tweet_id"]+'; '+jsonLine["post_text"],True)
                else:
                    o0Log(toFileName+user,'tweet_id:'+jsonLine["tweet_id"]+'; '+'retweet_user_id:'+jsonLine["retweet_user_id"]+'; '+jsonLine["post_text"],True)
    print counter
    
     
'''
Get user's all tweets by user/s ID

To use:
getUsers(output filename/path, user/s ID)

e.g.
getUsers('/vol1/o0Combine/o0Bot',['149529822'])
'''
def getUsers(toFileName,users):
    import json
    fromFile = open('/vol1/o0Combine/o0ComData4.json')
    
    counter = -1
    for line in fromFile:
        try:
            jsonLine = json.loads(line[:-2])
        except:
            print line
            continue
            
        counter = counter+1
        
        if counter%10000 is 0:
            print counter#'''
        for user in users:
            if cmp(user,jsonLine["user_id"]) is 0:
                if 'retweet_id' not in jsonLine:
                    o0Log(toFileName+user,'tweet_id:'+jsonLine["tweet_id"]+'; '+jsonLine["post_text"],True)
                else:
                    o0Log(toFileName+user,'tweet_id:'+jsonLine["tweet_id"]+'; '+'retweet_user_id:'+jsonLine["retweet_user_id"]+'; '+jsonLine["post_text"],True)
    print counter
#getUsers('/vol1/o0Combine/o0Bot',['149529822'])
  
     
'''
Get context of tweet by tweet/s ID

To use:
getTweet(output filename/path, tweet/s ID)

e.g.
getTweet('/vol1/o0Combine/o0HirerTweet.json',['893695240871096320'])   
'''
def getTweet(toFileName,tweets):
    import json
    fromFile = open('/vol1/o0Combine/o0ComData4.json')
    
    toFile = open(toFileName, 'w')
    toFile.seek(0)
    toFile.truncate()
    toFile.close()
    
    counter = -1
    for line in fromFile:
        try:
            jsonLine = json.loads(line[:-2])
        except:
            print line
            continue
            
        counter = counter+1
        
        if counter%1000000 is 0:
            print counter#'''
            
        for tweet in tweets:
            if cmp(tweet,jsonLine["tweet_id"]) is 0:
                #print jsonLine["post_text"]
                if 'retweet_id' not in jsonLine:
                    o0Log(toFileName,jsonLine["user_id"]+'; '+jsonLine["tweet_id"]+'; '+jsonLine["post_text"],True)
                else:
                    o0Log(toFileName,jsonLine["user_id"]+'; '+jsonLine["tweet_id"]+'; '+jsonLine["retweet_user_id"]+'; '+jsonLine["retweet_id"]+'; '+jsonLine["post_text"],True)
                break
                #o0Log(toFileName,jsonLine["post_text"],True)
    print counter
#getTweet('/vol1/o0Combine/o0HirerTweet.json',['893695240871096320'])      
      
      
     
'''
Count the number that each original tweet is retweeted. And apply criterion 4 (original tweets that only retweeted by more than 10 suspicious bot)

To use:
filterSta(users dictionary data filename/path, result filename/path)

e.g.
filterSta('/vol1/o0Combine/o0RTFilter1.json','/vol1/o0Combine/o0SuspiciousUser.json') 
'''
def filterSta(fromFileName,toFileName):
    import json
    data = json.loads(open(fromFileName).read())
    print 'Suspicious robot:'+str(len(data))
    
    sta = dict()
    
    for user in data:
        for item in user["RT"]:
            item['user_id'] = user['user_id']
            if item['retweet_id'] not in sta:
                sta[item['retweet_id']] = {}
                sta[item['retweet_id']]['count'] = 1
                sta[item['retweet_id']]['tweet'] = [item]
                break;
            else:
                sta[item['retweet_id']]['count'] += 1
                sta[item['retweet_id']]['tweet'].append(item)
                break;


                
            
        #print 'RTTH:'+str(jsonLine['RTTH'])+'; RTUH:'+str(jsonLine['RTUH'])+'; '+jsonLine['user_id']+'; orig:'+str(orig)+'; numFol:'+str(numFol)#'''      

    tweets = []
    usersCount = {}
    
    count  = 0
    for key in sta:
        count += 1
        if sta[key]['count'] > 10:
            print sta[key]['tweet'][0]['retweet_user_id']+ '; '+key + '; '+str(sta[key]['count'])
            for tweet in sta[key]['tweet']:
                tweets.append(tweet["tweet_id"])
                
                if tweet["user_id"] not in usersCount:
                    usersCount[tweet["user_id"]] = 1
                else:
                    usersCount[tweet["user_id"]] += 1
    print "Suspicious robot employers:"+str(count)
                    
    users  = {}
    for user in data:
        if user['user_id'] in usersCount:
            users[user['user_id']] = user
        

    user_idList = []
    for key in users:
        user = users[key]
        
        numFol = len(user['RTU'])
        orig = len(user["T"])
            
        '''
        if not (user['RTUH'] > 50 and numFol < 3 and orig < 1):
            continue#'''
        print 'RTTH:'+str(user['RTTH'])+'; RTUH:'+str(user['RTUH'])+'; '+user['user_id']+'; orig:'+str(orig)+'; numFol:'+str(numFol)#'''
        user_idList.append(user)
    
    print "Severely suspicious robot:"+str(len(user_idList))
    
    import time
    #getUsers('/vol1/o0Combine/o0Bot/o0User',user_idList)
    '''
    timeStamp = str(int(time.time()))
    for user in user_idList:
        getUsers('/vol1/o0Combine/o0Bot/o0'+timeStamp+'User',[user['user_id']])#'''

    
    toFile = open(toFileName, 'w')
    toFile.write(json.dumps(users))
    toFile.close()#'''
    #getTweet(toFileName,tweets)    
#filterSta('/vol1/o0Combine/o0RTFilter1.json','/vol1/o0Combine/o0SuspiciousUser.json')
import time
#getUsersByName('/vol1/o0Combine/o0Bot/o0'+str(int(time.time()))+'Hirer',['Samy ANGEL','Michel Vallance','Ankur Pate','JacquelineVictoriaReilly'])
#getUsers('/vol1/o0Combine/o0Bot/o0'+str(int(time.time()))+'CR23',['3392250739','32980366'])

   
    
'''
Find suspicious Tweets with retweet count larger than 10 and output their context.

e.g.
getSuspiciousTweet('/vol1/o0Combine/o0RTFilterRTTsta.json','/vol1/o0Combine/o0RTFilterSta2.json')
'''  
def getSuspiciousTweet(fromFileName,toFileName):
    import json
    jsonData = json.loads(open(fromFileName).read())
    
    tweets = []
    
    
    
    counter = -1
    for key in jsonData:
        counter += 1
        if jsonData[key] > 10:
            tweets.append(key)
            print key + ': '+str(jsonData[key]) 
    print len(tweets)
    
    getTweet('/vol1/o0Combine/o0HirerTwitter.json',tweets)
    
    
    toFile = open(toFileName, 'w')
    toFile.write(json.dumps(RTUsta))
    toFile.close()    #'''
#getSuspiciousTweet('/vol1/o0Combine/o0RTFilterRTTsta.json','/vol1/o0Combine/o0RTFilterSta2.json')
    
    
    
    
# python /vol1/o0Test.py
    
    
'''
Count data for generating graphs
'''   
def staListToGraData(toFileName,list): 
    dict = {}
    for i in list:
        if i not in dict:
            dict[i]= 1
        else:
            dict[i] += 1
    result = []
    for i in dict:
        result.append({'x':int(i),'y':dict[i]})
        
    
   
    toFile = open(toFileName, 'w')
    toFile.write(json.dumps(result))
    toFile.close()#'''
    
    
'''
Count data for generating graphs of criterion 1, 2 and 3

e.g.
staDict('/vol1/o0Combine/o0RTDict2.json','/vol1/o0Combine/o0Sta/o0Sta')
'''   
def staDict(fromFileName,toFileName):
    import json
    fromFile = open(fromFileName)
    
    StaRTUH = []
    StaNumFol = []
    StaOrig = []
    
    counter = -1
    for line in fromFile:
        try:
            jsonLine = json.loads(line[:-2])
        except:
            print line
            continue
            
        counter = counter+1
        if counter%10000 is 0:
            print counter
        '''
        if counter > 10000:
            break#'''
           
        numFol = len(jsonLine['RTU'])
        orig = len(jsonLine["T"])
        
        StaRTUH.append(jsonLine['RTUH'])
        StaNumFol.append(numFol)
        StaOrig.append(orig)
    print counter
    
    staListToGraData(toFileName+'RTUH.json',StaRTUH)
    staListToGraData(toFileName+'NumFol.json',StaNumFol)
    staListToGraData(toFileName+'Orig.json',StaOrig)
    
    
#staDict('/vol1/o0Combine/o0RTDict2.json','/vol1/o0Combine/o0Sta/o0Sta')
    

