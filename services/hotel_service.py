from adapters.hotel_adapter import HotelAdapter
from patterns.state import PendingState
from services.booking import Booking


class HotelService:
    def __init__(self):
        self.adapter = HotelAdapter()

    def book_hotel(self, hotel_name, check_in, check_out):
        booking_info = self.adapter.book_hotel(hotel_name, check_in, check_out)
        hotel_booking = HotelBooking(booking_info["booking_id"], hotel_name, check_in, check_out)
        hotel_booking.set_state(PendingState(hotel_booking))
        return hotel_booking

class HotelBooking(Booking):
    def __init__(self, booking_id, hotel_name, check_in, check_out, status="Oczekująca"):
        super().__init__(booking_id, status)
        self.hotel_name = hotel_name
        self.check_in = check_in
        self.check_out = check_out

    def set_status(self, status):
        self.status = status

    def set_state(self, state):
        self.state = state
        self.state.handle()

    def description(self):
        return f"Hotel {self.hotel_name} ({self.check_in} - {self.check_out}), Status: {self.status}"

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "type": "hotel",
            "hotel_name": self.hotel_name,
            "check_in": self.check_in,
            "check_out": self.check_out,
        })
        return data

    @staticmethod
    def from_dict(data):
        return HotelBooking(data["booking_id"], data["hotel_name"], data["check_in"], data["check_out"])
