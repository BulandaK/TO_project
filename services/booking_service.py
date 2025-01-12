from patterns.observer import Observable
from patterns.state import PendingState
from services.car_service import CarBooking
from services.flight_service import FlightBooking
from services.hotel_service import HotelBooking


class BookingService(Observable):
    def __init__(self):
        super().__init__()
        self.bookings = []

    def add_booking(self, booking):
        self.bookings.append(booking)
        self.notify_observers(f"Nowa rezerwacja: {booking.description()}")

    def list_bookings(self):
        for booking in self.bookings:
            print(booking.description())

    def list_pending_flights(self):
        """Zwraca listę lotów w stanie Oczekująca."""
        return [booking for booking in self.bookings if
                isinstance(booking, FlightBooking) and isinstance(booking.state, PendingState)]

    def to_dict(self):
        """Zapisuje stan wszystkich rezerwacji."""
        return [booking.to_dict() for booking in self.bookings]

    def from_dict(self, data):
        """
        Odtwarza stan rezerwacji na podstawie wczytanych danych.
        """
        self.bookings = []
        for booking_data in data:
            booking_type = booking_data.get("type")
            if booking_type == "flight":
                booking = FlightBooking.from_dict(booking_data)
            elif booking_type == "hotel":
                booking = HotelBooking.from_dict(booking_data)
            elif booking_type == "car":
                booking = CarBooking.from_dict(booking_data)
            else:
                raise ValueError(f"Nieznany typ rezerwacji: {booking_type}")
            self.bookings.append(booking)

