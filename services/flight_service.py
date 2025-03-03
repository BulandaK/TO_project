import json

from adapters.flight_adapter import FlightAdapter
from patterns.state import PendingState, ConfirmedState, CancelledState
from services.booking import Booking
from utils.flight_iterator import FlightIterator


class FlightService:
    def __init__(self):
        self.adapter = FlightAdapter()

    def book_flight(self, origin, destination, date):
        flight_id = "FLIGHT001"  # Przykładowy identyfikator rezerwacji
        flight_booking = FlightBooking(flight_id, origin, destination, date)
        flight_booking.set_state(PendingState())  # Ustaw stan na "Oczekująca"
        return flight_booking
    @staticmethod
    def load_flights_from_json(file_name):
        """Wczytuje loty z pliku JSON i zwraca iterator obiektów FlightBooking."""
        with open(file_name, "r", encoding="utf-8") as file:
            flight_data = json.load(file)

        flights = [
            FlightBooking(
                flight["booking_id"],
                flight["origin"],
                flight["destination"],
                flight["date"],
                status=flight["status"]
            )
            for flight in flight_data
        ]
        return FlightIterator(flights)


class FlightBooking(Booking):
    def __init__(self, booking_id, origin, destination, date, status="Oczekująca"):
        super().__init__(booking_id, status)
        self.origin = origin
        self.destination = destination
        self.date = date

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
        # Tworzenie obiektu FlightBooking
        booking = FlightBooking(
            data["booking_id"],
            data["origin"],
            data["destination"],
            data["date"]
        )

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
