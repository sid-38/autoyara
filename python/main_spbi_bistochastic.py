import os
import re
import pickle
import numpy as np
from sklearn.cluster import SpectralCoclustering
from sklearn.cluster import SpectralBiclustering
from AutoYaraCluster import *
from NGram import NGram, NGramCluster
from YaraRuleCreator import *

def sigCandidate_to_NGram(uid, sig_candidate, size):
    signature = sig_candidate.getSignature()
    ngram_list = []
    for i in range(size):
        ngram_list.append(signature.getUnsigned(i))
    return NGram(uid,ngram_list)

def main():
    
    
    filepath_maliciousBytes = input('Enter the filepath for malicious bytes: ')
    filepath_benignBytes = input('Enter the filepath for benign bytes: ')
    filepath_trainMalware = input('Enter the filepath for train malware files: ')
    
    sigcandidates, signaturecandidate_keys = getSigcandidates(filepath_maliciousBytes, 
                                     filepath_benignBytes, 
                                     filepath_trainMalware)
    
    
    filecount = getFilecount(filepath_trainMalware)
    bloomSizes = list(signaturecandidate_keys)
    # bloomSizes = [8,16]
    clusterSizes = [2, 3, 4, 5]
    for bloomSize in bloomSizes:
        for clusterSize in clusterSizes:
            # print(f"{bloomSize} n-grams")
            dataMatrix = createDataset(sigcandidates, bloomSize, filecount)
            clustering = SpectralBiclustering(n_clusters=clusterSize, method='bistochastic').fit(dataMatrix)
            clusterRows, clusterCols = clustering.row_labels_, clustering.column_labels_

            clusters = dict()
            # print(clusters)  


            for i,cluster in enumerate(clusterCols):
                if cluster not in clusters:
                    new_ngram_cluster = NGramCluster(cluster, bloomSize)
                    new_ngram_cluster.add_ngram(sigCandidate_to_NGram(i, sigcandidates[bloomSize][i], bloomSize))
                    clusters[cluster] = new_ngram_cluster
                else:
                    clusters[cluster].add_ngram(sigCandidate_to_NGram(i, sigcandidates[bloomSize][i], bloomSize))

            for i, cluster in enumerate(clusterRows):
                # Ignoring clusters with just samples and no ngrams
                if cluster in clusters:
                    clusters[cluster].add_sample(i)

            # Removing clusters with just ngrams and no samples

            for cluster_id in clusters.keys():
                if len(clusters[cluster_id].ngrams) == 0:
                    # print("Deleting a cluster with no ngrams")
                    del clusters[cluster_id]

            print(ngram_clusters_to_yara(list(clusters.values()), dataMatrix, name=f"rule_{bloomSize}ngram_{clusterSize}clusters"))
    
    
main()
