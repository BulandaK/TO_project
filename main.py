from patterns.observer import NotificationSystem
from services.booking_service import BookingService
from services.flight_service import FlightService
from services.hotel_service import HotelService
from services.car_service import CarService
from patterns.memento import BookingHistory
from utils.storm_generator import generate_storm


def main():
    # Tworzenie usług
    booking_service = BookingService()
    flight_service = FlightService()

    # Dodanie systemu powiadomień jako obserwatora
    notification_system = NotificationSystem()
    booking_service.add_observer(notification_system)

    # Wczytanie lotów z JSON i dodanie ich do BookingService
    print("\n=== Wczytywanie lotów z pliku JSON ===")
    flight_iterator = flight_service.load_flights_from_json("flights.json")
    for flight_booking in flight_iterator:
        booking_service.add_booking(flight_booking)

    # Wyświetlenie wszystkich rezerwacji
    print("\n=== Wszystkie rezerwacje ===")
    booking_service.list_bookings()

    # Generowanie burzy
    print("\n=== Generowanie burzy ===")
    generate_storm(booking_service)

    # Wyświetlenie rezerwacji po burzy
    print("\n=== Rezerwacje po burzy ===")
    booking_service.list_bookings()

    # Zapis stanu
    history = BookingHistory(booking_service)
    history.save_state("bookings_snapshot.json")

    # Symulacja zmiany statusu
    print("\n=== Aktualizacja rezerwacji ===")


    # Powiadomienia
    booking_service.notify_observers("Status rezerwacji został zmieniony.")

    # Przywrócenie stanu
    print("\n=== Przywracanie rezerwacji ===")
    history.load_state("bookings_snapshot.json")
    booking_service.list_bookings()


if __name__ == "__main__":
    main()
