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
        # print(hashes)

similarityInfo = {}
candidates = []
sims = []
counts = {}        
for i in range(len(hashes)):
    count = 0
    for j in range (i+1, len(hashes)):
        sim = ssdeep.compare(hashes[i], hashes[j])
        
        if sim >= 25:
            sims.append(sim)
            candidates.append([j])
            similarityInfo.update({f'{j}': sim})
            count = count + 1
    counts.update({i: count})

print(counts)
        
# with open('./similarityInfo.pkl', 'wb') as f:
#     pickle.dump(similarityInfo, f)
    