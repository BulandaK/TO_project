class BookingDecorator:
    def __init__(self, booking):
        self.booking = booking

    def description(self):
        return self.booking.description()

    def to_dict(self):
        data = self.booking.to_dict()  # Wywołanie bazowego obiektu
        data["addons"] = data.get("addons", []) + ["Insurance"]
        return data

    def set_status(self, status):
        # Delegowanie metody do dekorowanego obiektu
        self.booking.set_status(status)

    def __getattr__(self, attr):
        # Delegowanie innych wywołań metod do dekorowanego obiektu
        return getattr(self.booking, attr)


class InsuranceDecorator(BookingDecorator):
    def description(self):
        return f"{self.booking.description()} + Ubezpieczenie"

    def to_dict(self):
        data = self.booking.to_dict()
        data["addons"] = data.get("addons", []) + ["Insurance"]
        return data
