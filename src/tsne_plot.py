#!/usr/bin/env python3

import os
import argparse
import h5py
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn  as sns


def file_readable(arg):
    if not os.path.isfile(arg) or not os.access(arg, os.R_OK):
        raise argparse.ArgumentTypeError("The file " + arg + "does not exist "
                                         + "or is not readable!")
    return arg

def get_affiliation_and_palette(authors: pd.DataFrame,
                                author_ids: np.ndarray,
                                affiliation_map: pd.DataFrame, 
                                affiliation: str) -> tuple[list[str], dict]:
    """
    Get affiliations of autors by ID and generate color palette for the
    affiliations

    Args:
        authors (pandas.DataFrame): Table containing at least author ids and 
            their faculties and institutes.
        author_ids (numpay.ndarray): List of author ids for which to get the 
            affiliations.
        affiliation_map (pandas.DataFrame): Table with all possible 
            faculties or institutes.
        affiliation (str): Which affiliation to use - faculty or institute.

    Returns:
        affil (list[str]): List of affiliations for author IDs.
        pal (dict): Color palette for the affiliations.
    """

    # get affiliations of authors by ID
    affil = authors.loc[authors['id'].isin(author_ids), affiliation].to_list()
    # if institutes, switch long names of institutes to short names
    if affiliation == 'institute':
        mapping = dict(zip(affiliation_map['institute_long'], 
                           affiliation_map['institute_short']))

        affil_ = [mapping[item] for item in affil]
        affil = affil_
        affil_uniq = affiliation_map['institute_short'].to_list()
    else:
        affil_uniq = affiliation_map['faculty'].to_list()
    
    # generate color palette
    num_col = len(affil_uniq)  # number of colors
    colors = sns.color_palette("hls", num_col).as_hex()  # get colors
    pal = dict(zip(affil_uniq, colors))  # color palette for plot
    
    return affil, pal


def compute_tsne(X: np.ndarray, 
                 pca_reduction: bool = False, 
                 pca_components: int = 50,
                 tsne_perplexity: float = 30.0) -> np.ndarray:
    """ 
    Compute t-SNE for embeddings 
    
    Args:
        X (numpy.ndarray): Embeddings to transform
        pca_reduction (bool): If True, a PCA is performed before the t-SNE to 
            reduce computation resources. Default: True.
        pca_components (int): Number of components to keep, when PCA is 
            performed, i.e. dimension of the result. Default: 50.
        tsne_perplexity (float): Number of nearest neighbors that is used in 
            other manifold learning algorithms, must be less than the number of
            samples. Default: 30.0.

    Returns:
        tsne_result (numpy.ndarray): t-SNE transformed data.
    """
    # ada dimensions: 1536
    if pca_reduction:
        # build PCA, reduce to dim size pca_components
        pca = PCA(n_components = pca_components)
        pca_result = pca.fit_transform(X)  # fit model and apply dim reduction
        X = pca_result

    tsne = TSNE(perplexity = tsne_perplexity)  # perplexity = knn
    tsne_result = tsne.fit_transform(X)  # fit model and apply dim reduction

    return tsne_result

def tsne_plot(X: np.ndarray, 
              affiliation: list[str],
              palette: dict):
    """
    Plot t-SNE 

    Args:
        X (numpy.ndarray): Result of the t-SNE transformation.
        affiliation (list[str]): Containing the institutes or 
            faculties corresponding to the data points. This decides how to 
            color the points in the plot. 
        palette (dict): Color palette for the plot. Specifies which color to 
            use for which institute or faculty.

    Returns:
        matplotlib.figure.Figure: Figure of the plot.
    """

    plt.figure(figsize=(15,15))
    plot = sns.scatterplot(
        x = X[:, 0], y = X[:, 1],
        hue = affiliation,
        palette = palette,
        legend = "full",
        alpha = 0.75
    )
    
    return plot.get_figure()


def main():
    parser = argparse.ArgumentParser(
        description='Visualize the embeddings of publications with a t-SNE '
                    + 'plot.')
    parser.add_argument('embed_file', type = file_readable,
                        help = 'hdf5 file with embeddings.')
    parser.add_argument('author_file', type = file_readable,
                        help = 'File with table containing information about '
                        + 'the authors, like ID, fculty, and institute.')
    parser.add_argument('affiliation_map', type = file_readable,
                        help = 'File with table containig all possible '
                        + 'faculties/institutes.')
    parser.add_argument('-o', '--outfile', default = 'tsne_plot',
                        help = 'Stem for output file to save plot.')
    parser.add_argument('--format', default = 'png', 
                        choices = ['png', 'pdf', 'svg'],
                        help = 'Format for plot.')
    parser.add_argument('--pca', action = 'store_true',
                        help = 'Perform a PCA before the t-SNE.')
    parser.add_argument('--pca_components', type = int, default = 50,
                        help = 'Number of components to keep after performing'
                        + ' the PCA')
    parser.add_argument('--affiliation', default = 'faculty', 
                        choices = ['institute', 'faculty'],
                        help = 'Decides after which fashion to color the ' 
                        + 'plot.')
    args = parser.parse_args()
    
    outfile = args.outfile + '.' + args.format

    # read data
    with h5py.File(args.embed_file, 'r') as f_in:
        pub_embedding = f_in['publication_embedding'][:]
        author_ids = f_in['author_ids'][:]
    authors = pd.read_table(args.author_file, delimiter = '\t')
    affiliation_map = pd.read_table(args.affiliation_map, delimiter = '\t')

    # perplexity for tsne needs to be smaller than number of data points
    k = 30.0 if len(author_ids) > 30 else float(len(author_ids) - 1)
    # pca components needs to be <= min(n_samples, n_features)
    pca_components = args.pca_components \
        if min(pub_embedding.shape) >= args.pca_components \
        else min(pub_embedding.shape)
    # transform embeddings
    tsne_result = compute_tsne(pub_embedding, pca_reduction = args.pca, 
                               pca_components = pca_components, 
                               tsne_perplexity = k)
    
    # get affiliations and color palette
    affiliation, palette = get_affiliation_and_palette(authors, author_ids, 
                                                       affiliation_map, 
                                                       args.affiliation)
    # plot
    fig = tsne_plot(tsne_result, affiliation, palette)  
    fig.savefig(outfile, format = args.format)
    plt.show()
       
    exit(0)


if __name__ == "__main__":
    main()