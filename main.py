from collections import UserDict
from datetime import date, datetime
import itertools
import os
import pickle
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    ...


class Phone(Field):
    def __init__(self,value):
        self.value = value
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        if  new_value.isdigit() and len(new_value) == 10:
            self._value = new_value
        else:
            raise ValueError
        
class Birthday(Field):
    def __init__(self, value: str):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = datetime.strptime(new_value, r'%Y-%m-%d').date()
        if not self._value:
            raise ValueError


class Record:
    def __init__(self, name, phone, b_day=None):
        self.name = Name(name)
        phone_number = Phone(phone)
        self.phones = [phone_number]
        self.birthday = None
        if b_day:
            try:
                self.birthday = Birthday(b_day)
            except ValueError:
                print(f'For {self.name} wrong birthday format')

    def add_phone(self, phone_number):
        try:
            phone = Phone(phone_number)
            self.phones.append(phone)
        except ValueError:
            print(f'{phone_number} is wrong format, nuber must be only digits and 10 numbers length')
    
    def remove_phone(self, removing_phone):
        for ph in self.phones:
            if ph.value == removing_phone:
                self.phones.remove(ph)
                return f'{removing_phone} was removed'
        raise ValueError

    def edit_phone(self, existed_number, new_number):
        new_phone = Phone(new_number)
        for ph in self.phones:
            if ph.value == existed_number:
                self.phones.remove(ph)
                self.phones.append(new_phone)
                return 'Phone number edited'
        raise ValueError

    def find_phone(self, phone_number):
        phone = Phone(phone_number)
        for ph in self.phones:
            if ph.value == phone.value:
                return phone
        return None 
    
    def days_to_birthday(self):
        if self.birthday:
            self.todays_date = date.today()
            try:
                if (self.todays_date.month < self.birthday.value.month):
                    next_birthday = date(self.todays_date.year, self.birthday.value.month, self.birthday.value.day)
                elif (self.todays_date.month == self.birthday.value.month) and (self.todays_date.day < self.birthday.value.day):
                    next_birthday = date(self.todays_date.year, self.birthday.value.month, self.birthday.value.day)
                elif (self.todays_date.month == self.birthday.value.month) and (self.todays_date.day >= self.birthday.value.day):
                    next_birthday = date(self.todays_date.year + 1, self.birthday.value.month, self.birthday.value.day)
                else:
                    next_birthday = date(self.todays_date.year + 1, self.birthday.value.month, self.birthday.value.day)
                delta = next_birthday - self.todays_date
                # return f"{self.name}'s B-Day in {delta.days} days"
                return delta.days
            except ValueError:
                print(f'For {self.name} wrong birthday format')
        else:
            return f'{self.name} has no birthday date'

        
    def __str__(self):
        if self.birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    counter = 0

    def add_record(self, record: Record):
        self.data[record.name.value] = record
    
    def find(self, name: Name):
        if name in self.data:
            return self.data[name]
        return None 

    def delete(self, name_for_deleting: Name):
        if name_for_deleting in self.data:
            del self.data[name_for_deleting]

    def iterator(self, batch_size=2):
        counter = 0
        while counter < len(self.data):
            yield itertools.islice(self.data.values(), counter, counter + batch_size)
            _ = input('Press enter for next page...')
            counter += batch_size

    def searching(self, searching_phrase):
        searching_list = []
        if len(searching_phrase) >= 2:
            for el in self.data.values():
                el = str(el)
                match = re.search(searching_phrase, el)
                if match:
                    searching_list.append(el)
        return searching_list


def storeData(adressbook, file_name='saved_addressbook.bin'):
    with open(file_name, 'wb') as bin_file:
        pickle.dump(adressbook, bin_file)

def loadData():
    with open('saved_addressbook.bin', 'rb') as bin_file:
        readed = pickle.load(bin_file)
        return readed


if __name__ == '__main__':
    if os.path.isfile('./saved_addressbook.bin'):
        book = loadData()
    else:
        book = AddressBook()
    record1 = Record("John Doe", "0123456789", "1990-01-15")
    record2 = Record("Anna Smith", "9876543210", "1985-05-20")
    record3 = Record("Bob Johnson", "1111199999")
    record4 = Record("Tom Bombadil", "1122334455", "1995-05-20")    

    book.add_record(record1)
    book.add_record(record2)
    book.add_record(record3)
    book.add_record(record4)    

    # print(record1)
    # print(record2)
    # print(record3)
    # print(record4)
    record4.add_phone('1234567890')
    # print(record4)
    record4.remove_phone('1122334455')
    # print(record4)    

    # Input iterator of records by batches with 2 items
    # for batch in book.iterator(batch_size=10):
    #     for record in batch:
    #         print(record)
    #         if record.birthday:
    #             days = record.days_to_birthday()
    #             print(f"Days to birthday: {days} day(s)")    

    searching_phrase = input('Enter at least 2 symbols to start searching: ')
    result = book.searching(searching_phrase)
    print(result)    

    storeData(book)    
