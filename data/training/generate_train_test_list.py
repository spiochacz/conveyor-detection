from os import listdir
from os.path import isfile, join
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Generate train.txt and test.txt files.')
parser.add_argument('--DIR_PATH', type=str, default='generated',
                    help='images directory path')
parser.add_argument('--TEST_SIZE', type=float, default=0.08,
                    help='test size, float between 0.0 and 1.0, the proportion of the dataset to include in the test split')
parser.add_argument('--RANDOM_STATE', type=int, default=42,
                    help='just random state')
args = parser.parse_args()

DIR_PATH = args.DIR_PATH
TEST_SIZE = args.TEST_SIZE
random_state = args.RANDOM_STATE

np.random.seed(random_state)

def check_image(path):
    if not path.endswith(".jpg"):
        return False
    without_extension = path.split(".")[0]
    if without_extension.endswith("mask") or without_extension.endswith("p_label") or without_extension.endswith("vis"):
        return False
    else:
        return True


def print_file(file, data):
    out = ""
    for filename in data:
        out = out + DIR_PATH + "/" + filename.split('.')[0] + "\n"
    with open(file, 'w') as fout:
        fout.write(out)



filtered_files = [f for f in listdir(DIR_PATH) if isfile(join(DIR_PATH, f)) and check_image(f)]
TOTAL_SIZE = len(filtered_files)

# print(filtered_files)
print(f'TOTAL_SIZE={TOTAL_SIZE}')

files_without_flip = [i for i in filtered_files if not i.split('.')[0].endswith('flip')]

indexes = np.random.randint(low=0, high=len(files_without_flip), size=int(TEST_SIZE * TOTAL_SIZE))

test = np.array(files_without_flip)[indexes]
train = list(set(filtered_files).difference(test))

print(f'TEST_SIZE={len(test)}')

print_file("train.txt", train)
print_file("test.txt", test)