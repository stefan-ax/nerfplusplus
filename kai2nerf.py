"""
Input should be data/diamond/venus-rough-1/posed_images/kai_cameras_normalized.json
Outpout should be like data/tanks_and_temples/tat_training_Truck/*

"""

import json
import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transform Kai to Nerf')
    parser.add_argument('path', description='Path to where /images and kai_cameras.txt are.')
    args = parser.parse_args()

    cameras = None


