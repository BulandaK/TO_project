class Observer:
    def update(self, message):
        pass

class NotificationSystem(Observer):
    def update(self, message):
        print(f"[Powiadomienie]: {message}")

class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self, message):
        for observer in self._observers:
            observer.update(message)
