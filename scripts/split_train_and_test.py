import os
import shutil
import argparse
from threading import Thread


parser = argparse.ArgumentParser(description='Split data into train and test sets.')
parser.add_argument('subjects_root_path', type=str, help='Directory containing subject sub-directories.')
parser.add_argument('--test_set_file', type=str, help='Location of csv file that partitions between the training set and test set', default="resources/testset.csv")
args, _ = parser.parse_known_args()

testset = set()
with open(args.test_set_file, "r") as test_set_file:
    for line in test_set_file:
        x, y = line.split(',')
        if int(y) == 1:
            testset.add(x)

def move_to_partition(patients, partition):
    i = 0
    if not os.path.exists(os.path.join(args.subjects_root_path, partition)):
        os.mkdir(os.path.join(args.subjects_root_path, partition))
    for patient in patients:
        print("moving patient " + str(i))
        i += 1
        if not os.path.exists(os.path.join(os.path.join(args.subjects_root_path, patient))):
            continue
        src = os.path.join(args.subjects_root_path, patient)
        dest = os.path.join(args.subjects_root_path, partition, patient)
        shutil.move(src, dest)


folders = os.listdir(args.subjects_root_path)
folders = list((filter(str.isdigit, folders)))
train_patients = [x for x in folders if not x in testset]
test_patients = [x for x in folders if x in testset]

assert len(set(train_patients) & set(test_patients)) == 0

for i in range(0, 10):
    if i != 9:
        thr = Thread(target=move_to_partition, args=(train_patients[int(len(train_patients)*i/10):int(len(train_patients)*(i+1)/10)], "train"))
        thr.run()
        thr = Thread(target=move_to_partition, args=(test_patients[int(len(test_patients)*i/10):int(len(test_patients)*(i+1)/10)], "test"))
        thr.run()
    else:
        thr = Thread(target=move_to_partition, args=(train_patients[int(len(train_patients)*i/10):], "train"))
        thr.run()
        thr = Thread(target=move_to_partition, args=(test_patients[int(len(test_patients)*i/10):], "test"))
        thr.run()
    
print("done!")
