from collections import UserDict

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
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")



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
        index = self.phones.index(phone)
        self.phones[index] = Phone(new_phone)

    
    def find_phone(self, value):
        for phone in self.phones:
            if phone.value == value:
                return phone
        return None
        
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

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




# ─── Демонстрація роботи ────
 
if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону в записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
