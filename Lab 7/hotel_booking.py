def _parse_day(text):
    """Return text as a day-of-month int (1-31), or None if it isn't one.

    str.isdigit() alone is not enough: it accepts characters such as '²' or
    Arabic-Indic digits that int() rejects, so restrict to ASCII digits.
    """
    text = text.strip()
    if not text or not text.isascii() or not text.isdigit():
        return None
    day = int(text)
    if not 1 <= day <= 31:
        return None
    return day


def nights_stayed(days):
    """'12-15' -> 3. Returns None for any malformed or impossible input."""
    if not isinstance(days, str):
        return None
    parts = days.split('-')
    if len(parts) != 2:
        return None
    check_in, check_out = _parse_day(parts[0]), _parse_day(parts[1])
    if check_in is None or check_out is None:
        return None
    if check_out <= check_in:
        return None  # a stay must be at least one night
    return check_out - check_in


def room_floor(room_code):
    """'D-305' -> 3. Returns None for any malformed input."""
    if not isinstance(room_code, str):
        return None
    parts = room_code.strip().split('-')
    if len(parts) != 2:
        return None
    wing, number = parts[0].strip(), parts[1].strip()
    if not wing or not wing.isascii() or not wing.isalpha():
        return None
    if not number or not number.isascii() or not number.isdigit():
        return None
    return int(number[0])


def booking_label(names_csv):
    """'ravi, priya' -> 'Ravi +1'. Returns None if there are no guest names."""
    if not isinstance(names_csv, str):
        return None
    names = [n.strip() for n in names_csv.split(',')]
    names = [n for n in names if n]  # drop blanks from ',,' or trailing commas
    if not names:
        return None
    lead = names[0]
    return lead[0].upper() + lead[1:] + " +" + str(len(names) - 1)


def main():
    print("==== Running nights_stayed ====")
    user_input = input("Enter check-in and check-out day (e.g. 12-15): ")
    result = nights_stayed(user_input)
    if result is None:
        print("Invalid input: use two days 1-31 as 'checkin-checkout', check-out after check-in.")
    else:
        print("Nights:", result)

    print("\n==== Running room_floor ====")
    user_input = input("Enter a room code (e.g. D-305): ")
    result = room_floor(user_input)
    if result is None:
        print("Invalid input: use a wing letter, a dash and a room number (e.g. D-305).")
    else:
        print("Floor:", result)

    print("\n==== Running booking_label ====")
    user_input = input("Enter guest names as CSV (e.g. ravi, priya): ")
    result = booking_label(user_input)
    if result is None:
        print("Invalid input: enter at least one guest name.")
    else:
        print("Booking Label:", result)


if __name__ == "__main__":
    main()
