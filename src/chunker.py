#!/usr/bin/env python3

import os
import argparse
from pathlib import Path

def try_to_read_file(file_path: str) -> str:
    # a quick function for argparse to check if given arg is a readable file
    if not os.path.isfile(file_path) or not os.access(file_path, os.R_OK):
        raise argparse.ArgumentTypeError("The file " + file_path + "does not "
                                         + "exist or is not readable!")
    return file_path

def try_to_write_dir(dir_path: str) -> str:
    # a quick function for argparse to check if given arg is a writable dir
    if not os.path.isdir(dir_path) or not os.access(dir_path, os.W_OK):
        raise argparse.ArgumentTypeError("The directory " + dir_path + " does "
                                         + "not exist or is not writeable!")
    return dir_path

def get_indices_for_chunks(chunk_size: int,
                           overlap: int,
                           text_len: int) -> list[tuple[int]]:
    """
    Compute indices of chunks in text

    Args: 
        chunk_size (int): Number of characters per chunk
        overlap (int): Number of characters each chunk should overlap with the 
            next one
        text_len (int): Length of text that is to be cut in chunks
    
    Returns:
        chunks (list[tuple[int]]): A list of index tuples, where each index 
            tuple represents a chunk. The index tuples are half-open intervals 
            [start, end), i.e. the start position is included and the end 
            position is excluded. The indexing is 0-based.
    """
    i = 0  # index of chunk start
    indices = []

    while i + chunk_size < text_len:  
        indices.append((i, i + chunk_size))
        i = i + chunk_size - overlap

    # last chunk, has length <= chunk_len
    indices.append((i, text_len))  
    return indices

def text_to_chunks(indices: list[tuple[int]],
                   text: str) -> list[str]:
    """
    Cut text into chunks at indices

    Args:
        indices (list[tuple[int]]): A list of index tuples
        text (str): Text to cut into chunks

    Returns:
        chunks (list[str]): List of chunks, each chunk is represented by a 
            string
    """
    chunks = []
    for ind in indices:
        chunk = text[ind[0]:ind[1]]
        chunks.append(chunk)

    return chunks

def write_chunks_to_files(chunks: list[str],
                          dir_path: str,
                          file_stem: str):
    """
    Write chunks to files named after the file stem + chunk index

    Args:
        chunks (list[str]): List of chunks represented by strings
        dir_path (str): Path to output dir
        file_stem (str): File stem for output files
    """

    for i, chunk in zip(range(len(chunks)), chunks):
        file_path = dir_path + file_stem + '.' + str(i) + '.txt'  
        with  open(file_path, 'w') as f_out:
            f_out.write(chunk)

def main():
    parser = argparse.ArgumentParser(description = 'Cut text files into '
                        + ' chunks. The chunks of each input file are saved to'
                        + ' text files in a directory named after the input '
                        + 'file.')
    parser.add_argument('files', nargs = '+', type = try_to_read_file,
                        help = 'Plain text files.')
    parser.add_argument('-s', '--chunk_size', type = int, required = True,
                        help = 'Number of characters per chunk.')
    parser.add_argument('-o', '--overlap', type = int, default = 10,
                        help = 'Number of characters the chunks should '
                        + 'overlap.')
    parser.add_argument('-d', '--dir_path', type = try_to_write_dir, 
                        default = './',
                        help = 'Directory in which to save dirs and chunks.')
    parser.add_argument('-m', '--copy_meta', action = 'store_true',
                        help = 'Copies the meta file if it exists into the '
                        + 'chunks directory. The meta file has to have format '
                        + '<file_name.meta.txt>.')
    args = parser.parse_args()

    dir_path = os.path.join(args.dir_path, '')  # append '/' if not there
    for file in args.files:

        # read file
        with open(file, 'r') as f_in:
            text = f_in.read()

        # cut text into chunks
        indices = get_indices_for_chunks(args.chunk_size, args.overlap, 
                                         len(text))
        chunks = text_to_chunks(indices, text)

        # output dir
        file_stem = Path(file).stem
        outdir = dir_path + file_stem + '/'  # dir + file stem as output dir
        os.makedirs(outdir, exist_ok = True)  # create dir if it doesnt exist

        # create file with info data
        info_file = outdir + 'info.txt'
        info_data = "chunks generated from file: " + file + "\nchunk size: " \
            + str(args.chunk_size) + "\noverlap: " + str(args.overlap) + "\n"
        with open(info_file, 'w') as f_out:
            f_out.write(info_data)

        # copy meta file if -m and the meta file exists with specified format
        if args.copy_meta:
            meta_file_name = file_stem + '.meta.txt'
            meta_file = os.path.join(os.path.dirname(file), meta_file_name)
            if os.access(meta_file, os.R_OK) :
                with open(meta_file, 'r') as meta_in:
                    meta_data = meta_in.read()
            else:
                print(f'ERROR: Could not open the meta file {meta_file}.'
                      + 'Pleas make sure that the file exists and is accesable'
                      + ' or repeat the chunker without argument -m.')
                exit(1)

            meta_file = os.path.join(outdir, meta_file_name)
            with open(meta_file, 'w') as meta_out:
                meta_out.write(meta_data)

        # write chunks to files
        write_chunks_to_files(chunks, outdir, file_stem)

    exit(0)

if __name__ == "__main__":
    main()
