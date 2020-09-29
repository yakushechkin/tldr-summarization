#### Author: Dmitrii Iakushechkin

import h5py
import os
import errno
import json
import jsonlines
import numpy as np
import argparse


def convertSciTLDRforPacSum(path, task, mode):
    '''
    Args:
        task: ['A', 'AIC', 'FullText']
        mode: ['train','test','dev']
    '''

    tldr_list = []
    with jsonlines.open(os.path.join(path, 'SciTLDR-{}'.format(task), '{}.jsonl'.format(mode))) as reader:
        print('1. {} dataset is loaded'.format(mode))
        counter = 0
        counter_tldrs = 0

        # for each article
        for obj in reader:
            counter += 1
            obj_pacsum = dict()
            obj_pacsum['article'] = obj['source']

            # not unique output
            if isinstance(obj['target'], list):
                for item in obj['target']:
                    counter_tldrs += 1
                    obj_pacsum['abstract'] = [item]
                    s = json.dumps(obj_pacsum).encode('UTF-8')
                    tldr_list.append(s)
            # unique output
            elif isinstance(obj['target'], str):
                counter_tldrs += 1
                obj_pacsum['abstract'] = [obj['target']]
                s = json.dumps(obj_pacsum).encode('UTF-8')
                tldr_list.append(s)
            # unknown type
            else:
                print('Unknown type of target data.')

        print('2. The {} dataset has {} articles'.format(mode, counter))
        print('3. The {} dataset has {} TLDRs'.format(mode, counter_tldrs))
    arr = np.array(tldr_list)
    print('Array is ready for saving!')
    return arr


def saveSciTLDRforPacSum(path, arr, task, mode):
    '''
    Function for saving an array with bytes as a h5df file.
    Args:
        task: ['A', 'AIC', 'FullText']
        mode: ['train','test','dev']
    '''
    path = os.path.join(path, 'SciTLDR-{}'.format(task), 'forPacSum')
    try:
        os.mkdir(path)
    except OSError as err:
        if err.errno == errno.EEXIST:
            pass
        else:
            raise

    with h5py.File(os.path.join(path, 'tldr_{}.h5df'.format(mode)), 'w') as f:
        f.create_dataset("dataset", data=arr, dtype=h5py.string_dtype(encoding='ascii'))


def SciTLDRforPacSum(path,task,mode):
    '''
     Function for running the data conversion and saving a data to the folder 'forPacSum'
     '''

    arr = convertSciTLDRforPacSum(path,task,mode)
    saveSciTLDRforPacSum(path,arr,task,mode)
    print("The {} dataset for {} task is saved to the folder 'forPacSum'. \n".format(mode,task))


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--datadir', type=str,
                        help='the path to the ../scitldr/SciTLDR-Data/ folder')
    parser.add_argument('--task', type=str, choices = ['A', 'AIC', 'FullText'], help='A, AIC or FullText')

    args = parser.parse_args()

    # Path check
    if not os.path.exists(args.datadir):
        print('{} does not exist'.format(args.datadir))

    SciTLDRforPacSum(args.datadir, args.task,'test')
    SciTLDRforPacSum(args.datadir, args.task,'train')
    SciTLDRforPacSum(args.datadir, args.task,'dev')




