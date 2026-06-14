import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import pytest

from mosaicshade import mosaic


@pytest.fixture
def data():
    return pd.DataFrame({
        "A": ["x", "x", "y", "y"],
        "B": ["m", "n", "m", "n"],
        "Freq": [10, 20, 30, 40],
    })


def test_returns_figure_and_axes(data):
    fig, ax = mosaic(data, freq="Freq")

    assert fig is ax.figure
    assert ax.get_xlabel() == "A"
    assert ax.get_ylabel() == "B"

    plt.close(fig)


def test_accepts_tuple_dims(data):
    fig, ax = mosaic(data, freq="Freq", dims=("A", "B"))
    plt.close(fig)


def test_accepts_numeric_string_frequencies(data):
    data["Freq"] = data["Freq"].astype(str)

    fig, ax = mosaic(data, freq="Freq")
    plt.close(fig)


def test_missing_combination_is_allowed():
    data = pd.DataFrame({
        "A": ["x", "x", "y"],
        "B": ["m", "n", "m"],
        "Freq": [10, 20, 30],
    })

    fig, ax = mosaic(data, freq="Freq")
    plt.close(fig)


@pytest.mark.parametrize("freq", [
    [-1, 2, 3, 4],
    [float("nan"), 2, 3, 4],
    [float("inf"), 2, 3, 4],
    [0, 0, 0, 0],
])
def test_invalid_frequencies_raise(data, freq):
    data["Freq"] = freq

    with pytest.raises(ValueError):
        mosaic(data, freq="Freq")


def test_missing_dimension_values_raise(data):
    data.loc[0, "A"] = None

    with pytest.raises(ValueError):
        mosaic(data, freq="Freq")


def test_invalid_dims_type_raises(data):
    with pytest.raises(TypeError):
        mosaic(data, freq="Freq", dims=123)


def test_properties_cannot_be_overridden(data):
    with pytest.raises(TypeError):
        mosaic(data, freq="Freq", properties=lambda key: {})


def test_invalid_labelizer_raises(data):
    with pytest.raises(TypeError):
        mosaic(data, freq="Freq", labelizer="values")


def test_custom_labelizer(data):
    fig, ax = mosaic(
        data,
        freq="Freq",
        labelizer=lambda key: "",
    )
    plt.close(fig)


def test_invalid_gap_length_raises(data):
    with pytest.raises(ValueError):
        mosaic(data, freq="Freq", gap=[0.01])
