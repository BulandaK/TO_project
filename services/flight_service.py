from adapters.flight_adapter import FlightAdapter
from patterns.state import PendingState
from services.booking import Booking


class FlightService:
    def __init__(self):
        self.adapter = FlightAdapter()

    def book_flight(self, origin, destination, date):
        available_flights = self.adapter.search_flights(origin, destination, date)
        if available_flights:
            flight_id = available_flights[0]["flight"]
            booking_info = self.adapter.book_flight(flight_id)
            flight_booking = FlightBooking(booking_info["booking_id"], origin, destination, date)
            flight_booking.set_state(PendingState(flight_booking))
            return flight_booking
        return None


class FlightBooking(Booking):
    def __init__(self, booking_id, origin, destination, date, status="Oczekująca"):
        super().__init__(booking_id, status)
        self.origin = origin
        self.destination = destination
        self.date = date

    def set_status(self, status):
        self.status = status

    def set_state(self, state):
        self.state = state
        self.state.handle()

    def description(self):
        return f"Lot {self.origin} -> {self.destination} ({self.date}), Status: {self.status}"

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "type": "flight",
            "origin": self.origin,
            "destination": self.destination,
            "date": self.date,
        })
        return data

    @staticmethod
    def from_dict(data):
        return FlightBooking(data["booking_id"], data["origin"], data["destination"], data["date"])
