from adapters.car_adapter import CarAdapter
from patterns.state import PendingState
from services.booking import Booking


class CarService:
    def __init__(self):
        self.adapter = CarAdapter()

    def book_car(self, car_name, pick_up_date, drop_off_date):
        booking_info = self.adapter.book_car(car_name, pick_up_date, drop_off_date)
        car_booking = CarBooking(booking_info["booking_id"], car_name, pick_up_date, drop_off_date)
        car_booking.set_state(PendingState(car_booking))
        return car_booking

class CarBooking(Booking):
    def __init__(self, booking_id, car_name, pick_up_date, drop_off_date, status="Oczekująca"):
        super().__init__(booking_id, status)
        self.car_name = car_name
        self.pick_up_date = pick_up_date
        self.drop_off_date = drop_off_date

    def set_status(self, status):
        self.status = status

    def set_state(self, state):
        self.state = state
        self.state.handle()

    def description(self):
        return f"Samochód {self.car_name} ({self.pick_up_date} - {self.drop_off_date}), Status: {self.status}"

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "type": "car",
            "car_name": self.car_name,
            "pick_up_date": self.pick_up_date,
            "drop_off_date": self.drop_off_date,
        })
        return data

    @staticmethod
    def from_dict(data):
        return CarBooking(data["booking_id"], data["car_name"], data["pick_up_date"], data["drop_off_date"])
