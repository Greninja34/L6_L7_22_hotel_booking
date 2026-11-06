from hypothesis import given, strategies as st
from hotel_booking import nights_stayed, room_floor, booking_label


# ---------------------------------------------------------------------------
# 1. "No crash" fuzz tests: throw arbitrary text (or None) at every function.
#    A robust function must never raise; it should return None for bad input.
# ---------------------------------------------------------------------------

@given(st.text() | st.none())
def test_nights_stayed_no_crash(s):
    try:
        result = nights_stayed(s)
    except Exception as e:
        assert False, f"nights_stayed crashed on {s!r} with: {e!r}"
    assert result is None or (isinstance(result, int) and result > 0)


@given(st.text() | st.none())
def test_room_floor_no_crash(s):
    try:
        result = room_floor(s)
    except Exception as e:
        assert False, f"room_floor crashed on {s!r} with: {e!r}"
    assert result is None or (isinstance(result, int) and 0 <= result <= 9)


@given(st.text() | st.none())
def test_booking_label_no_crash(s):
    try:
        result = booking_label(s)
    except Exception as e:
        assert False, f"booking_label crashed on {s!r} with: {e!r}"
    assert result is None or isinstance(result, str)


# ---------------------------------------------------------------------------
# 2. Targeted fuzzing: inputs that *look* almost valid, which is where most
#    real-world validation bugs hide (missing parts, extra separators, etc.).
# ---------------------------------------------------------------------------

near_valid_days = st.one_of(
    st.integers(min_value=-100, max_value=100).map(str),
    st.builds(lambda a, b: f"{a}-{b}", st.integers(-50, 50), st.integers(-50, 50)),
    st.builds(lambda a, b, c: f"{a}-{b}-{c}", st.integers(0, 31), st.integers(0, 31), st.integers(0, 31)),
    st.builds(lambda a, b: f"{a}-{b}", st.text(max_size=3), st.text(max_size=3)),
)


@given(near_valid_days)
def test_nights_stayed_near_valid_no_crash(s):
    try:
        result = nights_stayed(s)
    except Exception as e:
        assert False, f"nights_stayed crashed on {s!r} with: {e!r}"
    # Negative or zero nights must never be reported as a valid stay.
    assert result is None or result > 0


near_valid_rooms = st.one_of(
    st.text(alphabet="ABCD-0123456789 ", max_size=8),
    st.builds(lambda w, n: f"{w}-{n}", st.text(max_size=2), st.text(max_size=4)),
)


@given(near_valid_rooms)
def test_room_floor_near_valid_no_crash(s):
    try:
        room_floor(s)
    except Exception as e:
        assert False, f"room_floor crashed on {s!r} with: {e!r}"


near_valid_names = st.text(alphabet="ab ,", max_size=10)


@given(near_valid_names)
def test_booking_label_near_valid_no_crash(s):
    try:
        booking_label(s)
    except Exception as e:
        assert False, f"booking_label crashed on {s!r} with: {e!r}"


# ---------------------------------------------------------------------------
# 3. Correctness properties: for well-formed input the answer must be right.
# ---------------------------------------------------------------------------

@given(st.integers(min_value=1, max_value=31), st.integers(min_value=1, max_value=31))
def test_nights_stayed_correct_for_valid_days(a, b):
    check_in, check_out = min(a, b), max(a, b)
    if check_in == check_out:
        return
    assert nights_stayed(f"{check_in}-{check_out}") == check_out - check_in
    # Surrounding whitespace should not matter.
    assert nights_stayed(f" {check_in} - {check_out} ") == check_out - check_in


@given(
    st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=1, max_size=2),
    st.integers(min_value=100, max_value=999),
)
def test_room_floor_correct_for_valid_codes(wing, number):
    assert room_floor(f"{wing}-{number}") == number // 100


name = st.text(alphabet="abcdefghijklmnopqrstuvwxyz", min_size=1, max_size=8)


@given(st.lists(name, min_size=1, max_size=6))
def test_booking_label_correct_for_valid_names(names):
    label = booking_label(", ".join(names))
    lead = names[0]
    assert label == lead[0].upper() + lead[1:] + " +" + str(len(names) - 1)
