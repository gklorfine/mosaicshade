# ==================================================
# The below TODOs are listed in order of priority:
# ==================================================
# [ ] TODO: Allow input other than just type = pd.DataFrame. Goal is to take same types as statsmodels function
# [ ] TODO: Arguments for statistical models other than independence
# [ ] TODO: Arguments for shading limits (e.g., changing from 2-4 for light and 4+ for dark)
# [ ] TODO: Different labeling schemes (e.g., label cells with numeric residual)
# [ ] TODO: Generalize to n-dimensions (currently at 4)
# ==================================================

## Setup
import pandas as pd
import numpy as np
from statsmodels.graphics.mosaicplot import mosaic as sm_mosaic
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches

## Create same colours from R
BLUE_FULL  = mcolors.hsv_to_rgb([2/3, 1.0, 1.0])
BLUE_MID   = mcolors.hsv_to_rgb([2/3, 0.5, 1.0])
WHITE      = mcolors.hsv_to_rgb([0,   0.0, 1.0])
RED_MID    = mcolors.hsv_to_rgb([0,   0.5, 1.0])
RED_FULL   = mcolors.hsv_to_rgb([0,   1.0, 1.0])

def mosaic(df : pd.DataFrame, freq : str, dims : list | None = None, **kwargs):
    """
    Wrapper for statsmodels.graphics.mosaicplot.mosaic that implements residual-based shading.

    Parameters
    ----------
    df : pd.DataFrame
        Data to plot
    dims : list
        Two to four dimensions to use for the mosaic. Defaults to all dimensions except the frequency column
    freq : str
        The frequency column of your DataFrame
    **kwargs
        Any remaining keyword arguments passed to statsmodels.graphics.mosaicplot.mosaic
    """
    title = kwargs.pop('title', None)

    if dims is None: dims = [col for col in df.columns if col != freq]

    grouped_counts = df.groupby(dims, observed=True)[freq].sum()

    # Include every combination of the observed category levels. Missing
    # combinations are valid zero-count cells in the contingency table.
    levels = [
        grouped_counts.index.get_level_values(i).unique()
        for i in range(len(dims))
    ]
    index = pd.MultiIndex.from_product(levels, names=dims)
    counts = grouped_counts.reindex(index, fill_value=0)

    # Reshape the complete, consistently ordered counts into an n-D array.
    shape = [len(level) for level in levels]
    obs = counts.to_numpy().reshape(shape)

    ## Calculate Pearson residuals. Use model of independence for this example
    _, _, _, expected = chi2_contingency(obs)
    std_res_array = (obs - expected) / np.sqrt(expected)

    # Wrap back into a MultiIndex Series so residuals[k] lookup works
    std_res = pd.Series(std_res_array.ravel(), index=index)

    ## Construct mosaic!

    def Friendly_shading(residuals):
        def res_color(k):

            res = residuals.loc[k]

            edgecolor = BLUE_FULL if res >= 0 else RED_FULL
            linestyle = '-' if res >= 0 else '--'

            if res >= 4:      facecolor = BLUE_FULL
            elif res >= 2:    facecolor = BLUE_MID
            elif res > -2:    facecolor = 'WHITE'
            elif res > -4:    facecolor = RED_MID
            else:             facecolor = RED_FULL

            return {'facecolor': facecolor, 'linestyle': linestyle, 'edgecolor': edgecolor}
        return res_color

    # With values as labels
    def labeling_values(k): 
        return str(counts.loc[k])
    
    # Gaps b/w rectangles
    gap_list = [.01,.01]
    for i in range(2, len(dims)): gap_list.append(.05)

    # Make plot in way that allows black border removal
    fig, rects = sm_mosaic(
        counts, 
        properties=Friendly_shading(std_res), labelizer=labeling_values, 
        gap=gap_list, #[.01] * len(dims),
        **kwargs
    )

    right_label_texts = []
    if len(dims) > 2:
        ax = fig.axes[0]
        right_edge = max(x + w for x, y, w, h in rects.values())
        for level in range(2, len(dims)):
            best_tiles = {}
            for k, (x, y, w, h) in rects.items():
                key = (k[0], k[level])
                if level % 2 == 0:   # horizontal split → find topmost tile
                    if key not in best_tiles or (y + h) > (best_tiles[key][1] + best_tiles[key][3]):
                        best_tiles[key] = (x, y, w, h)
                else:                 # vertical split → find rightmost tile
                    if key not in best_tiles or (x + w) > (best_tiles[key][0] + best_tiles[key][2]):
                        best_tiles[key] = (x, y, w, h)

            for (_, label), (x, y, w, h) in best_tiles.items():
                if level % 2 == 0:
                    ax.text(x + w/2, y + h + 0.01, label,
                            ha='center', va='bottom', clip_on=False,
                            fontsize=ax.xaxis.get_ticklabels()[0].get_fontsize() if ax.xaxis.get_ticklabels() else 10)
                elif np.isclose(x + w, right_edge):
                    right_label_texts.append(
                        ax.text(x + w + 0.01, y + h/2, label,
                                ha='left', va='center', rotation=90, clip_on=False,
                                fontsize=ax.xaxis.get_ticklabels()[0].get_fontsize() if ax.xaxis.get_ticklabels() else 10)
                    )


    # Remove black border, axes ticks
    for ax in fig.axes:
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_xlim(-0.01, 1.01)
        ax.set_ylim(-0.01, 1.01)
        ax.tick_params(length=0, labeltop=False)

    # Make bold labels
    ax = fig.axes[0]
    ax.set_xlabel(dims[0], fontweight='bold')
    ax.set_ylabel(dims[1], fontweight='bold')
    ax.tick_params(axis='y', labelrotation=90)
    if len(dims) > 2:
        ax.text(0.5, 1.05, dims[2], transform=ax.transAxes,
                ha='center', va='bottom', fontweight='bold')
    if len(dims) > 3:
        right_axis_labels = set(df[dims[3]].astype(str))
        fig.canvas.draw()
        plot_right = ax.get_window_extent().x1
        for candidate_ax in fig.axes:
            for text in candidate_ax.get_yticklabels():
                display_position = text.get_transform().transform(text.get_position())
                if text.get_text() in right_axis_labels and display_position[0] >= plot_right:
                    right_label_texts.append(text)

        for text in dict.fromkeys(right_label_texts):
            display_position = text.get_transform().transform(text.get_position())
            _, axes_y = ax.transAxes.inverted().transform(display_position)
            text.set_transform(ax.transAxes)
            text.set_position((1.01, axes_y))
            text.set_rotation(90)
            text.set_rotation_mode('anchor')
            text.set_ha('center')
            text.set_va('top')
        ax.text(1.06, 0.5, dims[3], transform=ax.transAxes,
                ha='left', va='center', rotation=90, fontweight='bold')
    
    # Title
    if title: fig.suptitle(title)

    # Create legend
    legend_items = []

    max_res = np.max(std_res)
    if max_res >= 4:
        legend_items.append(
            mpatches.Patch(
                facecolor=BLUE_FULL,
                label=f' 4.0 to  {max_res:.1f}',
                edgecolor=BLUE_FULL, linestyle='-'
            )
        )

    legend_items.extend([
        mpatches.Patch(
            facecolor=BLUE_MID, 
            label=' 2.0 to  4.0', 
            edgecolor=BLUE_FULL, linestyle='-'
        ),
        mpatches.Patch(
            facecolor='WHITE', 
            label=' 0.0 to  2.0', 
            edgecolor=BLUE_FULL, linestyle='-'
        ),
        mpatches.Patch(
            facecolor='WHITE', 
            label='-2.0 to  0.0', 
            edgecolor=RED_FULL, linestyle='--'
        ),
        mpatches.Patch(
            facecolor=RED_MID, 
            label='-4.0 to -2.0', 
            edgecolor=RED_FULL, linestyle='--'
        ),
    ])

    min_res = np.min(std_res)
    if min_res <= -4:
        legend_items.append(
            mpatches.Patch(
                facecolor=RED_FULL,
                label=f'{min_res:.1f} to -4.0',
                edgecolor=RED_FULL, linestyle='--'
            )
        )

    fig.axes[0].legend(handles=legend_items, title='Pearson\nresiduals:',
                    bbox_to_anchor=(1.18, 0.5), loc='center left', frameon=False)
    
    plt.tight_layout()
    
    return fig, ax