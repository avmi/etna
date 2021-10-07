from copy import deepcopy

import numpy as np

from etna.models import LinearPerSegmentModel
from etna.pipeline import Pipeline
from etna.transforms import AddConstTransform
from etna.transforms import DateFlagsTransform


def test_fit(example_tsds):
    """
    Test that Pipeline correctly transforms dataset on fit stage
    """
    original_ts = deepcopy(example_tsds)
    model = LinearPerSegmentModel()
    transforms = [AddConstTransform(in_column="target", value=10, inplace=True), DateFlagsTransform()]
    pipeline = Pipeline(model=model, transforms=transforms, horizon=5)
    pipeline.fit(example_tsds)
    original_ts.fit_transform(transforms)
    assert np.all(original_ts.df.values == pipeline.ts.df.values)


def test_forecast(example_tsds):
    """
    Test that the forecast from the Pipeline is correct
    """
    original_ts = deepcopy(example_tsds)

    model = LinearPerSegmentModel()
    transforms = [AddConstTransform(in_column="target", value=10, inplace=True), DateFlagsTransform()]
    pipeline = Pipeline(model=model, transforms=transforms, horizon=5)
    pipeline.fit(example_tsds)
    forecast_pipeline = pipeline.forecast()

    original_ts.fit_transform(transforms)
    model.fit(original_ts)
    future = original_ts.make_future(5)
    forecast_manual = model.forecast(future)

    assert np.all(forecast_pipeline.df.values == forecast_manual.df.values)