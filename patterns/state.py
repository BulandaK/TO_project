class BookingState:
    def __init__(self, booking):
        self.booking = booking

    def handle(self):
        raise NotImplementedError

class PendingState(BookingState):
    def handle(self):
        self.booking.set_status("Oczekująca")

class ConfirmedState(BookingState):
    def handle(self):
        self.booking.set_status("Potwierdzona")

class CancelledState(BookingState):
    def handle(self):
        self.booking.set_status("Anulowana")
