import json
import time
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from services.flight_service import FlightBooking
from patterns.state import PendingState, ConfirmedState, CancelledState
from utils.storm_manager import add_storm, remove_expired_storms
from patterns.memento import BookingHistory



class FlightGraphVisualizer:
    def __init__(self, booking_service):
        self.booking_service = booking_service
        self.history = BookingHistory(booking_service)
        self.fig, self.ax = plt.subplots(figsize=(16, 9))
        self.G = nx.DiGraph()
        self.pos = None  # Pozycje węzłów na grafie (stałe)

        # Przechowywanie aktywnych burz
        self.active_storms = {}  # Klucz: (origin, destination), Wartość: czas wygaśnięcia

        # Rejestracja zdarzeń klawiatury
        self.fig.canvas.mpl_connect("key_press_event", self._handle_key_press)

    def _update_graph(self):
        """Buduje graf na podstawie rezerwacji."""
        self.G.clear()

        for booking in self.booking_service.bookings:
            if isinstance(booking, FlightBooking):
                # Domyślny kolor krawędzi zależny od stanu
                color = "blue" if isinstance(booking.state, PendingState) else \
                        "green" if isinstance(booking.state, ConfirmedState) else "red"

                # Jeśli linia jest dotknięta burzą, ustaw kolor na żółty
                if (booking.origin, booking.destination) in self.active_storms:
                    color = "yellow"

                self.G.add_edge(booking.origin, booking.destination, color=color)

        # Jeśli pozycje węzłów nie zostały jeszcze obliczone, oblicz je raz
        if self.pos is None:
            self.pos = nx.spring_layout(self.G, k=0.6, iterations=30)

    def _draw_graph(self):
        """Rysuje graf na podstawie zaktualizowanych danych."""
        self.ax.clear()

        # Kolory krawędzi
        edge_colors = [self.G[u][v]["color"] for u, v in self.G.edges()]

        # Rysowanie grafu
        nx.draw(
            self.G, self.pos, ax=self.ax,
            with_labels=True, edge_color=edge_colors,
            node_size=3000, node_color="lightblue",
            font_size=10
        )
        self.ax.set_title("Graf lotów (dynamiczna aktualizacja)")

    def _handle_key_press(self, event):
        """Obsługuje zdarzenia klawiatury."""
        if event.key == "s":
            self._save_state()
        elif event.key == "w":
            self._load_state()

    def _save_state(self):
        """Zapisuje aktualny stan rezerwacji."""
        self.history.save_state("last_graph_state.json")

    def _load_state(self):
        """Wczytuje stan rezerwacji."""
        try:
            self.history.load_state("last_graph_state.json")
            print("Stan wczytany z last_graph_state.json.")
            self._update_graph()
            self._draw_graph()
        except FileNotFoundError:
            print("Nie znaleziono pliku last_graph_state.json.")
        except Exception as e:
            print(f"Błąd podczas wczytywania stanu: {e}")

    def update(self, frame):
        """Funkcja aktualizująca graf co interwał."""
        # Dodaj nową burzę
        add_storm(self.booking_service, self.active_storms, duration=10)
        # Usuń wygasłe burze i przywróć stan lotów
        remove_expired_storms(self.active_storms, self.booking_service)

        # Aktualizuj graf i rysuj
        self._update_graph()
        self._draw_graph()

    def run(self):
        """Uruchamia dynamiczną wizualizację."""
        self._update_graph()  # Wstępne ustawienie grafu
        animation = FuncAnimation(self.fig, self.update, interval=900)  # Aktualizuj co 5000 ms (5 sekund)
        plt.show()
