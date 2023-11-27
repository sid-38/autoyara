import os
import re
import pickle
import numpy as np
from sklearn.cluster import SpectralCoclustering
from AutoYaraCluster import *
from NGram import NGram
from YaraRuleCreator import *

def sigCandidate_to_NGram(sig_candidate, size):
    signature = sig_candidate.getSignature()
    ngram_list = []
    for i in range(size):
        ngram_list.append(signature.getUnsigned(i))
    return NGram(ngram_list)

def main():
    
    
    
    sigcandidates, signaturecandidate_keys = getSigcandidates("./malicious-bytes", 
                                     "./benign-bytes", 
                                     "./mw1")
    
    
    filecount = getFilecount("./mw1")
    bloomSizes = list(signaturecandidate_keys)
    for bloomSize in bloomSizes:
        print(f"{bloomSize} n-grams")
        dataMatrix = createDataset(sigcandidates, bloomSize, filecount)
        clustering = SpectralCoclustering(n_clusters=2, random_state=0).fit(dataMatrix)
        clusterRows, clusterCols = clustering.row_labels_, clustering.column_labels_
        
        # print('Signature Candidates\n', sigcandidates)
        # print('Signature Candidates Keys\n', signaturecandidate_keys)
        # print('File Count\n', filecount)
        # print('Data Matrix\n', dataMatrix, type(dataMatrix))
        # print(clusterRows , clusterCols)

        clusters = dict()
        for i, cluster in enumerate(clusterCols):
            if cluster in clusters:
                clusters[cluster].append(sigCandidate_to_NGram(sigcandidates[bloomSize][i], bloomSize))
            else:
                clusters[cluster] = [sigCandidate_to_NGram(sigcandidates[bloomSize][i], bloomSize)]
        # print('NGram Clusters\n', clusters)

        ngram_clusters = []
        for key in clusters:
            ngram_clusters.append({'cluster':clusters[key], 'count':len(clusters[key])})

        # print('NGram Clusters new\n', ngram_clusters)

        print(ngram_clusters_to_yara(ngram_clusters, name=f"{bloomSize}_rule"))
    
    
main()
