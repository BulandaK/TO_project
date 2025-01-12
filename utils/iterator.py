class BookingIterator:
    def __init__(self, bookings):
        self._bookings = bookings
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._bookings):
            booking = self._bookings[self._index]
            self._index += 1
            return booking
        raise StopIteration
