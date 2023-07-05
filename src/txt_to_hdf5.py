#!/usr/bin/env python3

import os
from pathlib import Path
import argparse
import numpy as np
import pandas as pd

from text_embedder import read_pub, read_pubs_in_dir, embeddings_from_pubs, write_hdf5

def try_to_read_dir(dir_path: str) -> str:
    # a quick function for argparse to check if given arg is a readable dir
    if not os.path.isdir(dir_path) or not os.access(dir_path, os.R_OK):
        raise argparse.ArgumentTypeError("The directory " + dir_path + " does "
                                         + "not exist or is not readable!")
    return dir_path

def try_to_read_file(file_path: str) -> str:
    # a quick function for argparse to check if given arg is a readable file
    if not os.path.isfile(file_path) or not os.access(file_path, os.R_OK):
        raise argparse.ArgumentTypeError("The file " + file_path + " does not "
                                         + "exist or is not readable!")
    return file_path

def try_to_write_file_if_exists(file_path: str) -> str:
    # a quick function for argparse to check if given arg is a writable file
    if os.path.isfile(file_path) and not os.access(file_path, os.W_OK):
        raise argparse.ArgumentTypeError("The file " + file_path + " is not "
                                         + "writable!")
    return file_path

def main():
    parser = argparse.ArgumentParser(
        description='Compute embeddings for lists of publications.')
    parser.add_argument('-d', '--dir_path', type = try_to_read_dir,
                        metavar = 'DIR', 
                        help = 'Directory containing files with chunks '
                        + '(.txt). The files should have the format '
                        + '<chunk_id>.txt. For publications it is '
                        + '<author_id>.txt, which contain publication lists. '
                        + 'For examination regulations the ID is a string '
                        + 'which identifies the short name of the original '
                        + ' file with an index for the chunk number.')
    parser.add_argument('-u', '--update', nargs = '+', type = try_to_read_file,
                        metavar='FILE',
                        help = 'Update existing embeddings in hdf5 file with '
                        +' the texts in the specified file(s). The '
                        + ' names of the files must again have format '
                        + '<chunk_id>.txt. If the chunk ID already exists in'
                        + ' the HDF5 file, the corresponding embedding will be'
                        + ' overwritten, if not, it will be added to the '
                        + 'dataset. This option is mutually exclusive with '
                        + '\'--dir_path\'.')
    parser.add_argument('-f', '--hdf5_file', required = True,
                        type = try_to_write_file_if_exists,
                        help = 'Output file in hdf5 format with data sets: ' 
                        + 'embeddings: 2-dim pandas dataFrame with the '
                        + 'computed embeddings. \nids: 1-dim pandas DataFrame '
                        + 'containing the ids for each embedding.')
    parser.add_argument('-m', '--mode', required = True,
                        type = str,
                        help = 'Defines what type of texts are used to compute'
                        + ' the embeddings. Either type \'p\' or '
                        + '\' puplications\' when using publcations lists or '
                        + 'type \'r\' or \'regulations\' if examination '
                        + ' regulations are used as text files.')
    args = parser.parse_args()

    # either compute new embedding or update existing embedding
    if args.dir_path == args.update:
        print("ERROR: You need to specifiy exactly one of the 2 arguments: " 
              + "'--dir_path' or '--update'.")
        exit(1)
    # check if file to update exists
    if args.update and not os.path.isfile(args.hdf5_file):
        print("ERROR: File", args.hdf5_file, "does not exist! Please specify"
            + " a HDF5 file to update.")
    # check if the mode of the files is defined properly:
    #TODO hshsh 
    files_are_pubs = True
    #examination_regulations = False

    if(files_are_pubs):
        # compute embeddings for publications in directory
        if args.dir_path:
            # read publications and compute embeddings
            pubs, author_ids = read_pubs_in_dir(args.dir_path)
            embeddings = embeddings_from_pubs(pubs)
            # write data to hdf5 file
            write_hdf5(args.hdf5_file, embeddings, author_ids)
        
        else:  # update existing embedding
            author_ids = []
            pubs = []
            for file_path in args.update:
                # check if file names have format <author_id>.txt
                file_stem = Path(file_path).stem
                try:
                    id = int(file_stem)
                except ValueError:
                    print("ERROR: The name of file \"", file_path, "\" does not " 
                    + "have format <author_id>.txt!")
                    exit(1)
                # read if yes
                author_pubs = read_pub(file_path)
                author_ids.append(id)
                pubs.append(author_pubs)
            # compute embeddings            
            embeddings = pd.DataFrame(embeddings_from_pubs(pubs))
            author_ids = pd.DataFrame(author_ids)
            # update hdf5 file
            write_hdf5(args.hdf5_file, embeddings, author_ids, update = True)

    exit(0)

if __name__ == "__main__":
    main()
