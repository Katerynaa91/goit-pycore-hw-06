"""Завдання. Розробити сутності (класи) для книги контактів.
Сутності:
•	Field: Базовий клас для полів запису.
•	Name: Клас для зберігання імені контакту. Обов'язкове поле.
•	Phone: Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
•	Record: Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів. Функціональність:
    •   Додавання телефонів.
    •	Видалення телефонів.
    •	Редагування телефонів.
    •	Пошук телефону.
•	AddressBook: Клас для зберігання та управління записами. Функціональність:
    •	Додавання записів.
    •	Пошук записів за іменем.
    •	Видалення записів за іменем."""

from collections import UserDict
import re


class Field:
    """Базовий клас для полів запису"""
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)
    

class Name(Field):
    """Клас для зберігання імені контакту. Наслідується від класу Field. Мість перевірку на довжину введеного імені."""
    def __init__(self, value):
        super().__init__(value)
        if len(str(value)) < 2:
            raise ValueError("The name should have at least 2 letters. Please use a different name")
        else: self.value = str(value).title()


class Phone(Field):
    """Клас для зберігання номера телефону. Для валідації формату (10 цифр) використовується модуль re. Наслідується від класу Field."""
    phone_pattern = r'\b[0-9]{10}\b'

    def __init__(self, value):
        super().__init__(value)
        if re.match(Phone.phone_pattern, str(value)):
            self.value = value
        else: self.value = None


class Record:
    """Клас для зберігання імені та списку телефонів контакту."""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
    
    def add_phone(self, phone):
        """Метод для додавання номерів телефонів для певного контакту. Якщо фомат номеру невірний (повертається None) 
        або якщо телефон вже є у списку телефонів, виводиться відповідне повідомлення."""
        if Phone(phone) in self.phones:
            print(f"The phone number {phone} is already in your Contacts list")
        else:
            if Phone(phone):
                self.phones.append(Phone(phone))
                print(f"Phone {phone} added to the Contacts list")
                return self.phones
            
            else: print(f"Unsupported format of the phone number {phone}. Please enter a valid number.")
    
    def remove_phone(self, phone):
        """Метод для видалення телефонів контакту. Якщо номер не знайдено у списку телефонів, виводиться відповідне повідомлення."""
        for p in self.phones:
            if str(p) == phone:
                self.phones.remove(p)
                print(f"Phone number {str(p)} removed from the Contacts list.")
            else:
                print(f"Couldn't remove the phone. Phone number {phone} not in the Contacts list")

    def edit_phone(self, old_phone, new_phone):
        """Метод для редагування телефонів контакту. Якщо новий номер не відповідає формату телефону, повертається попередній список телефонів.
        Перевіряється, чи номер телефону, який потрібно змінити, існує у списку телефонів даного контакту."""
        
        if not Phone(new_phone).value:
            print("Unsupported format of the new number")
            
        else:
            if old_phone in [p.value for p in self.phones]:
                self.phones[[p.value for p in self.phones].index(old_phone)] = Phone(new_phone)
                
            else: print("The number you are trying to replace is not in your Contacts list")
    
    def find_phone(self, phone):
        """Метод для пошуку номера телефону контакту у списку його телефонів. Якщо телефон не знайдено, викликається виключення."""
        if phone in [p.value for p in self.phones]:
            return Phone(phone)
        else: 
            raise ValueError("Phone number not in your Contacts list")

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    

class AddressBook(UserDict):
    """Клас для зберігання та управління записами про всі контакти. Наслудється від класу UserDict. 
    Атрибут класу - словник, де ключем є ім'я контакту, значення - список його номерів телефонів."""
    def __init__(self, **kwargs):
        self.data = dict(kwargs)

    def add_record(self, key):
        """Метод для додавання записів до словника-атрибута класу. 
        У якості ключа - ім'я об'єкта класу Record, значення - список телефонів об'єкта класу Record.
        Обробляється помилка AttributeError, яка виникає, якщо введене ім'я не є об'єктом класу Record."""
        try:
            self.data[key.name.value] = [p.value for p in key.phones]
        except AttributeError:
            print(f"No Record found for {key}")
        
    def find (self, key):
        """Метод для пошуку запису за ім'ям-ключем у словнику контактів. Обробляється помилка, якщо імені немає у словнику контактів.""" 
        try:
            return self.data[key.title()] if key.title() in [k for k in self.data.keys()] else None
        except KeyError: print(f"Name '{key}' not found")

    def delete(self, key):
        """Метод для видалення запису за ім'ям-ключем у словнику контактів. Виводиться відповідне помідомлення,
        якщо ім'я вудсутнє у словнику контактів і не може бути видалене.""" 
        if key.title() in self.data:
            del self.data[key.title()]
            print(f"{key} deleted")
        else: print(f"Cannot delete name {key} as it was not found in your Contacts list")


if __name__ == "__main__":


    book = AddressBook()

    john = Record("John")
    john.add_phone("1234567890")
    john.add_phone("5555555555")
    print(john)
    john.edit_phone("1234567890", "1223334444")
    print(john)
    found_phone = john.find_phone("5555555555")
    print(f"{john.name.value} found phone: {found_phone}")
    jane = Record("Jane")
    jane.add_phone("1231231231")
    book.add_record(john)
    book.add_record(jane)

    for name, record in book.data.items():
        print(name, record)

    print(book.find("john"))
    book.delete("jane")
    for name, record in book.data.items():
        print(name, record)
