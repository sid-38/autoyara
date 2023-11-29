import sys 
import re

if len(sys.argv) < 4:
    print("Not enough arguments")
    sys.exit(1)

results_filepath = sys.argv[1]
num_of_benign = int(sys.argv[2])
num_of_malicious = int(sys.argv[3])

print("Num of benign", num_of_benign)
print("Num of malicious", num_of_malicious)
evaluations = dict()

with open(results_filepath) as f:
    for line in f:
        words = line.split()
        rule_name = words[0]
        if rule_name not in evaluations:
            evaluations[rule_name] = {
                    'mal_count': 0,
                    'ben_count': 0
                    }
        detected_filename = words[1]
        if re.search("malware", detected_filename):
            evaluations[rule_name]['mal_count'] += 1
        elif re.search("benign", detected_filename):
            evaluations[rule_name]['ben_count'] += 1
        else:
            print("Something else found")


for rule_name in evaluations:
    print(rule_name)
    tp = evaluations[rule_name]["mal_count"]
    fp = evaluations[rule_name]["ben_count"]
    tn = num_of_benign - fp
    fn = num_of_malicious - tp
    accuracy = (tp+tn)/(tp+tn+fp+fn)
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    f1 = (2*precision*recall)/(precision+recall)
    evaluations[rule_name]['tp'] = tp
    evaluations[rule_name]['fp'] = fp
    evaluations[rule_name]['tn'] = tn
    evaluations[rule_name]['fn'] = fn
    evaluations[rule_name]['accuracy'] = accuracy
    evaluations[rule_name]['precision'] = precision
    evaluations[rule_name]['recall'] = recall
    evaluations[rule_name]['f1'] = f1
    print("TP", tp,"FP", fp, "TN", tn, "FN", fn,)

    print("Accuracy", accuracy*100)
    print("Precision", precision)
    print("Recall", recall)
    print("F1", f1)
    print("\n")
print(evaluations)

       

# print(evaluations)



sys.exit(0)
