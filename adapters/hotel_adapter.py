class HotelAdapter:
    def search_hotels(self, location, check_in, check_out):
        # Zasymulowany wynik API
        return [{"hotel": "Hilton", "location": location, "check_in": check_in, "check_out": check_out}]

    def book_hotel(self, hotel_name, check_in, check_out):
        return {"booking_id": "HOTEL001", "hotel_name": hotel_name, "check_in": check_in, "check_out": check_out}
