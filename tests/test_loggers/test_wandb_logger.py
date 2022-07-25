from unittest.mock import call
from unittest.mock import patch

import pytest

from etna.loggers import WandbLogger
from etna.loggers import tslogger as _tslogger


@pytest.fixture()
def tslogger():
    _tslogger.loggers = []
    return _tslogger


@patch("etna.loggers.wandb_logger.wandb")
def test_wandb_logger_log(wandb, tslogger):
    wandb_logger = WandbLogger()
    tslogger.add(wandb_logger)
    tslogger.log("test")
    tslogger.log({"MAE": 0})
    tslogger.log({"MAPE": 1.5})
    calls = [
        call({"MAE": 0}),
        call({"MAPE": 1.5}),
    ]
    wandb.init.return_value.log.assert_has_calls(calls)
