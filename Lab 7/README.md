# L6_L7_22_hotel_booking — Hotel Booking

Lab 7: Fuzz Testing

## Files

| File | Description |
|------|-------------|
| `hotel_booking.py` | Buggy code to test and fix |
| `test_hotel_booking.py` | Fuzz test file to complete using Hypothesis |

Refer to the lab handout for instructions.

## How to run

```bash
pip install hypothesis pytest
python hotel_booking.py              # interactive app
python -m pytest test_hotel_booking.py -v
```

## Bugs found by fuzzing (and fixed)

| Function | Crashing inputs found by Hypothesis | Fix |
|----------|-------------------------------------|-----|
| `nights_stayed` | `None`, `''`, `'0'`, `'-'`, `'-1'`, non-numeric days; also returned negative nights for e.g. `'15-12'` | Type check, require exactly two ASCII-digit days in 1–31, check-out after check-in; return `None` otherwise |
| `room_floor` | `None`, `''`, `'-'`, `'-A'`, `'-:'` (missing dash / empty or non-numeric room number) | Type check, require `<letters>-<digits>`; return `None` otherwise |
| `booking_label` | `None`, `''`, blank names such as `' , priya'` | Type check, drop blank names, return `None` when no names remain |

Invalid input now returns `None` instead of raising, and `main()` prints a friendly error message.
