class BookingState:
    """Interfejs dla stanów rezerwacji."""
    def handle(self, booking):
        raise NotImplementedError

    def change_state(self, booking, new_state):
        booking.set_state(new_state)


class PendingState(BookingState):
    """Stan: Oczekująca."""
    def handle(self, booking):
        print(f"Rezerwacja {booking.booking_id} jest w stanie: Oczekująca. Oczekuje na potwierdzenie.")

    def confirm(self, booking):
        print(f"Rezerwacja {booking.booking_id} została potwierdzona.")
        self.change_state(booking, ConfirmedState())

    def cancel(self, booking):
        print(f"Rezerwacja {booking.booking_id} została anulowana.")
        self.change_state(booking, CancelledState())


class ConfirmedState(BookingState):
    """Stan: Potwierdzona."""
    def handle(self, booking):
        print(f"Rezerwacja {booking.booking_id} jest w stanie: Potwierdzona.")

    def cancel(self, booking):
        print(f"Rezerwacja {booking.booking_id} została anulowana po potwierdzeniu.")
        self.change_state(booking, CancelledState())


class CancelledState(BookingState):
    """Stan: Anulowana."""
    def handle(self, booking):
        print(f"Rezerwacja {booking.booking_id} jest w stanie: Anulowana. Nie można już jej zmienić.")
