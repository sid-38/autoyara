import os
import re
import numpy as np
from sklearn.cluster import SpectralCoclustering

from py4j.java_gateway import JavaGateway

def collectBloomSizes(filepaths):

    sizes = set()
    for filepath in filepaths:
        for root, dirs, files in os.walk(filepath, topdown=False):
           for name in files:
              sizes.add(int(re.search(r"^.+\_(\d+)\.bloom", name).groups()[0]))
    sizes = list(sizes)
    sizes.sort()
    return sizes

def collectBloomFilters(filepath):
    pass

def buildCandidateSet():
    pass

def getSigcandidates(malware_bloom_dir, benign_bloom_dir, live_mal_dir):
    
    gateway = JavaGateway()

    # mal_dir = "/Users/soumyajyotidutta/AutoYara 2/malicious-bytes"
    # ben_dir = "/Users/soumyajyotidutta/AutoYara 2/benign-bytes"
    # live_mal_dir = "/Users/soumyajyotidutta/Desktop/caution!!"
    
    mal_dir = malware_bloom_dir
    ben_dir = benign_bloom_dir
    # Create an ordered list of bloom sizes
    bloomSizes = collectBloomSizes([mal_dir, ben_dir])
    # bloomSizes = [8]
    # Create bloom filters
    mal_bloom = collectBloomFilters(mal_dir)
    ben_bloom = collectBloomFilters(ben_dir)

    # TO-DO: Java implementation is atomic. Should we care?
    best_rule_coverage = 0.0
    meets_min_desired_coverage = False
    
    print(bloomSizes);
    
    sigcandidates = {}
    
    for bloomSize in bloomSizes:
        if best_rule_coverage >= 1.0 and meets_min_desired_coverage:
            break # Break or Return ??

        # print(os.path.abspath("./mw1"))
        # print(os.path.abspath(ben_dir))
        # print(os.path.abspath(mal_dir))
        final_candidates = gateway.entry_point.myBuildCandidateSet(os.path.abspath(live_mal_dir), os.path.abspath(ben_dir), os.path.abspath(mal_dir), bloomSize, 100, 100, False, 0.001)
        # print(final_candidates)
        
        sigcandidates.update({bloomSize: final_candidates})
        sigkeys = sigcandidates.keys()
        
    return sigcandidates, sigkeys

def getFilecount(dir_path):
    # dir_path = r'/Users/soumyajyotidutta/Desktop/caution!!'
    count = 0
    for path in os.listdir(dir_path):

        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    # print('File count:', count)
    
    return count

def createDataset(signatureCandidates: dict, ngramSize: int, numberOfFiles: int):
    
    # print(signatureCandidates)
    # sigkeys = list(signatureCandidates.keys())
    # print(sigkeys)
    # sigIndex = np.where(sigkeys == ngramSize) 
    # print(sigIndex)
    sigcandidate_required = signatureCandidates[ngramSize]
    
    datamatrix = np.zeros((numberOfFiles, len(sigcandidate_required)))
    # print("HERE", datamatrix)
    for i, sigCandid in enumerate(sigcandidate_required):
        
        cover = sigCandid.getCoverage()
        
        for fileNumber in cover:
            datamatrix[fileNumber][i] = 1
    # print(datamatrix, type(datamatrix))
    # return datamatrix, sigcandidate_required
    return datamatrix

