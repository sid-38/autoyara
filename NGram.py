class NGram:
    def __init__(self, ngram_list):
        self.ngram_list = ngram_list
        self.name = ''.join(f"{ngram_int} " for ngram_int in ngram_list).strip()
        self.int_rep = ''.join(f"{ngram_int} " for ngram_int in ngram_list).strip()
        self.size = len(ngram_list)

class NGramCluster:
    def __init__(self, uid,  ngrams=[], samples=[]):
        self.uid = uid
        self.ngrams = ngrams
        self.samples = samples

    def add_ngram(self,ngram):
        self.ngrams.append(ngram)

    def add_sample(self,sample):
        self.samples.append(sample)

    def get_minCount(self):
        return len(self.ngrams)
