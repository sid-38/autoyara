import ssdeep
import seaborn as sns
import os
import pickle

basepath = '/Users/soumyajyotidutta/Desktop/WinMM/'

filelist = []
for root, dirs, files in os.walk(basepath, topdown=True): 
    # with open(basepath + file, 'rb') as content:
    #     binary = content.read()
    # hashes.append(ssdeep.hash(binary))
    # print(hashes)
    filelist += files     
    
hashes = []
for file in filelist:
    with open(basepath + file, 'rb') as content:
        
        binary = content.read()
        
        hashes.append(ssdeep.hash(binary))
        
fileNumber = input('Enter File Number: ')
fileNumber = int(fileNumber)
req_files = []
for j in range (len(hashes)):
    sim = ssdeep.compare(hashes[fileNumber], hashes[j])
        
    if sim >= 15:
        req_files.append(filelist[j])

print(req_files)