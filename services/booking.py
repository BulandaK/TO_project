class Booking:
    def __init__(self, booking_id, status="Oczekująca"):
        self.booking_id = booking_id
        self.status = status
        self.addons = []

    def set_status(self, status):
        self.status = status

    def add_addon(self, addon):
        self.addons.append(addon)

    def description(self):
        addons_desc = " + ".join(self.addons)
        return f"Rezerwacja ID: {self.booking_id}, Status: {self.status}" + (f" + {addons_desc}" if addons_desc else "")

    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "status": self.status,
            "addons": self.addons,
        }

    @staticmethod
    def from_dict(data):
        booking = Booking(data["booking_id"], data["status"])
        booking.addons = data.get("addons", [])
        return booking
