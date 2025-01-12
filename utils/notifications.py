class Notification:
    def __init__(self, message):
        self.message = message

    def send(self):
        print(f"[NOTYFIKACJA]: {self.message}")
