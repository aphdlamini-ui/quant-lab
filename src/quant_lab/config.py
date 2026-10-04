from pathlib import Path

import yaml

DEFAULT_PATH = Path(__file__).resolve().parents[2] / "config" / "mandate.yaml"


def load_mandate(path: Path = DEFAULT_PATH) -> dict:
    with open(path, encoding="utf-8-sig") as f:
        return yaml.safe_load(f)


def liquidity_cap_fraction(m: dict) -> float:
    """Max position as a fraction of 30-day ADV under the stressed 4-hour unwind rule."""
    liq = m["liquidity"]
    return (
        liq["participation"]
        * (1 - liq["stress_haircut"])
        * liq["window_hours"]
        / liq["session_hours"]
    )


def max_position_usd(m: dict, adv_usd: float) -> float:
    """Binding position limit in dollars: the lower of the name cap and the liquidity cap."""
    name_cap = m["positions"]["name_cap"] * m["pod"]["capital"]
    return min(name_cap, liquidity_cap_fraction(m) * adv_usd)


def daily_vol_usd(m: dict) -> float:
    return m["pod"]["capital"] * m["pod"]["vol_target"] / 252**0.5
