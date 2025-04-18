import hmac

class Hmacdict:
    # Приватные поля ключей и значений типа "list"
    __keys: list
    __values: list

    def __init__(self):
        self.__keys = []
        self.__values = []

    def my_hash(self, x):
        
        if isinstance(x, str):
            hex_digest = hmac.new(b'secret-key', x.encode('utf-8'), 'sha256').hexdigest() # Если тип x - строка, то конвертируем ее в байты, затем используем hmac с ключом 'secret-key' и переводим в 16-ричную запись
        elif isinstance(x, (int, float)):
            hex_digest = hmac.new(b'secret-key', str(x).encode('utf-8'), 'sha256').hexdigest() # Если тип x - int или float, то сначала конвертируем его в строку, затем конвертируем ее в байты, затем используем hmac с ключом 'secret-key' и переводим в 16-ричную запись
        
        return hex_digest
        
    # Возвращает значение по ключу в виде dict[key]
    def __getitem__(self, key):
        for idx, my_key in enumerate(self.__keys):
            if self.my_hash(my_key) == self.my_hash(key):
                return self.__values[idx]
        raise ValueError(f"Key {key} not found")

    # Устанавливает пару ключ, значение dict[key] = value
    def __setitem__(self, key, value):
        for idx, my_key in enumerate(self.__keys):
            if self.my_hash(my_key) == self.my_hash(key):
                self.__values[idx] = value
                return self
        self.__keys.append(key)
        self.__values.append(value)

    # Реализации функции len()
    def __len__(self):
        return len(self.__keys)
    
    # Функция для вывода словаря в консоль 
    def __repr__(self):
        if len(self.__keys) == 0:
            return "{}"
        s = "{"
        for idx, my_key in enumerate(self.__keys[:-1]):
            s += f"{my_key}: {self.__values[idx]}, "
        s += f"{self.__keys[-1]}: {self.__values[-1]}"
        s += "}"
        return s
    
    # Очищает поля класса: списки ключей и значений, возвращает None(ничего)
    def clear(self):
        self.__keys.clear()
        self.__values.clear()
        return None

    # Создает deep copy словаря 
    def copy(self):
        copy_dict = Hmacdict()
        copy_dict.__keys = self.__keys.copy()
        copy_dict.__values = self.__values.copy()
        return copy_dict

    # Возвращает список пар ключ-значение
    def items(self):
        return list(zip(self.__keys, self.__values))

    # Возвращает список ключей
    def keys(self):
        return self.__keys

    # Возвращает список значений 
    def values(self):
        return self.__values

    # Возвращает значение по ключу, если есть в словаре, если нет, то default
    def get(self, key, default = None):
        for idx, my_key in enumerate(self.__keys):
            if self.my_hash(my_key) == self.my_hash(key):
                return self.__values[idx]
        return default
    
    # Удаляет и возвращает пару ключ-значение по ключу, если и так нет, то возвращает default
    def pop(self, key, default = None):
        for idx, my_key in enumerate(self.__keys):
            if self.my_hash(my_key) == self.my_hash(key):
                del self.__keys[idx]
                return_value = self.__values[idx]
                del self.__values[idx]
                return return_value
        return default

    # Удаляет и возвращает последнюю пару ключ-значение из словаря
    def popitem(self):
        return_key = self.__keys[-1]
        return_value = self.__values[-1]
        del self.__keys[-1]
        del self.__values[-1]
        return return_key, return_value

    # Возвращает значение ключа, но если его нет, не бросает исключение, а создает ключ со значением default (по умолчанию None).
    def setdefault(self, key, default=None):
        for idx, my_key in enumerate(self.__keys):
            if self.my_hash(my_key) == self.my_hash(key):
                return self.__values[idx]
        self.__keys.append(key)
        self.__values.append(default)
        return default

    # Создает словарь с ключами из seq и значением value (по умолчанию None).
    @classmethod
    def fromkeys(cls, seq, value=None):
        new_dict = cls()
        for key in seq:
            new_dict[key] = value
        return new_dict
    
    # Обновляет словарь, добавляя пары (ключ, значение) из other. Существующие ключи перезаписываются. Возвращает None (не новый словарь!).
    def update(self, other):
        for item in other.items():
            self.setdefault(*item)
            for my_key in self.__keys:
                if self.my_hash(item[0]) == self.my_hash(my_key):
                    self[my_key] = item[1]
        return None

mydict = Hmacdict()

mydict["apple"] = 5
mydict["banana"] = 6
mydict["pineapple"] = 9
mydict["peach"] = 5

mydict.get("banana", "fruit")
mydict.get("strawberry", "berry")

mydict.setdefault("strawberry", 10)

print(mydict)
print(mydict.items())
print(mydict.keys())
print(mydict.values())

Hmacdict.fromkeys(["first", "second", "third", "fourth"], [1, 2, 3, 4])

dict_2 = Hmacdict()
dict_2[9] = 9
dict_2[6] = 6
dict_2[10] = 10
mydict.update(dict_2)
print(mydict)

mydict.popitem()
print(mydict)
