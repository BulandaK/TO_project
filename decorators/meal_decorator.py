from decorators.insurance_decorator import BookingDecorator

class MealDecorator(BookingDecorator):
    def description(self):
        return f"{self.booking.description()} + Posiłek"

    def to_dict(self):
        data = self.booking.to_dict()
        data["addons"] = data.get("addons", []) + ["Meal"]
        return data
