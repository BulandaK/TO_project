import random

def generate_storm(booking_service):
    """Generuje burzę w losowym mieście i wpływa na loty."""
    # Pobierz listę lotów oczekujących na zatwierdzenie
    pending_flights = booking_service.list_pending_flights()

    if not pending_flights:
        booking_service.notify_observers("Brak lotów oczekujących na zatwierdzenie.")
        return

    # Losowy wybór lotu i miasta (origin lub destination)
    affected_flight = random.choice(pending_flights)
    storm_city = random.choice([affected_flight.origin, affected_flight.destination])

    # Powiadomienie o burzy
    booking_service.notify_observers(f"Burza w mieście: {storm_city}!")
    booking_service.notify_observers(f"Lot {affected_flight.origin} -> {affected_flight.destination} został anulowany.")

    # Anulowanie lotu
    affected_flight.cancel()
