from NGram import NGram 

def ngram_clusters_to_yara(ngram_clusters, name="untitled"):
    new_line = "\n"
    tab = "\t"
    rule = ""
    strings = ""
    ngrams_with_nums = dict()
    next_ngram_num = 1

    for ngram_cluster in ngram_clusters:
        for ngram in ngram_cluster.ngrams:
            
    # for cluster_counts in ngram_clusters:
    #     for ngram in cluster_counts['cluster']:
            if ngram.name in ngrams_with_nums:
                ngram_num = ngrams_with_nums[ngram.name]
            else:
                ngrams_with_nums[ngram.name] = next_ngram_num
                ngram_num = next_ngram_num
                next_ngram_num += 1

            strings += f"$x{ngram_num} = " + "{" + ngram.int_rep + "},\n\t\t"  

    condition = ""

    for j,ngram_cluster in enumerate(ngram_clusters):
        condition += f"({ngram_cluster.get_minCount()} of ("
        for i,ngram in enumerate(ngram_cluster.ngrams):
            condition += f"$x{ngrams_with_nums[ngram.name]}"
            if i != len(ngram_cluster.ngrams) - 1:
                condition += ','
        condition += '))'
        if j != len(ngram_clusters) - 1:
            condition += ' or '
                
    rule += "rule " + name + "\n{\n\tstrings:\n\t\t" + strings + "\n\tcondition:\n\t\t" + condition + "}"
    return rule

def main():

    test_ngram_clusters = [
            {
                'cluster': [NGram([23,43,12]),NGram([13,32,54]),NGram([54,25,76])],
                'count': 2
            },
            {
                'cluster': [NGram([11,34]),NGram([79,98,87])],
                'count': 3
            }
        ]
    print(ngram_clusters_to_yara(test_ngram_clusters, name="test"))

# main()

            
            
