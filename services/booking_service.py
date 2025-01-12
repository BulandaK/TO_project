from patterns.observer import Observable
from services.booking import Booking
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

    def to_dict(self):
        return [booking.to_dict() for booking in self.bookings]

    def from_dict(self, data):
        self.bookings = []
        for item in data:
            try:
                if "type" not in item:
                    raise KeyError("Brak klucza 'type' w danych rezerwacji.")

                if item["type"] == "flight":
                    self.bookings.append(FlightBooking.from_dict(item))
                elif item["type"] == "hotel":
                    self.bookings.append(HotelBooking.from_dict(item))
                elif item["type"] == "car":
                    self.bookings.append(CarBooking.from_dict(item))
                else:
                    raise ValueError(f"Nieznany typ rezerwacji: {item['type']}")
            except Exception as e:
                print(f"Błąd podczas przetwarzania elementu: {item}. Szczegóły: {e}")


