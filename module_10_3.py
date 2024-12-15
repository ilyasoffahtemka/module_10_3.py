import threading
from random import randint
from time import sleep

class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()  # Блокировка для синхронизации потоков

    def deposit(self):
        for _ in range(100):  # Совершаем 100 транзакций пополнения
            amount = randint(50, 500)  # Случайная сумма для пополнения
            with self.lock:  # Блокируем доступ к балансу
                self.balance += amount
                print(f"Пополнение: {amount}. Баланс: {self.balance}")
                if self.balance >= 500 and self.lock.locked():  # Если баланс >= 500, разблокируем
                    self.lock.release()
            sleep(0.001)  # Имитируем задержку

    def take(self):
        for _ in range(100):  # Совершаем 100 транзакций снятия
            amount = randint(50, 500)  # Случайная сумма для снятия
            print(f"Запрос на {amount}")
            with self.lock:  # Блокируем доступ к балансу
                if amount <= self.balance:  # Если хватает средств
                    self.balance -= amount
                    print(f"Снятие: {amount}. Баланс: {self.balance}")
                else:  # Если недостаточно средств
                    print("Запрос отклонён, недостаточно средств")
                    self.lock.acquire()  # Блокируем поток
            sleep(0.001)  # Имитируем задержку


# Создаем объект банка
bk = Bank()

# Создаем потоки для пополнения и снятия
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

# Запускаем потоки
th1.start()
th2.start()

# Ожидаем завершения потоков
th1.join()
th2.join()

# Итоговый баланс
print(f"Итоговый баланс: {bk.balance}")