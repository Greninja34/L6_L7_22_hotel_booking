def nights_stayed(days):
    check_in, check_out = days.split('-')
    return int(check_out) - int(check_in)

def room_floor(room_code):
    number = room_code.split('-')[1]
    return int(number[0])

def booking_label(names_csv):
    names = [n.strip() for n in names_csv.split(',')]
    lead = names[0]
    return lead[0].upper() + lead[1:] + " +" + str(len(names) - 1)

def main():
    print("==== Running nights_stayed ====")
    user_input = input("Enter check-in and check-out day (e.g. 12-15): ")
    result = nights_stayed(user_input)
    print("Nights:", result)

    print("\n==== Running room_floor ====")
    user_input = input("Enter a room code (e.g. D-305): ")
    result = room_floor(user_input)
    print("Floor:", result)

    print("\n==== Running booking_label ====")
    user_input = input("Enter guest names as CSV (e.g. ravi, priya): ")
    result = booking_label(user_input)
    print("Booking Label:", result)

if __name__ == "__main__":
    main()
