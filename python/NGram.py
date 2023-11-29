import statistics
import math

class NGram:
    def __init__(self, uid, ngram_list):
        self.uid = uid
        self.ngram_list = ngram_list
        self.name = ''.join(f"{ngram_int} " for ngram_int in ngram_list).strip()
        self.int_rep = ''.join(f"{ngram_int:02x} " for ngram_int in ngram_list).strip()
        self.ascii_string = ''.join(chr(ngram_int) for ngram_int in ngram_list)
        self.size = len(ngram_list)

class NGramCluster:
    def __init__(self, uid, size, ngrams=None, samples=None):
        self.uid = uid
        if ngrams:
            self.ngrams = ngrams
        else:
            self.ngrams = []
        if samples:
            self.samples = samples
        else:
            self.samples = []
        self.size = size 

    def add_ngram(self,ngram):
        self.ngrams.append(ngram)

    def add_sample(self,sample):
        self.samples.append(sample)

    def is_contain_ngram(self, ngram_id:int):
        for ngram in self.ngrams:
            if ngram.uid == ngram_id:
                return True

        return False

    def get_minCount(self, dataMatrix):
        # return len(self.ngrams)
        file_occurence_counts = []
        for sample in self.samples:
            num_ngrams = 0
            for ngram_id, value in enumerate(dataMatrix[sample]):
                if self.is_contain_ngram(ngram_id) and value > 0:
                    num_ngrams += 1
            file_occurence_counts.append(num_ngrams)

        file_occurence_counts.sort()

        if(len(file_occurence_counts) == 0):
            return 0

        # print(file_occurence_counts)


        min_variance = math.inf
        min_index = -1
        
        for i in range(len(file_occurence_counts)):
            left_portion = file_occurence_counts[:i]
            right_portion = file_occurence_counts[i:]
            left_portion_variance = 0
            right_portion_variance = 0
            if len(left_portion) > 1:
                left_portion_variance = statistics.variance(left_portion)
            if len(right_portion) > 1:
                right_portion_variance = statistics.variance(right_portion)
            # total_variance = statistics.variance(left_portion) * len(left_portion) + statistics.variance(right_portion) * len(right_portion)
            total_variance = left_portion_variance * len(left_portion) + right_portion_variance * len(right_portion)
            if total_variance < min_variance:
                # print(f"Changing min index from {min_index} to {i}")
                min_index = i
                min_variance = total_variance 

        index = min(len(file_occurence_counts)-1 , min_index)
        # print(index) 
            
        return file_occurence_counts[index]
        # return file_occurence_counts[-1]
