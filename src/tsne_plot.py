#!/usr/bin/env python3

import os
import argparse
import h5py
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn  as sns


def compute_tsne(X: np.ndarray, 
                 pca_reduction = True, 
                 pca_components = 50,
                 tsne_perplexity = 30.0) -> np.ndarray:
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
            samples. Default: 30.0.S

    Returns:
        tsne_result (numpy.ndarray): t-SNE transformed data.
    """
    # ada dimensions: 1536
    if pca_reduction:
        # build PCA, reduce to dim size pca_components
        pca = PCA(n_components = pca_components)
        pca_result = pca.fit_transform(X)  # fit model and apply dim reduction
        X = pca_result

    # perplexity = knn, n_job = how many parallel searches for knn
    tsne = TSNE(perplexity = tsne_perplexity, n_jobs = None) 
    tsne_result = tsne.fit_transform(X)  # fit model and apply dim reduction

    return tsne_result


def tsne_plot(X: np.ndarray, 
              color: np.ndarray):
    """
    Plot t-SNE 

    Args:
        X (numpy.ndarray): Result of the t-SNE transformation.
        color (numpy.ndarray): 1-dim containing the institutes or faculties 
            corresponding to the data points. This decides how to color the 
            points in the plot. 

    Returns:
        matplotlib.figure.Figure: Figure of the plot.
    """
    num_col = len(np.unique(color))  # number of colors
    plt.figure(figsize=(15,15))
    plot = sns.scatterplot(
        x = X[:, 0], y = X[:, 1],
        hue = color,
        palette = sns.color_palette("hls", num_col),
        legend = "full",
        alpha = 0.75
    )
    
    return plot.get_figure()


def main():
    parser = argparse.ArgumentParser(
        description='Visualize the embeddings of ...')
    parser.add_argument('infile', help = 'hdf5 file with embeddings')
    parser.add_argument('-o', '-outfile', default = 'tsne_plot',
                        help = 'Stem for outfile')
    parser.add_argument('--format', default = 'png', 
                        choices = ['png', 'pdf', 'svg'],
                        help = 'Format for outfile')
    parser.add_argument('--no_pca', action = 'store_true',
                        help = '')
    parser.add_argument('--pca_components', type = int, default = 50,
                        help = '')
    parser.add_argument('--affiliation', default = 'faculty', 
                        choices = ['institute', 'faculty'],
                        help = '')
    args = parser.parse_args()

    #### test if input is readable
    #### test if outfile is writable 
    outfile = args.outfile + args.format

    # read data
    with h5py.File(args.infile, 'r') as f_in:
        pub_embedding = f_in['pub_embedding'][:]
        affiliation = f_in['author_affiliation'][:]

    # transform embeddings and plot result
    tsne_result = compute_tsne(pub_embedding, pca_reduction = args.no_pca, 
                               pca_components = args.pca_components)
    color = affiliation[1]  ###### adjust
    fig = tsne_plot(tsne_result, color)  
    fig.savefig(outfile, format = args.format)
    plt.show()

    exit(0)


if __name__ == "__main__":
    main()