from unittest.mock import MagicMock

import numpy as np
import pytest

from etna.metrics import MAE
from etna.models.nn import RNN
from etna.transforms import StandardScalerTransform


@pytest.mark.parametrize("horizon", [8, 13])
def test_rnn_model_run_weekly_overfit_with_scaler(ts_dataset_weekly_function_with_horizon, horizon):
    """
    Given: I have dataframe with 2 segments with weekly seasonality with known future
    When: I use scale transformations
    Then: I get {horizon} periods per dataset as a forecast and they "the same" as past
    """

    ts_train, ts_test = ts_dataset_weekly_function_with_horizon(horizon)

    std = StandardScalerTransform(in_column="target")
    ts_train.fit_transform([std])

    encoder_length = 14
    decoder_length = 14
    model = RNN(
        input_size=1, encoder_length=encoder_length, decoder_length=decoder_length, trainer_params=dict(max_epochs=100)
    )
    future = ts_train.make_future(decoder_length, encoder_length)
    model.fit(ts_train)
    future = model.forecast(future, horizon=horizon)

    mae = MAE("macro")
    assert mae(ts_test, future) < 0.06


def test_rnn_make_samples(example_df):
    rnn_model = MagicMock()
    rnn_model.encoder_length = 8
    rnn_model.decoder_length = 4

    ts_samples = list(RNN.make_samples(rnn_model, df=example_df))
    first_sample = ts_samples[0]
    second_sample = ts_samples[1]

    assert first_sample["segment"] == "segment_1"
    assert first_sample["encoder_real"].shape == (rnn_model.encoder_length - 1, 1)
    assert first_sample["decoder_real"].shape == (rnn_model.decoder_length, 1)
    assert first_sample["encoder_target"].shape == (rnn_model.encoder_length - 1, 1)
    assert first_sample["decoder_target"].shape == (rnn_model.decoder_length, 1)
    np.testing.assert_equal(example_df[["target"]].iloc[: rnn_model.encoder_length - 1], first_sample["encoder_real"])
    np.testing.assert_equal(example_df[["target"]].iloc[1 : rnn_model.encoder_length], second_sample["encoder_real"])