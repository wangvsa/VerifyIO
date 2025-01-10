#!/usr/bin/python3

import os, sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LogNorm
import numpy as np
import warnings
warnings.filterwarnings('ignore')

SEMANTICS_NAMES= ['POSIX', 'Commit', 'Session', 'MPI-IO']

def remove_after_last_dash(column_name):
    parts = column_name.rsplit('-', 1)
    return parts[0]


def plot_multi_heat_map(file_paths):
    # install latex to use this
    #plt.rcParams.update({
    #    "text.usetex": True,
    #    "font.family": "Times Roman"
    #})
    title_fontsize = 14
    label_fontsize = 14
    tick_fontsize = 10

    fig = plt.figure(figsize=(12, 12))
    gs = gridspec.GridSpec(nrows=2, ncols=2, width_ratios=[1, 1])  # 2 rows, 2 columns with different widths

    # Define subplot positions
    ax1 = plt.subplot(gs[0, 0])  # Top left
    ax2 = plt.subplot(gs[1, 0])  # Bottom left
    ax3 = plt.subplot(gs[:, 1])  # Right column spanning both rows

    axes = [ax1, ax2, ax3]

    # Step 1: Calculate the global maximum value (vmax) across all datasets
    vmax = -np.inf
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        heatmap_data = df.set_index('test')[[
            'total_semantic_violation_POSIX',
            'total_semantic_violation_Commit',
            'total_semantic_violation_Session',
            'total_semantic_violation_MPI-IO',
        ]]
        vmax = max(vmax, heatmap_data.max().max())  # Find the global max across all files

    # Step 2: Generate heatmaps using the global vmax
    for i, file_path in enumerate(file_paths):
        file_name = os.path.basename(file_path).replace('.csv', '')
        df = pd.read_csv(file_path)

        heatmap_data = df.set_index('test')[[
            'total_semantic_violation_POSIX',
            'total_semantic_violation_Commit', 
            'total_semantic_violation_Session',
            'total_semantic_violation_MPI-IO', 
        ]]
        heatmap_data.index = heatmap_data.index.map(remove_after_last_dash)
        heatmap_data.columns = SEMANTICS_NAMES
        
        # Fill missing data
        heatmap_data.fillna(-1, inplace=True)

        # Mask zeros for separate color mapping
        masked_data = heatmap_data.copy()
        masked_data.replace(0, np.nan, inplace=True)  # Mask zeros for the heatmap
        grey_mask = heatmap_data == -1

        ax = axes[i]

        cmap = sns.color_palette("gist_heat_r", as_cmap=True)
        cmap.set_bad('green') 

        # Step 3: Use the global vmax for consistent coloring across subplots
        sns.heatmap(
            heatmap_data, 
            annot=True,      
            fmt='g',
            cmap=cmap,
            linewidths=0.5,
            norm=LogNorm(vmin=1, vmax=vmax),  # Use global vmax here
            cbar=False,
            annot_kws={'size': 10, 'weight': 'bold', 'color': 'white'},
            mask=masked_data.isna(), 
            ax=ax 
        )

        for t in ax.texts:
            if t.get_text() == '0':
                t.set_text('')
            if t.get_text() == '-1':
                t.set_text('')


        # Grey mask for missing data
        sns.heatmap(
            grey_mask, 
            annot=False,  
            cmap=sns.color_palette(['grey']), 
            linewidths=0.5,
            cbar=False,  # No color bar for grey mask
            mask=~grey_mask,  # Mask everything except -1 values
            ax=ax 
        )

        ax.set_title(f'{file_name}', fontsize=title_fontsize)
        ax.set_xlabel('consistency semantics', fontsize=label_fontsize)
        ax.set_ylabel('test case', fontsize=label_fontsize)
        ax.tick_params(axis='x', rotation=0, labelsize=tick_fontsize)
        ax.tick_params(axis='y', labelsize=tick_fontsize)
        ax.set_aspect('auto')

    # Create a single color bar for all subplots
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])  # Adjust color bar position
    sm = plt.cm.ScalarMappable(cmap=sns.color_palette("gist_heat_r", as_cmap=True), norm=LogNorm(vmin=1, vmax=vmax))
    fig.colorbar(sm, cax=cbar_ax, label='number of data races')

    plt.tight_layout(rect=[0, 0, 0.9, 1])
    plt.savefig('heatmap.png', dpi=800, bbox_inches='tight')


def plot_single_heat_map(file_path):

    #plt.rcParams.update({
    #    "text.usetex": True,
    #    "font.family": "Times Roman"
    #})
    title_fontsize = 14
    label_fontsize = 14
    tick_fontsize = 10

    # Read data
    df = pd.read_csv(file_path)
    heatmap_data = df.set_index('test')[[
        'total_semantic_violation_POSIX',
        'total_semantic_violation_Commit',
        'total_semantic_violation_Session',
        'total_semantic_violation_MPI-IO',
    ]]

    heatmap_data.index = heatmap_data.index.map(remove_after_last_dash)
    heatmap_data.columns = SEMANTICS_NAMES

    # Fill missing data
    heatmap_data.fillna(-1, inplace=True)

    # Mask zeros for separate color mapping
    masked_data = heatmap_data.copy()
    # replace 0 with nan; then later plot nan with green color
    masked_data.replace(0, np.nan, inplace=True)
    grey_mask  = heatmap_data == -1

    # Determine vmax
    vmax = heatmap_data.max().max()

    # Plot heatmap
    fig, ax = plt.subplots(figsize=(8, 6))
    cmap = sns.color_palette("gist_heat_r", as_cmap=True)
    cmap.set_bad('green')

    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt='g',
        cmap=cmap,
        linewidths=0.5,
        norm=LogNorm(vmin=1, vmax=vmax),
        cbar=False,
        annot_kws={'size': 10, 'weight': 'bold', 'color': 'white'},
        mask=masked_data.isna(),
        ax=ax
    )

    for t in ax.texts:
        if t.get_text() == '0':
            t.set_text('')
        if t.get_text() == '-1':
            t.set_text('')

    # Grey mask for missing data
    sns.heatmap(
        grey_mask,
        annot=False,
        cmap=sns.color_palette(['grey']),
        linewidths=0.5,
        cbar=False,
        mask=~grey_mask,
        ax=ax
    )

    # Set labels and title
    file_name = os.path.basename(file_path).replace('.csv', '')
    ax.set_title(f'{file_name}', fontsize=title_fontsize)
    ax.set_xlabel('consistency semantics', fontsize=label_fontsize)
    ax.set_ylabel('test case', fontsize=label_fontsize)
    ax.tick_params(axis='x', rotation=0, labelsize=tick_fontsize)
    ax.tick_params(axis='y', labelsize=tick_fontsize)

    # Create a color bar
    cbar = fig.colorbar(
        plt.cm.ScalarMappable(cmap=cmap, norm=LogNorm(vmin=1, vmax=vmax)),
        ax=ax,
        fraction=0.046,
        pad=0.04,
        label='number of data races'
    )

    plt.tight_layout()
    plt.savefig(f'{file_name}_heatmap.png', dpi=800, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    csv_files = sys.argv[1:]
    if len(csv_files) == 1:
        plot_single_heat_map(csv_files[0])
    else:
        plot_multi_heat_map(csv_files)
