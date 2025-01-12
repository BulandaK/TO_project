class FlightIterator:
    """Iterator do przeglądania lotów wczytanych z JSON."""
    def __init__(self, flights):
        self._flights = flights
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._flights):
            flight = self._flights[self._index]
            self._index += 1
            return flight
        raise StopIteration
