from hypothesis import given, strategies as st
from hotel_booking import nights_stayed, room_floor, booking_label

@given(st.text() | st.none())
def test_nights_stayed_no_crash(s):

@given(st.text() | st.none())
def test_room_floor_no_crash(s):

@given(st.text() | st.none())
def test_booking_label_no_crash(s):
