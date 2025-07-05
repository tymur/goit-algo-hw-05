class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        key_hash = self.hash_function(key)
        key_value = [key, value]

        # Перевіряємо, чи вже є bucket
        if not self.table[key_hash]:
            self.table[key_hash] = [key_value]
            return True
        else:
            # Оновлюємо значення, якщо ключ існує
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            # Якщо ключ новий, додаємо пару
            self.table[key_hash].append(key_value)
            return True

    def get(self, key):
        key_hash = self.hash_function(key)
        # Пошук пари за ключем
        if self.table[key_hash]:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    def delete(self, key):
        """Видалити пару ключ-значення з таблиці."""
        key_hash = self.hash_function(key)
        if self.table[key_hash]:
            for index, pair in enumerate(self.table[key_hash]):
                if pair[0] == key:
                    # Видаляємо пару
                    self.table[key_hash].pop(index)
                    return True
        # Ключ не знайдено
        return False

    def __str__(self):
        """Для візуалізації вмісту таблиці."""
        return str(self.table)


# Тестування функціоналу 
# Тестування додавання
H = HashTable(5)
H.insert("apple", 10)
H.insert("orange", 20)
H.insert("banana", 30)

print(H.get("apple"))    # Виведе: 10
print(H.get("orange"))   # Виведе: 20
print(H.get("banana"))   # Виведе: 30

# Тестування видалення
# Видалимо "orange"
H.delete("orange")
print(H.get("orange"))   # Виведе: None

# Спробуємо видалити неіснуючий ключ
print(H.delete("grape")) # Виведе: False

# Перевіряємо вміст таблиці
print(H)
