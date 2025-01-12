class FlightAdapter:
    def search_flights(self, origin, destination, date):
        # Zasymulowany wynik API
        return [{"flight": "LOT123", "origin": origin, "destination": destination, "date": date}]

    def book_flight(self, flight_id):
        return {"booking_id": "FLIGHT001", "flight_id": flight_id}
