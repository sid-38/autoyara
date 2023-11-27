from NGram import NGram 

def ngram_clusters_to_yara(ngram_clusters, name="untitled"):
    new_line = "\n"
    tab = "\t"
    rule = ""
    strings = ""
    ngrams_with_nums = dict()
    next_ngram_num = 1
    for cluster_counts in ngram_clusters:
        for ngram in cluster_counts['cluster']:
            if ngram.name in ngrams_with_nums:
                ngram_num = ngrams_with_nums[ngram.name]
            else:
                ngrams_with_nums[ngram.name] = next_ngram_num
                ngram_num = next_ngram_num
                next_ngram_num += 1

            strings += f"$x{ngram_num} = " + "{" + ngram.int_rep + "},\n\t\t"  

    condition = ""
    for j, cluster_counts in enumerate(ngram_clusters):
        condition += f"({cluster_counts['count']} of ("
        for i, ngram in enumerate(cluster_counts['cluster']):
            condition += f"$x{ngrams_with_nums[ngram.name]}"
            if i != len(cluster_counts['cluster']) - 1:
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

            
            
