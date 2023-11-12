from collections import Counter

def extract_byte_ngrams(file_path, n):
    with open(file_path, 'rb') as file:
        # Read the binary content of the file
        binary_content = file.read()

        # Extract byte n-grams
        byte_ngrams = [binary_content[i:i+n] for i in range(len(binary_content) - n + 1)]

    return byte_ngrams

def frequency(byte_ngrams):

	return Counter(byte_ngrams)

# Example usage: Extracting byte 3-grams from an exe file
file_path = '/Users/soumyajyotidutta/Desktop/autoyara/calc.exe'
n = 1024
result = extract_byte_ngrams(file_path, n)
frequency = frequency(result)

# Print the result
for ngram in result:
    print(ngram)

print(frequency)
