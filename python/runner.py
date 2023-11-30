import sys
import shutil
import os
from sklearn.model_selection import train_test_split
from main import main
import yara
import evaluator

path = sys.argv[1]
benign_path = sys.argv[2]
ben_bytes = sys.argv[3]
mal_bytes = sys.argv[4]
ben_name = sys.argv[5]
mal_name = sys.argv[6]

# for root, d_names, f_names in os.walk(path):
#    print(f_names)
files = []

for root, d_names, f_names in os.walk(path):
    # check if current file_path is a file
    for f_name in f_names:
        files.append(os.path.abspath(os.path.join(root,f_name)))

benign_files = []

for root, d_names, f_names in os.walk(benign_path):
    # check if current file_path is a file
    for f_name in f_names:
        benign_files.append(os.path.abspath(os.path.join(root,f_name)))

# evaluations_avg = {
#         'accuracy' : 0.0,
#         'precision' : 0.0,
#         'recall': 0.0,
#         'f1': 0.0,
#         'count': 0
#         }

evaluations_avg = dict()

for i in range(20):
    print("Iteration", i)
    files_train, files_test = train_test_split(files, test_size =0.99, train_size = 0.01)



    malware_train_dir = os.path.abspath("./malware_train")
    shutil.rmtree(malware_train_dir)
    os.mkdir(malware_train_dir)
    for file_path in files_train:
        shutil.copy(file_path, malware_train_dir)

    yara_rules = main(malware_train_dir, ben_bytes, mal_bytes)

    # print(yara_rules)
    if os.path.exists("./yara_rules.yar"):
      os.remove("./yara_rules.yar")

    with open('./yara_rules.yar','w') as f:
        f.writelines(yara_rules)

    yara_compiled = yara.compile("./yara_rules.yar")
    yara_matches = []
    for file_path in files_test:
        matches = yara_compiled.match(file_path)
        for match in matches:
            # print(match)
            yara_matches.append(str(match) + " " + file_path) 

    for file_path in benign_files:
        matches = yara_compiled.match(file_path)
        for match in matches:
           yara_matches.append(str(match) + " " + file_path) 


    evaluations = evaluator.evaluate(yara_matches, len(benign_files), len(files_test), ben_name, mal_name)

    for rule_name in evaluations:
        if rule_name not in evaluations_avg:
            evaluations_avg[rule_name] = { 
                                'accuracy' : 0.0,
                                'precision' : 0.0,
                                'recall': 0.0,
                                'f1': 0.0,
                                'tp': 0.0,
                                'tn': 0.0,
                                'fp': 0.0,
                                'fn': 0.0,
                                'count': 0
                                }
        for key in ['accuracy','precision','recall','f1', 'tp', 'fp', 'tn', 'fn']:
            evaluations_avg[rule_name][key] = ((evaluations_avg[rule_name][key] * evaluations_avg[rule_name]['count']) + evaluations[rule_name][key])/(evaluations_avg[rule_name]['count'] + 1)
        evaluations_avg[rule_name]['count'] += 1

    
    print(evaluations_avg)










