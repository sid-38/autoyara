class NGram:
    def __init__(self, ngram_list):
        self.ngram_list = ngram_list
        self.name = ''.join(f"{ngram_int} " for ngram_int in ngram_list).strip()
        self.int_rep = ''.join(f"{ngram_int} " for ngram_int in ngram_list).strip()
        self.size = len(ngram_list)
    
