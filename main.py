from services.booking_service import BookingService
from services.flight_service import FlightService
from services.hotel_service import HotelService
from services.car_service import CarService
from patterns.memento import BookingHistory
from patterns.observer import NotificationSystem
from decorators.insurance_decorator import InsuranceDecorator
from decorators.meal_decorator import MealDecorator


def main():
    # Tworzenie usług
    flight_service = FlightService()
    hotel_service = HotelService()
    car_service = CarService()

    booking_service = BookingService()
    notification_system = NotificationSystem()
    booking_service.add_observer(notification_system)

    # Rezerwacja lotu
    flight_booking = flight_service.book_flight("Warszawa", "Nowy Jork", "2025-01-15")
    flight_booking = InsuranceDecorator(flight_booking)
    flight_booking = MealDecorator(flight_booking)

    # Rezerwacja hotelu
    hotel_booking = hotel_service.book_hotel("Hilton", "2025-01-15", "2025-01-20")

    # Rezerwacja samochodu
    car_booking = car_service.book_car("Toyota", "2025-01-15", "2025-01-20")

    # Dodanie rezerwacji do systemu
    booking_service.add_booking(flight_booking)
    booking_service.add_booking(hotel_booking)
    booking_service.add_booking(car_booking)

    # Wyświetlenie stanu rezerwacji
    print("\n=== Rezerwacje ===")
    booking_service.list_bookings()

    # Zapis stanu
    history = BookingHistory(booking_service)
    history.save_state("bookings_snapshot.json")

    # Symulacja zmiany statusu
    print("\n=== Aktualizacja rezerwacji ===")
    flight_booking.set_status("Potwierdzona")
    hotel_booking.set_status("Anulowana")

    # Powiadomienia
    booking_service.notify_observers("Status rezerwacji został zmieniony.")

    # Przywrócenie stanu
    print("\n=== Przywracanie rezerwacji ===")
    history.load_state("bookings_snapshot.json")
    booking_service.list_bookings()


if __name__ == "__main__":
    main()
