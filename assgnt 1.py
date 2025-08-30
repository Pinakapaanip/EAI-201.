import time

def get_room_size():
    return input("Enter the room size (small / medium / large): ").lower()

def get_room_shape():
    return input("Enter the room shape (square / rectangle / circular): ").lower()

def get_dust_location():
    return input("Where is most of the dust located? (center / sides / entrance): ").lower()

def get_dust_quantity():
    return input("How much dust is there? (less / medium / large): ").lower()

def ask_dock_option():
    return input("Should the vacuum dock itself after cleaning? (yes / no): ").lower()

def start_cleaning(room_size, room_shape, dust_location, dust_quantity):
    print("\nInitializing Cleaning Process...\n")
    print(f"Room Size: {room_size}")
    print(f"Room Shape: {room_shape}")
    print(f"Dust Location: {dust_location}")
    print(f"Dust Quantity: {dust_quantity}")
    print("Status: Cleaning...\n")
    time.sleep(5)
    print("Cleaning is completed")

def handle_docking(dock_option):
    if dock_option == "yes":
        print("Returning to docking station...")
        time.sleep(5)
        print("Docked successfully.")
    else:
        print("Staying in current location. Docking skipped.")

def vacuum_cleaner():
    print("Welcome to Smart AI Vacuum Cleaner\n")
    room_size = get_room_size()
    room_shape = get_room_shape()
    dust_location = get_dust_location()
    dust_quantity = get_dust_quantity()
    dock_option = ask_dock_option()
    start_cleaning(room_size, room_shape, dust_location, dust_quantity)
    handle_docking(dock_option)
    print("\nThank you for using Smart AI Vacuum Cleaner.")

vacuum_cleaner()
4
