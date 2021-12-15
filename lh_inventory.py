"""
Utility to inventorize SteamVR (Lighthouse) tracked devices from 
their JSON config files. 
"""

import os
import glob
import json
import pprint
import argparse

import pandas as pd

LH_PATH = os.environ['ProgramFiles(x86)'] + '\\Steam\\config\\lighthouse'
SEP = ';'

if __name__ == '__main__':

    # Parse command line arguments
    desc = 'Tool to create a list (CSV) of all tracked Lighthouse devices (e.g. HMD, controllers, Vive Trackers) known to SteamVR. '
    desc += 'Alternatively, compiles such a list from JSON config files downloaded from SteamVR devices using lighthouse_console.exe.'
    ap = argparse.ArgumentParser(description=desc)
    ap.add_argument('-j', '--json_files', default=None, help='JSON files or folders to convert, e.g. "folder/*.json"')
    ap.add_argument('-o', dest='output_file', default=None, metavar='output_file', help='Ouput file (default: steamvr_inventory.tsv)')
    ap.add_argument('-u', dest='update', action='store_true', default=False, help='Update output file instead of overwriting')
    ap.add_argument('-d', dest='debug', action='store_true', default=False, help='If set, print out JSON and MAT file structures')
    options = ap.parse_args()

    # Set default options
    if options.output_file is None:
        output_file = 'steamvr_inventory.csv'
    else:
        output_file = options.output_file 
    if options.json_files is None:
        print('Reading local lighthouse config at {:s}...\n'.format(LH_PATH))
        jfiles = glob.glob(LH_PATH + '\\**\\*.json', recursive=True)
    else:
        if os.path.isdir(options.json_files):
            print('Reading JSON config files from {:s}...\n'.format(options.json_files))
            jfiles = glob.glob(os.path.join(options.json_files, '**\\*.json'), recursive=True)
        else:
            jfiles = glob.glob(options.json_files)

    df = []

    for j in jfiles:
        if os.path.split(j)[1] == 'lighthousedb.json':
            continue # Skip base station config db

        with open(j, 'rb') as f:
            data = json.load(f)
            basename = os.path.splitext(os.path.split(j)[-1])[0]
            if options.debug:
                print('JSON INPUT: {:s}'.format(j))
                pprint.pprint(data)
                print('\n\n')

            # Drop every key that doesn't contain a single value
            dropped = []
            for k in data.keys():
                if type(data[k]) in (dict, tuple, list):
                    dropped.append(k)
            for k in dropped:
                del data[k]

            # Add file name for easy reference
            data['_input_file'] = basename
            try:
                print('{:s}: {:s}, {:s} ({:s})'.format(data['device_serial_number'],
                                                    data['manufacturer'],
                                                    data['model_number'],
                                                    data['device_class']))
            except:
                print(' ') # don't break if one of above fields isn't defined
        
        df.append(data)

    df = pd.DataFrame(df)
    if options.update and os.path.isfile(output_file):
        df_old = pd.read_csv(output_file, sep=SEP, index_col=False)
        df = df.merge(df_old, how='outer')
    
    if options.debug:
        print(df)

    df.sort_values(['device_class']).to_csv(output_file, sep=SEP, index=False)
    print('\nSaved {:d} devices to {:s}.'.format(df.shape[0], output_file))
