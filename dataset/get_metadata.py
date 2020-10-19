"""
Collect metadata from images.

Author: Jinhui Yi
Date: 2020.10.03
"""

from PIL import Image, ExifTags
import os
import time
import random
import pickle as pkl
import shutil
from collections import Counter

IND_TO_DATE = {
    1: '20190710',
    2: '20190719',
    3: '20190730',
    4: '20190804',
    5: '20190815',
    6: '20190826',
    7: '20190903',
    8: '20190915',
    9: '20191003',
    10: '20191104', }

def get_metadata(root_path, split_random='', split_time=[], split='random'):
    t_start = time.time()

    # initialization
    img_names = []
    img_labels = []
    dates = []
    locations = []
    sizes = []

    # ------------------data split
    # random split 7:3 (train: 4006, test: 1642)
    if len(split_random) > 0:
        assert os.path.exists(split_random), "Please check your split_path"
        with open(split_random, 'r') as f:
            file_names = f.readlines()
            print("Datasplit loaded from {}".format(split_random))

    # temporal split
    elif len(split_time) > 0:
        file_names = os.listdir(root_path)
        file_names = [f for f in file_names if f[4:].startswith( tuple([IND_TO_DATE[i] for i in split_time]) )]

    else:
        file_names = os.listdir(root_path)
        # file_names = random.sample(file_names, int(0.7 * len(file_names)))

    # ----------------------read metadata from image
    for file_name in file_names:
        # print(file_name)
        img_path = os.path.join(root_path, file_name.strip())
        img = Image.open(img_path)
        # print(img.size)

        # read & correct metadata
        exif = {ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS}
        label = exif['Artist']
        label = label.replace(" ", "").replace("m+s", "M+S")        # attention!

        img_names.append(file_name)
        img_labels.append(label)
        dates.append(file_name[4:12])
        locations.append(exif['Copyright'])
        sizes.append(img.size)

    print("Num of images: ", len(img_names))
    print("Num of labels: ", sum(Counter(img_labels).values()), len(Counter(img_labels).values()),Counter(img_labels))
    print("Num of dates: ", sum(Counter(dates).values()), len(Counter(dates).values()),Counter(dates))
    print("Num of locations: ", sum(Counter(locations).values()), len(Counter(locations).values()), Counter(locations))
    print("Num of sizes: ", sum(Counter(sizes).values()), len(Counter(sizes).values()), Counter(sizes))
    print("elapsed time: {:.2f}".format(time.time() - t_start))

    return root_path, img_names, img_labels

if __name__ == '__main__':
    root_path = '../data/DND-SB/images'

    print("Analysis: collecting metadata")
    random = True                               # True: random split, False: temporal split
    split_random = './train.txt'                # ./train.txt | ./test.txt
    split_time = [1]                            # a sub set of [1,2,3,4,5,6,7,8,9,10], indicating different dates
    get_metadata(root_path, split_random if random else '', split_time if not random else [])
