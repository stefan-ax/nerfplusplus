"""
Input should be data/diamond/venus-rough-1/posed_images/kai_cameras_normalized.json
Outpout should be like data/tanks_and_temples/tat_training_Truck/*

"""

import json
import os
import argparse
import shutil
import numpy as np
from tqdm.auto import tqdm

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transform Kai to Nerf')
    parser.add_argument('path', help='Path to where /images and kai_cameras.txt are.')
    parser.add_argument('output_path', help='Path where train/, test/ will be saved.')
    parser.add_argument('--test_size', help='Test percentage (default: 0.1)', default=.1, type=float)
    args = parser.parse_args()

    cameras_path = os.path.join(args.path, 'kai_cameras_normalized.json')
    images_path = os.path.join(args.path, 'images/')

    train_path_rgb = os.path.join(args.output_path, 'train', 'rgb')
    train_path_pose = os.path.join(args.output_path, 'train', 'pose')
    train_path_intrinsics = os.path.join(args.output_path, 'train', 'intrinsics')
    test_path_rgb = os.path.join(args.output_path, 'test', 'rgb')
    test_path_pose = os.path.join(args.output_path, 'test', 'pose')
    test_path_intrinsics = os.path.join(args.output_path, 'test', 'intrinsics')

    for path in [train_path_rgb, train_path_pose, train_path_intrinsics,
                 test_path_rgb, test_path_pose, test_path_intrinsics]:
        os.makedirs(path, exist_ok=True)

    with open(cameras_path, 'r') as fin:
        cameras = json.load(fin)
        cameras_items = list(cameras.items())
    N_cameras = len(cameras.keys())

    all_indices = np.array(list(range(N_cameras)))
    np.random.shuffle(all_indices)
    test_indices = all_indices[:int(N_cameras * args.test_size)]
    train_indices = all_indices[int(N_cameras * args.test_size):]

    for i in tqdm(range(N_cameras), total=N_cameras):
        name = f'{i:06d}'
        if i in train_indices :
            # Copy image to /rgb
            shutil.copyfile(os.path.join(images_path, cameras_items[i][0]), os.path.join(train_path_rgb, name+'.png'))

            # Add pose
            with open(os.path.join(train_path_pose, name + '.txt'), 'w') as fout:
                fout.write(' '.join(map(str, cameras_items[i][1]['W2C'])))

            # Add intrinsics
            with open(os.path.join(train_path_intrinsics, name + '.txt'), 'w') as fout:
                fout.write(' '.join(map(str, cameras_items[i][1]['K'])))

        else:
            # Copy image to /rgb
            shutil.copyfile(os.path.join(images_path, cameras_items[i][0]), os.path.join(test_path_rgb, name+'.png'))

            # Add pose
            with open(os.path.join(test_path_pose, name + '.txt'), 'w') as fout:
                fout.write(' '.join(map(str, cameras_items[i][1]['W2C'])))

            # Add intrinsics
            with open(os.path.join(test_path_intrinsics, name + '.txt'), 'w') as fout:
                fout.write(' '.join(map(str, cameras_items[i][1]['K'])))








