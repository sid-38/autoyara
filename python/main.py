import os
import sys
import re
import pickle
import numpy as np
from sklearn.cluster import SpectralCoclustering
from AutoYaraCluster import *
from NGram import NGram, NGramCluster
from YaraRuleCreator import *
from py4j.java_gateway import JavaGateway

def sigCandidate_to_NGram(uid, sig_candidate, size):
    signature = sig_candidate.getSignature()
    ngram_list = []
    for i in range(size):
        ngram_list.append(signature.getUnsigned(i))

    return NGram(uid,ngram_list)

def main(filepath_trainMalware, filepath_benignBytes, filepath_maliciousBytes):
    
    rules = [] 
    gateway = JavaGateway()
    
    sigcandidates, signaturecandidate_keys = getSigcandidates(gateway, filepath_maliciousBytes,filepath_benignBytes,filepath_trainMalware)
    
    
    filecount = getFilecount(filepath_trainMalware)
    bloomSizes = list(signaturecandidate_keys)
    # bloomSizes = [8,16]
    # clusterSizes = input('Enter the array of cluster sizes you wanna experiment with: ')
    clusterSizes = [2,3,4,5]
    for bloomSize in bloomSizes:
        for clusterSize in clusterSizes:
            # print(f"{bloomSize} n-grams")
            dataMatrix = createDataset(sigcandidates, bloomSize, filecount)
            try:
                clustering = SpectralCoclustering(n_clusters=clusterSize).fit(dataMatrix)
            except ValueError:
                print(ValueError)
                continue
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

            rules.append(ngram_clusters_to_yara(list(clusters.values()), dataMatrix, name=f"rule_{bloomSize}ngram_{clusterSize}clusters"))

    for size in sigcandidates:
        for obj in sigcandidates[size]:
            gateway.detach(obj)

    return rules
    
    
# if __name__ == "__main__":
#     filepath_maliciousBytes = sys.argv[2]
#     filepath_benignBytes = sys.argv[1]
#     filepath_trainMalware = sys.argv[3]

#     rules = main(filepath_trainMalware, filepath_benignBytes, filepath_maliciousBytes)
#     for rule in rules:
#         print(rule)
