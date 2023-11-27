import os
import re
import pickle
import numpy as np
from sklearn.cluster import SpectralCoclustering
from AutoYaraCluster import *

def main():
    
    
    
    sigcandidates, signaturecandidate_keys = getSigcandidates("/Users/soumyajyotidutta/AutoYara 2/malicious-bytes", 
                                     "/Users/soumyajyotidutta/AutoYara 2/benign-bytes", 
                                     "/Users/soumyajyotidutta/Desktop/caution!!")
    
    
    filecount = getFilecount("/Users/soumyajyotidutta/Desktop/caution!!")
    dataMatrix = createDataset(sigcandidates, 8, filecount)
    clustering = SpectralCoclustering(n_clusters=2, random_state=0).fit(dataMatrix)
    clusterRows, clusterCols = clustering.row_labels_, clustering.column_labels_
    
    print('Signature Candidates\n', sigcandidates)
    print('Signature Candidates Keys\n', signaturecandidate_keys)
    print('File Count\n', filecount)
    print('Data Matrix\n', dataMatrix, type(dataMatrix))
    print(clusterRows , clusterCols)

    
    
    
    
main()