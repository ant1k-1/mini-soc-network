import requests
import json
import os
clear = lambda: os.system('cls')
pause = lambda: os.system('pause')
class User:
    def __init__(self) -> None:
        self.username = ''
        self.password = ''
        self.logged = False
    # Метод регистрации пользователя
    def register(self, username, password):
        # Определение данных пользователя
        data = {'username': username, 'password': password}
        
        # Отправка POST-запроса на серверный маршрут /register
        response = requests.post('http://localhost:5000/register', json=data)
        
        # Печать ответа сервера
        return response.json()['message']

    # Метод авторизации пользователя
    def login(self, username, password):
        # Определение данных пользователя
        data = {'username': username, 'password': password}
        
        # Отправка POST-запроса на серверный маршрут /login
        response = requests.post('http://localhost:5000/login', json=data)
        if response.json()['status']==True:
            self.username=username
            self.password=password
            self.logged = True
            return 'Авторизация прошла успешно'
        else:
            return 'Неверное имя пользователя или пароль, либо вы авторизованы на другом устройстве'
    # Метод выхода пользователя
    def logout(self):
        data = {'username': self.username}
        response = requests.post('http://localhost:5000/logout', json=data)
        if response.json()['status']==True:
            self.username=''
            self.password=''
            self.logged=False
            return 'Вы вышли из профиля'
        else:
            return 'Что-то пошло не так'
    # Функция добавления друга
    def add_friend(self, user2):
        if not self.logged:
            return 'Вы не авторизованы'
        # Определение данных пользователей для добавления друзей
        data = {'user1': self.username, 'user2': user2}
        
        # Отправка POST-запроса на серверный маршрут /add_friend
        response = requests.post('http://localhost:5000/add_friend', json=data)
        
        # Печать ответа сервера
        return response.json()['message']

    # Метод отправки сообщения
    def send_message(self, receiver, message):
        if not self.logged:
            return 'Вы не авторизованы'
        # Определение данных сообщения
        data = {'sender': self.username, 'receiver': receiver, 'message': message}
        
        # Отправка POST-запроса на серверный маршрут /send_message
        response = requests.post('http://localhost:5000/send_message', json=data)
        
        # Печать ответа сервера
        return response.json()['message']
    
    # Метод просмотра всех сообщений
    def get_messages(self):
        if not self.logged:
            return 'Вы не авторизованы'
        data = {'username': self.username}
        # Отправка POST-запроса на серверный маршрут /add_friend
        response = requests.post('http://localhost:5000/get_messages', json=data)
        messages = response.json()['messages']
        string = "---------------------------------------------------------------\n"
        for msg in messages:
            if msg['sender'] == self.username:
                string +="Я: "+msg['message']
            else:
                string +=msg['sender'] + ": " + msg['message']
            string +="\n---------------------------------------------------------------\n"
        return string
    # Метод просмотра всех друзей
    def get_friends(self):
        if not self.logged:
            return 'Вы не авторизованы'
        data = {'username': self.username}
        # Отправка POST-запроса на серверный маршрут /add_friend
        response = requests.post('http://localhost:5000/get_friends', json=data)
        friends = response.json()['friends']
        string = "Друзья:\n"
        for f in friends:
            string += f
        return string
        
    
    # Метод просмотра диалога с пользователем
    def get_messages_by_user(self, target):
        if not self.logged:
            return 'Вы не авторизованы'
        data = {'username': self.username, 'target': target}
        response = requests.post('http://localhost:5000/get_messages_by_user', json=data)
        messages = response.json()['messages']
        string = "---------------------------------------------------------------\n"
        for msg in messages:
            if msg['sender'] == self.username:
                string +="Я: "+msg['message']
            else:
                string +=msg['sender'] + ": " + msg['message']
            string +="\n---------------------------------------------------------------\n"
        return string

    # Основной цикл интерфейса
    def run(self):
        while True:
            clear()
            if len(self.username) != 0: print(f'Вы авторизованы как "{self.username}"')
            else: print('Вы не авторизованы')
            print('Выберите действие:')
            print('1. Зарегистрироваться')
            print('2. Войти в систему')
            print('3. Добавить друга')
            print('4. Отправить сообщение')
            print('5. Выйти из профиля')
            print('6. Проверить сообщения')
            print('7. Вывести друзей')
            print('8. Показать переписку с пользователем')
            print('9. Закрыть программу')
            
            choice = input()
            
            if choice == '1':
                username = input('Введите имя пользователя: ')
                password = input('Введите пароль: ')
                print(self.register(username, password))
            elif choice == '2':
                username = input('Введите имя пользователя: ')
                password = input('Введите пароль: ')
                print(self.login(username, password))
            elif choice == '3':
                friend = input('Введите имя пользователя: ')
                print(self.add_friend(friend))
            elif choice == '4':
                receiver = input('Введите получателя: ')
                message = input('Введите сообщение: ')
                print(self.send_message(receiver, message))
            elif choice == '5':
                print(self.logout())
            elif choice == '6':
                print(self.get_messages())
            elif choice == '7':
                print(self.get_friends())
            elif choice == '8':
                target = input('Введите имя пользователя: ')
                print(self.get_messages_by_user(target))
            elif choice == '9':
                print(self.logout())
                break
            pause()
        

if __name__ == '__main__':
    user = User()
    try:
        user.run()
    except Exception:
        user.logout()
