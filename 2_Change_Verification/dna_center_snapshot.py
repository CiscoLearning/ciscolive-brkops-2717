#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pyATS sample script for taking a snapshot of the network and comparing the
state with an earlier snapshot.

Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import os
import json

from pyats import topology
from genie.utils.diff import Diff

__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

TESTBED = topology.loader.load('testbed.yaml')
DEVICE = TESTBED.devices['dnac']
URL = '/dna/intent/api/v1/interface'
PRE_SNAPSHOT_DIR = 'pre-snapshot'
POST_SNAPSHOT_DIR = 'post-snapshot'

def get_snapshot(device, url, output_folder):
    '''
    Function to get a snapshot and place it to pre- or post-snapshot
    folder for future use.
    '''
    snapshot = device.rest.get(url)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    with open(f'{output_folder}/snapshot.json', 'w', encoding="utf-8") as file:
        json.dump(snapshot.json(), file)
    print(f'Took a snapshot of {url} and saved it in folder {output_folder}')

def compare(pre_dir, post_dir):
    '''
    Function to compare the snapshots in pre_snapshot and post_snapshot
    folders.
    '''
    try:
        with open(f'{pre_dir}/snapshot.json', 'r', encoding="utf-8") as file:
            pre_snapshot = json.load(file)
        with open(f'{post_dir}/snapshot.json', 'r', encoding="utf-8") as file:
            post_snapshot = json.load(file)
    except:
        print('Reading the files did not succeed!')
        print('Make sure you first take the snapshots!')
        return

    diff = Diff(pre_snapshot, post_snapshot)
    diff.findDiff()

    print('The following differences were found:')
    print(diff)

if __name__ == '__main__':
    DEVICE.connect()
    while True:
        print("\n-----------")
        print("What do you want to do?")
        print("1. Take a pre-snapshot")
        print("2. Take a post-snapshot")
        print("3. Compare snapshots")
        print("4. Exit the program")

        selection = int(input("Your selection: "))
        print("-----------\n")
        if selection == 1:
            get_snapshot(DEVICE, URL, PRE_SNAPSHOT_DIR)
        elif selection == 2:
            get_snapshot(DEVICE, URL, POST_SNAPSHOT_DIR)
        elif selection == 3:
            compare(PRE_SNAPSHOT_DIR, POST_SNAPSHOT_DIR)
        elif selection == 4:
            print("Thank you for using the program!")
            DEVICE.rest.disconnect()
            break
        else:
            print("Not a valid option!")
