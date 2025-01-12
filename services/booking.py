from patterns.state import PendingState, ConfirmedState, CancelledState

class Booking:
    def __init__(self, booking_id, status="Oczekująca"):
        self.booking_id = booking_id
        self.state = PendingState()  # Domyślny stan to "Oczekująca"

    def set_state(self, new_state):
        self.state = new_state

    def handle(self):
        self.state.handle(self)

    def confirm(self):
        if hasattr(self.state, "confirm"):
            self.state.confirm(self)
        else:
            print(f"Stan {self.state.__class__.__name__} nie obsługuje potwierdzenia.")

    def cancel(self):
        if hasattr(self.state, "cancel"):
            self.state.cancel(self)
        else:
            print(f"Stan {self.state.__class__.__name__} nie obsługuje anulowania.")

    def description(self):
        """Zwraca ogólny opis rezerwacji."""
        return f"Rezerwacja ID: {self.booking_id}, Status: {self.state.__class__.__name__.replace('State', '')}"

    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "status": self.state.__class__.__name__.replace("State", ""),
        }

    @staticmethod
    def from_dict(data):
        # Tworzenie obiektu Booking
        booking = Booking(data["booking_id"])

        # Mapowanie nazw statusów na klasy stanów
        state_map = {
            "Pending": PendingState,
            "Confirmed": ConfirmedState,
            "Cancelled": CancelledState,
        }

        # Ustawienie odpowiedniego stanu na podstawie "status"
        if data["status"] in state_map:
            booking.set_state(state_map[data["status"]]())
        else:
            raise ValueError(f"Nieznany status: {data['status']}")

        return booking
