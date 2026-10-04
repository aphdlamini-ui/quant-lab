import pytest

from quant_lab.config import (
    daily_vol_usd,
    liquidity_cap_fraction,
    load_mandate,
    max_position_usd,
)


@pytest.fixture
def m():
    return load_mandate()


def test_sleeve_gross_adds_to_target(m):
    assert sum(m["gross"]["sleeves"].values()) == pytest.approx(m["gross"]["target"])


def test_liquidity_fraction(m):
    assert liquidity_cap_fraction(m) == pytest.approx(0.04615, abs=1e-4)


def test_liquidity_binds_at_adv_floor(m):
    assert max_position_usd(m, 45e6) == pytest.approx(2.077e6, rel=0.01)


def test_name_cap_binds_for_liquid_names(m):
    assert max_position_usd(m, 200e6) == pytest.approx(2.25e6)


def test_daily_vol(m):
    assert daily_vol_usd(m) == pytest.approx(472_000, rel=0.01)


def test_stops_ordered(m):
    d = m["drawdown"]
    assert d["alert"] <= d["governor_start"] < d["governor_end"] < d["soft_stop"] < d["hard_stop"]
