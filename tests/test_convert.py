from collections import namedtuple

from metatrader5_wrapper._convert import model_from_namedtuple, models_from_namedtuples
from metatrader5_wrapper.positions.models import Position


def test_model_from_namedtuple_builds_model() -> None:
    raw_position = namedtuple(
        "RawPosition",
        [
            "ticket",
            "time",
            "time_msc",
            "time_update",
            "time_update_msc",
            "type",
            "magic",
            "identifier",
            "reason",
            "volume",
            "price_open",
            "sl",
            "tp",
            "price_current",
            "swap",
            "profit",
            "symbol",
            "comment",
            "external_id",
        ],
    )

    payload = raw_position(
        1,
        1_700_000_000,
        1_700_000_000_000,
        1_700_000_010,
        1_700_000_010_000,
        0,
        42,
        99,
        0,
        0.5,
        1.1,
        1.09,
        1.12,
        1.101,
        0.0,
        12.5,
        "EURUSD",
        "demo",
        "external",
    )

    result = model_from_namedtuple(Position, payload)

    assert result.ticket == 1
    assert result.symbol == "EURUSD"
    assert result.profit == 12.5


def test_models_from_namedtuples_builds_list() -> None:
    raw_position = namedtuple(
        "RawPosition",
        [
            "ticket",
            "time",
            "time_msc",
            "time_update",
            "time_update_msc",
            "type",
            "magic",
            "identifier",
            "reason",
            "volume",
            "price_open",
            "sl",
            "tp",
            "price_current",
            "swap",
            "profit",
            "symbol",
            "comment",
            "external_id",
        ],
    )

    payloads = [
        raw_position(
            1,
            1_700_000_000,
            1_700_000_000_000,
            1_700_000_010,
            1_700_000_010_000,
            0,
            42,
            99,
            0,
            0.5,
            1.1,
            1.09,
            1.12,
            1.101,
            0.0,
            12.5,
            "EURUSD",
            "demo",
            "external",
        ),
        raw_position(
            2,
            1_700_000_100,
            1_700_000_100_000,
            1_700_000_110,
            1_700_000_110_000,
            1,
            43,
            100,
            1,
            0.2,
            1.2,
            1.18,
            1.25,
            1.205,
            0.0,
            -3.0,
            "GBPUSD",
            "demo-2",
            "external-2",
        ),
    ]

    result = models_from_namedtuples(Position, payloads)

    assert [position.ticket for position in result] == [1, 2]
    assert [position.symbol for position in result] == ["EURUSD", "GBPUSD"]
