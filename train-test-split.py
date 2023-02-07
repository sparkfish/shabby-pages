import os
import shutil
from pathlib import Path
import cv2
import random
from multiprocessing import Pool
import sys
import math

random.seed(0)
train_percent = 0.7
validate_percent = 0.2
test_percent = 0.1

clean_patch_path = Path("patches/clean_patches")
shabby_patch_path = Path("patches/shabby_patches")
train_clean_path = Path("patches/train_clean")
train_clean_path.mkdir()
train_path = Path("patches/train")
train_path.mkdir()
validate_clean_path = Path("patches/validate_clean")
validate_clean_path.mkdir()
validate_path = Path("patches/validate")
validate_path.mkdir()
test_clean_path = Path("patches/test_clean")
test_clean_path.mkdir()
test_path = Path("patches/test")
test_path.mkdir()


clean_patches = sorted(os.listdir("patches/clean_patches"))
shabby_patches = sorted(os.listdir("patches/shabby_patches"))

num_patches = len(train_clean_patches)
indices = range(num_patches)

train_count = math.floor(train_percent * num_patches)
train_sample = random.sample(indices, train_count)

validate_count = math.floor(validate_percent * num_patches)
indices_not_train = list(set(indices).difference(set(train_sample)))
validate_sample = random.sample(indices_not_train, validate_count)

test_count = num_patches - train_count - validate_count
indices_not_train_validate = list(set(indices).difference(set(train_sample)).difference(set(validate_sample)))
test_sample = indices_not_train_validate

for i in train_sample:
    shutil.copyfile(clean_patch_path / clean_patches[i], train_clean_path / clean_patches[i])
    shutil.copyfile(shabby_patch_path / shabby_patches[i], train_path / shabby_patches[i])

for i in validate_sample:
    shutil.copyfile(clean_patch_path / clean_patches[i], validate_clean_path / clean_patches[i])
    shutil.copyfile(shabby_patch_path / shabby_patches[i], validate_path / shabby_patches[i])

for i in test_sample:
    shutil.copyfile(clean_patch_path / clean_patches[i], test_clean_path / clean_patches[i])
    shutil.copyfile(shabby_patch_path / shabby_patches[i], test_path / shabby_patches[i])

# check that all went according to plan
train_cleans = sorted(os.listdir(train_clean_path))
trains = sorted(os.listdir(train_path))
validate_cleans = sorted(os.listdir(validate_clean_path))
validates = sorted(os.listdir(validate_path))
test_cleans = sorted(os.listdir(test_clean_path))
tests = sorted(os.listdir(test_path))

print(f"Complete: {(train_cleans + validate_cleans + test_cleans) == clean_patches && (trains + validates + tests) == shabby_patches}")
