import os
import re

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


def main():

    gateway = JavaGateway()

    mal_dir = "./malicious-bytes"
    ben_dir = "./benign-bytes"

    # Create an ordered list of bloom sizes
    bloomSizes = collectBloomSizes([mal_dir, ben_dir])

    # Create bloom filters
    mal_bloom = collectBloomFilters(mal_dir)
    ben_bloom = collectBloomFilters(ben_dir)

    # TO-DO: Java implementation is atomic. Should we care?
    best_rule_coverage = 0.0
    meets_min_desired_coverage = False
    
    print(bloomSizes);
    
    for bloomSize in bloomSizes:
        if best_rule_coverage >= 1.0 and meets_min_desired_coverage:
            break # Break or Return ??

        print(os.path.abspath("./mw1"))
        print(os.path.abspath(ben_dir))
        print(os.path.abspath(mal_dir))
        final_candidates = gateway.entry_point.myBuildCandidateSet(os.path.abspath("./mw1"), os.path.abspath(ben_dir), os.path.abspath(mal_dir), bloomSize, 100, 100, False, 0.001)
        print(final_candidates)

main()







