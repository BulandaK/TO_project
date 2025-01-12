import random
import time

from patterns.state import ConfirmedState
from services.flight_service import FlightBooking


def generate_storm(booking_service):
    """
    Generuje burzę w losowym mieście i wpływa na loty.

    :param booking_service: Instancja BookingService.
    :return: Dotknięty burzą lot (FlightBooking) lub None, jeśli brak oczekujących lotów.
    """
    # Pobierz listę lotów oczekujących na zatwierdzenie
    pending_flights = booking_service.list_pending_flights()

    if not pending_flights:
        booking_service.notify_observers("Brak lotów oczekujących na zatwierdzenie.")
        return None

    # Losowy wybór lotu i miasta (origin lub destination)
    affected_flight = random.choice(pending_flights)
    storm_city = random.choice([affected_flight.origin, affected_flight.destination])

    # Powiadomienie o burzy
    booking_service.notify_observers(f"Burza w mieście: {storm_city}!")
    booking_service.notify_observers(f"Lot {affected_flight.origin} -> {affected_flight.destination} został anulowany.")

    # Anulowanie lotu
    affected_flight.cancel()

    return affected_flight  # Zwraca lot dotknięty burzą


def add_storm(booking_service, active_storms, duration=10):
    """
    Generuje burzę między losowymi miastami i zapisuje ją na ograniczony czas.

    :param booking_service: Instancja BookingService.
    :param active_storms: Słownik przechowujący aktywne burze.
    :param duration: Czas trwania burzy w sekundach.
    """
    affected_flight = generate_storm(booking_service)
    if affected_flight:
        origin, destination = affected_flight.origin, affected_flight.destination
        expiration_time = time.time() + duration  # Burza trwa `duration` sekund
        active_storms[(origin, destination)] = expiration_time
        print(f"Burza wygenerowana między {origin} a {destination}. Wygaśnie o {expiration_time}.")


def remove_expired_storms(active_storms, booking_service):
    """
    Usuwa burze, które wygasły, i przywraca stan lotów na Confirmed.

    :param active_storms: Słownik przechowujący aktywne burze.
    :param booking_service: Instancja BookingService.
    """
    current_time = time.time()
    expired_storms = [
        route for route, expiration in active_storms.items() if expiration < current_time
    ]
    for route in expired_storms:
        # Usuwanie burzy z aktywnych
        del active_storms[route]
        print(f"Burza między {route[0]} a {route[1]} wygasła.")

        # Znajdź dotknięty lot
        for booking in booking_service.bookings:
            if isinstance(booking, FlightBooking) and \
               booking.origin == route[0] and booking.destination == route[1]:
                # Przywróć lot do stanu Confirmed
                booking.set_state(ConfirmedState())
                booking_service.notify_observers(
                    f"Lot {route[0]} -> {route[1]} został przywrócony i jest teraz potwierdzony."
                )
