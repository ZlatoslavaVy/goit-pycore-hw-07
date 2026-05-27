from collections import UserDict
from datetime import datetime, date, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    # реалізація класу
    pass


class Phone(Field):
    # реалізація класу
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("The phone number must be a 10-digits long.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            # Додайте перевірку коректності даних
            # та перетворіть рядок на об'єкт datetime
            string_to_object = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(string_to_object)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # реалізація класу

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        phone = self.find_phone(phone_number)
        if phone is not None:
            self.phones.remove(phone)
        else:
            raise ValueError("That phone number wasn't found!")

    def edit_phone(self, phone_number, new_phone):
        phone = self.find_phone(phone_number)
        if phone is None:
            raise ValueError("That phone number wasn't found!")
        new_phone_obj = Phone(new_phone)
        index = self.phones.index(phone)
        self.phones[index] = new_phone_obj

    def find_phone(self, value):
        for phone in self.phones:
            if phone.value == value:
                return phone
        return None

    def add_birthday(self, birthday_day):
        self.birthday = Birthday(birthday_day)

    def __str__(self):
        # Додано відображення дня народження, якщо воно є
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{birthday_str}"


class AddressBook(UserDict):
    # реалізація класу
    def add_record(self, record_object):
        self.data[record_object.name.value] = record_object

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name not in self.data:
            raise KeyError("There is no such contact!")
        del self.data[name]

    def get_upcoming_birthdays(self):
        today = date.today()
        result = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            born = record.birthday.value

            candidate = born.replace(year=today.year)

            if candidate < today:
                try:
                    candidate = born.replace(year=today.year + 1)
                except ValueError:
                    candidate = born.replace(year=today.year, day=28)

            delta = (candidate - today).days

            if 0 <= delta <= 7:

                if candidate.weekday() == 5:
                    candidate += timedelta(days=2)
                elif candidate.weekday() == 6:
                    candidate += timedelta(days=1)

                result.append(
                    {
                        "name": record.name.value,
                        "congratulation_date": candidate.strftime("%d.%m.%Y"),
                    }
                )

        result.sort(
            key=lambda x: datetime.strptime(x["congratulation_date"], "%d.%m.%Y")
        )
        return result
