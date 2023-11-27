import os
import re
import pickle
import numpy as np
from sklearn.cluster import SpectralCoclustering
from AutoYaraCluster import *
from NGram import NGram, NGramCluster
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
        

        clusters = dict()


        for i,cluster in enumerate(clusterCols):
            if cluster not in clusters:
                new_ngram_cluster = NGramCluster(cluster)
                new_ngram_cluster.add_ngram(sigCandidate_to_NGram(sigcandidates[bloomSize][i], bloomSize))
                clusters[cluster] = new_ngram_cluster
            else:
                clusters[cluster].add_ngram(sigCandidate_to_NGram(sigcandidates[bloomSize][i], bloomSize))

        for i, cluster in enumerate(clusterRows):
            clusters[cluster].add_sample(i)

        print(ngram_clusters_to_yara(list(clusters.values()), name=f"{bloomSize}_rule"))
    
    
main()
