import pytest
from hotel_booking import booking_cost, cancellation_refund, room_upgrade


# ---- booking_cost: both outcomes of every decision ----
@pytest.mark.parametrize("room, rate", [("standard", 2000), ("deluxe", 3500), ("suite", 6000)])
def test_each_room_off_peak(room, rate):
    assert booking_cost(room, 1, 2, False) == rate


def test_unknown_room_raises():
    with pytest.raises(ValueError, match="unknown room"):
        booking_cost("penthouse", 1, 1, False)


def test_known_room_is_not_rejected():
    # `room not in ROOM_RATE` False branch
    assert booking_cost("standard", 1, 1, False) == 2000


@pytest.mark.parametrize("nights", [0, -3])
def test_invalid_nights_raises(nights):
    with pytest.raises(ValueError, match="invalid nights"):
        booking_cost("standard", nights, 1, False)


def test_one_night_is_valid_boundary():
    assert booking_cost("standard", 1, 1, False) == 2000


def test_peak_season_adds_25_percent():
    assert booking_cost("standard", 1, 1, True) == 2500


def test_off_peak_no_surcharge():
    assert booking_cost("standard", 1, 1, False) == 2000


def test_two_guests_no_extra_charge_boundary():
    assert booking_cost("standard", 2, 2, False) == 4000


def test_three_guests_extra_charge_boundary():
    # 2000*2 + (3-2)*500*2 = 5000
    assert booking_cost("standard", 2, 3, False) == 5000


def test_six_nights_no_discount_boundary():
    assert booking_cost("standard", 6, 1, False) == 12000


def test_seven_nights_discount_boundary():
    # 14000 - 1400
    assert booking_cost("standard", 7, 1, False) == 12600


def test_peak_extra_guests_long_stay_all_true():
    assert booking_cost("suite", 7, 4, True) == 53550


# ---- cancellation_refund: every if/elif/else and the member check ----
def test_refund_seven_days_boundary():
    assert cancellation_refund(1000, 7, False) == 1000


def test_refund_member_full_refund_ignores_bonus():
    assert cancellation_refund(1000, 10, True) == 1000


def test_refund_six_days_half():
    assert cancellation_refund(1000, 6, False) == 500


def test_refund_two_days_boundary_half():
    assert cancellation_refund(1000, 2, False) == 500


def test_refund_half_member_bonus():
    assert cancellation_refund(1000, 3, True) == 750


def test_refund_one_day_none():
    assert cancellation_refund(1000, 1, False) == 0


def test_refund_zero_days_member_bonus_only():
    assert cancellation_refund(1000, 0, True) == 250


# ---- room_upgrade: every condition outcome ----
def test_upgrade_no_rooms_free():
    assert room_upgrade("standard", True, 0) == "standard"


def test_upgrade_standard_member():
    assert room_upgrade("standard", True, 3) == "deluxe"


def test_upgrade_standard_non_member():
    assert room_upgrade("standard", False, 3) == "standard"


def test_upgrade_deluxe_member():
    assert room_upgrade("deluxe", True, 3) == "suite"


def test_upgrade_deluxe_non_member():
    assert room_upgrade("deluxe", False, 3) == "deluxe"


def test_upgrade_suite_member_stays():
    assert room_upgrade("suite", True, 3) == "suite"


def test_upgrade_suite_non_member_stays():
    assert room_upgrade("suite", False, 3) == "suite"
