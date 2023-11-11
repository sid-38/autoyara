import os
import re

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


def main():
    mal_dir = "./malicious-bytes"
    ben_dir = "./benign-bytes"

    # Create an ordered list of bloom sizes
    boolSizes = collectBloomSizes([mal_dir, ben_dir])

    # Create bloom filters
    mal_bloom = collectBloomFilters(mal_dir)
    ben_bloom = collectBloomFilters(ben_dir)

    # TO-DO: Java implementation is atomic. Should we care?
    best_rule_coverage = 0.0
    meets_min_desired_coverage = False
    
    for bloomSize in bloomSizes:
        if best_rule_coverage >= 1.0 and meets_min_desired_coverage:
            break





