

<!-- README.md is generated from README.qmd. Please edit README.qmd. Make sure to place an HTML comment such as this one after every chunk of code... Quarto does not like us. -->

# MosaicShade <a href="https://github.com/gklorfine/mosaicshade"><img src="https://raw.githubusercontent.com/gklorfine/mosaicshade/main/images/logo.png" align="right" height="192" alt="MosaicShade logo"/></a>

[![PyPI
version](https://img.shields.io/pypi/v/mosaicshade.svg)](https://pypi.org/project/mosaicshade/)
[![Python
versions](https://img.shields.io/pypi/pyversions/mosaicshade.svg)](https://pypi.org/project/mosaicshade/)
[![Tests](https://github.com/gklorfine/mosaicshade/actions/workflows/tests.yml/badge.svg)](https://github.com/gklorfine/mosaicshade/actions/workflows/tests.yml)
[![Downloads](https://static.pepy.tech/badge/mosaicshade.png)](https://pepy.tech/project/mosaicshade)
[![License](https://img.shields.io/github/license/gklorfine/mosaicshade.png)](https://github.com/gklorfine/mosaicshade/blob/main/LICENSE)

## Overview

Implements residual-based shading for mosaic displays in Python.

Shading based on residuals offers a way of visualizing how your data
departs from a given statistical model. Currently, **MosaicShade** only
uses the model of independence (see [Limitations](#limitations)).

Colour and shading intensity respectively indicate the direction and
magnitude of residuals, making patterns of association between
categorical variables easier to identify.

**MosaicShade** extends
[`statsmodels.graphics.mosaicplot.mosaic`](https://www.statsmodels.org/stable/generated/statsmodels.graphics.mosaicplot.mosaic.html).
The shading scheme used was inspired by `shading_Friendly` from the
[**vcd**](https://cran.r-project.org/package=vcd) package in the
programming language [**R**](https://www.r-project.org/).

## Installation

Install MosaicShade from PyPI:

``` bash
python -m pip install mosaicshade
```

## Usage

Currently, data needs to be a `pd.DataFrame` to be accepted by the
`mosaic` function (see [Limitations](#limitations)). The below is a
made-up `pd.DataFrame` that will be used for subsequent examples:

``` python
import pandas as pd

df = pd.DataFrame({
    "Treatment": ["A", "A", "A", "A", "B", "B", "B", "B"],
    "Outcome": ["Good", "Good", "Bad", "Bad"] * 2,
    "Sex": ["Female", "Male"] * 4,
    "Freq": [20, 23, 3, 4, 2, 2, 10, 72]
})

df
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

|     | Treatment | Outcome | Sex    | Freq |
|-----|-----------|---------|--------|------|
| 0   | A         | Good    | Female | 20   |
| 1   | A         | Good    | Male   | 23   |
| 2   | A         | Bad     | Female | 3    |
| 3   | A         | Bad     | Male   | 4    |
| 4   | B         | Good    | Female | 2    |
| 5   | B         | Good    | Male   | 2    |
| 6   | B         | Bad     | Female | 10   |
| 7   | B         | Bad     | Male   | 72   |

</div>

<!-- Keep the following heading separate from the executable cell. -->

To make a mosaic from this data, we can call the `mosaicshade.mosaic`
function, specifying the frequency column with the `freq` argument:

``` python
import mosaicshade
import matplotlib.pyplot as plt

fig, ax = mosaicshade.mosaic(df, freq='Freq')
fig.savefig('images/mosaic_3dims.png', dpi=150, bbox_inches='tight')
plt.show() # Show the plot
```

![Three-dimensional shaded mosaic
plot](https://raw.githubusercontent.com/gklorfine/mosaicshade/main/images/mosaic_3dims.png)

<!-- Keep the following heading separate from the executable cell. -->

We can optionally select specific dimensions (columns) to use in this
plot, summing over those that are excluded:

``` python
fig, ax = mosaicshade.mosaic(
    df,
    freq='Freq',
    dims=['Treatment', 'Outcome']
)
fig.savefig('images/mosaic_2dims.png', dpi=150, bbox_inches='tight')
plt.show()
```

![Two-dimensional shaded mosaic
plot](https://raw.githubusercontent.com/gklorfine/mosaicshade/main/images/mosaic_2dims.png)

<!-- Keep the following heading separate from the executable cell. -->

Remaining keyword arguments from
[`statsmodels.graphics.mosaicplot.mosaic`](https://www.statsmodels.org/stable/generated/statsmodels.graphics.mosaicplot.mosaic.html)
also work (with the exception of the `properties` argument, as this is
used to perform the shading). For example, here is how you may add a
title to the above plot:

``` python
fig, ax = mosaicshade.mosaic(
    df,
    freq='Freq',
    dims=['Treatment', 'Outcome'],
    title='Shaded Mosaic'
)
fig.savefig('images/mosaic_title.png', dpi=150, bbox_inches='tight')
plt.show()
```

![Two-dimensional shaded mosaic plot with a
title](https://raw.githubusercontent.com/gklorfine/mosaicshade/main/images/mosaic_title.png)

## API

### `mosaicshade.mosaic(df, freq, dims=None, **kwargs)`

Used to construct mosaic displays. An extension of
[`statsmodels.graphics.mosaicplot.mosaic`](https://www.statsmodels.org/stable/generated/statsmodels.graphics.mosaicplot.mosaic.html)
that implements residual-based shading.

#### Parameters:

**df :** ***pd.Dataframe***

> The data to plot.

**freq :** ***str***

> The frequency column of your DataFrame.

**dims :** ***list\[str\] or tuple\[str, …\], optional***

> Two to four dimensions (column names) to use for the mosaic. Defaults
> to all dimensions except the frequency column.

**\*\*kwargs**

> Any remaining keyword arguments passed to
> [`statsmodels.graphics.mosaicplot.mosaic`](https://www.statsmodels.org/stable/generated/statsmodels.graphics.mosaicplot.mosaic.html).
> Note that the properties argument is managed by mosaicshade and cannot
> be changed.

#### Returns:

**fig :** (`matplotlib.figure.Figure`)

> The figure containing the mosaic plot.

**ax :** (`matplotlib.axes.Axes`)

> The axes containing the mosaic plot.

## Limitations

I am working to address these limitations in future versions. You are
also welcome to contribute to help in this regard (see the
[Contributing](#contributing) section below).

- Data input to the `mosaicshade.mosaic()` function must be of type
  `pd.DataFrame`
- Residuals are currently calculated assuming a model of mutual
  independence
- No way to adjust shading limits (e.g., changing from magnitude 2-4 for
  light and 4+ for dark)
- Only labelling scheme added so far is `labeling_values`
- Limited to 2-4 dimensions (i.e., 5+ dimensions are untested and
  currently blocked by the `mosaic` function)

## Contributing

Contributions, bug reports, and feature requests are welcome. Please
open an [issue](https://github.com/gklorfine/mosaicshade/issues) or
submit a pull request. Contributions addressing the above limitations
are especially appreciated.

## Citation

If you use MosaicShade, please cite the software using information found
in [`CITATION.cff`](CITATION.cff) or GitHub’s “**Cite this repository**”
menu.

## References

Friendly, M. (1994). Mosaic Displays for Multi-Way Contingency Tables.
*Journal of the American Statistical Association*, *89*(425), 190–200.
https://doi.org/10.1080/01621459.1994.10476460

Meyer, D., Zeileis, A., Hornik, K., & Friendly, M. (2024). *vcd:
Visualizing Categorical Data*. R package version 1.4-13.
<https://doi.org/10.32614/CRAN.package.vcd>

Zeileis, A., Meyer, D., & Hornik, K. (2007). Residual-based Shadings for
Visualizing (Conditional) Independence. *Journal of Computational and
Graphical Statistics*, *16*(3), 507-525.
<https://doi.org/10.1198/106186007X237856>

## License

MosaicShade is licensed under the GNU General Public License version 3
(GPL-3.0-only). See [LICENSE](LICENSE) for details.
