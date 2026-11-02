import pytest
from hotel_booking import booking_cost, cancellation_refund, room_upgrade


# ---- booking_cost: executes every line ----
def test_standard_two_nights():
    assert booking_cost("standard", 2, 2, False) == 4000


def test_unknown_room_raises():
    with pytest.raises(ValueError, match="unknown room"):
        booking_cost("penthouse", 1, 1, False)


def test_invalid_nights_raises():
    with pytest.raises(ValueError, match="invalid nights"):
        booking_cost("standard", 0, 1, False)


def test_peak_extra_guests_long_stay():
    # suite 6000 + 1500 peak = 7500/night * 7 = 52500
    # + (4-2)*500*7 = 7000 -> 59500, minus 10% (5950) = 53550
    assert booking_cost("suite", 7, 4, True) == 53550


# ---- cancellation_refund: executes every line ----
def test_full_refund():
    assert cancellation_refund(1000, 10, False) == 1000


def test_half_refund_member():
    # 1000 // 2 = 500, + 1000 // 4 = 250
    assert cancellation_refund(1000, 3, True) == 750


def test_no_refund():
    assert cancellation_refund(1000, 1, False) == 0


# ---- room_upgrade: executes every line ----
def test_upgrade_no_rooms_free():
    assert room_upgrade("standard", True, 0) == "standard"


def test_upgrade_standard_member():
    assert room_upgrade("standard", True, 5) == "deluxe"


def test_upgrade_deluxe_member():
    assert room_upgrade("deluxe", True, 5) == "suite"


def test_upgrade_suite_stays():
    assert room_upgrade("suite", True, 5) == "suite"
