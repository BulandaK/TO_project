import json

class BookingHistory:
    def __init__(self, booking_service):
        self.booking_service = booking_service

    def save_state(self, file_name):
        data = self.booking_service.to_dict()
        print("Zapisywane dane:", data)  # Debug: sprawdzamy dane przed zapisem
        with open(file_name, 'w') as file:
            json.dump(data, file)
        print(f"Stan zapisany do {file_name}.")

    def load_state(self, file_name):
        with open(file_name, 'r') as file:
            data = json.load(file)
        print("Odczytane dane:", data)  # Debug: sprawdzamy dane po odczycie
        self.booking_service.from_dict(data)
        print(f"Stan załadowany z {file_name}.")
