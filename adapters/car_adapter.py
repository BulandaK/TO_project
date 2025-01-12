class CarAdapter:
    def search_cars(self, location, pick_up_date, drop_off_date):
        # Zasymulowany wynik API
        return [{"car": "Toyota", "location": location, "pick_up_date": pick_up_date, "drop_off_date": drop_off_date}]

    def book_car(self, car_name, pick_up_date, drop_off_date):
        return {"booking_id": "CAR001", "car_name": car_name, "pick_up_date": pick_up_date, "drop_off_date": drop_off_date}
