import ngram
import time
start_time = time.time()

with open('/Users/soumyajyotidutta/Desktop/autoyara/calc.exe', 'rb') as file:
    # Read the binary content of the file
    binary_content = file.read()

index = ngram.NGram(N=512)
x = list(index.ngrams((binary_content)))
print(x)
print("--- %s seconds ---" % (time.time() - start_time))