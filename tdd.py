import unittest
from client import User

class YourTestClass(unittest.TestCase):

    def setUp(self):
        self.your_class = User()
    #Успешная регистрация
    def test1_register(self):
        # каждый раз надо менять содержимое бд на
        # Ђ•Q       ]”}”(Њusername”Њaidar”Њpassword”Њaidar”Њ friends”]”Њmessages”]”Њonline”‰ua.
        response = self.your_class.register('user', 'user')
        self.assertEqual(response, 'Регистрация прошла успешно')
        response = self.your_class.register('user1', 'user1')
        self.assertEqual(response, 'Регистрация прошла успешно')
        response = self.your_class.register('user2', 'user2')
        self.assertEqual(response, 'Регистрация прошла успешно')

    # Успешный вызов функции при успешном логине
    def test2_inlogin(self):
        response = self.your_class.login('user', 'user')
        self.assertEqual(response, 'Авторизация прошла успешно')
        response = self.your_class.add_friend('user1')
        self.assertEqual(response, 'Друг добавлен успешно')
        response = self.your_class.add_friend('user1')
        self.assertEqual(response, 'Пользователь уже в друзьях с вами')
        response = self.your_class.send_message('user2', 'Privet')
        self.assertEqual(response, 'Сообщение отправлено успешно')
        response = self.your_class.get_messages()
        self.assertEqual(response, '---------------------------------------------------------------\nЯ: Privet\n---------------------------------------------------------------\n')
        response = self.your_class.get_friends()
        self.assertEqual(response, 'Друзья:\nuser1')
        response = self.your_class.get_messages_by_user('user2')
        self.assertEqual(response, '---------------------------------------------------------------\nЯ: Privet\n---------------------------------------------------------------\n')
        response = self.your_class.logout()
        self.assertEqual(response, 'Вы вышли из профиля')

    # Ошибочный вызов функции при успешном логине
    def test3_wrong_inlogin(self):
        response = self.your_class.login('user', 'user')
        self.assertEqual(response, 'Авторизация прошла успешно')
        response = self.your_class.add_friend('user3')
        self.assertEqual(response, 'Один или оба пользователя не найдены')
        response = self.your_class.send_message('user3', 'Privet')
        self.assertEqual(response, 'Один или оба пользователя не найдены')
        response = self.your_class.logout()
        self.assertEqual(response, 'Вы вышли из профиля')
        
    #Ошибочный выход из акка
    def test4_wrong_logout(self):
        response = self.your_class.logout()
        self.assertEqual(response, 'Что-то пошло не так')

    # Ошибочный вход в акк
    def test5_wrong_login(self):
        response = self.your_class.login('wrong_user', 'wrong_password')
        self.assertEqual(response, 'Неверное имя пользователя или пароль, либо вы авторизованы на другом устройстве')

    # Ошибочная регистрация
    def test6_wrong_register(self):
        response = self.your_class.register('aidar', 'aidar')
        self.assertEqual(response, 'Имя пользователя уже занято')

    # Ошибочная отправка сообщения
    def test7_wrong_sendMes(self):
        response = self.your_class.send_message('user2', 'Privet')
        self.assertEqual(response, 'Вы не авторизованы')

    # Ошибочное добавление в друзья
    def test8_wrong_addFr(self):
        response = self.your_class.add_friend('user2')
        self.assertEqual(response, 'Вы не авторизованы')

    # Ошибочное получение сообщений
    def test90_wrong_getMes(self):
        response = self.your_class.get_messages()
        self.assertEqual(response, 'Вы не авторизованы')

    # Ошибочное получение друзей
    def test91_wrong_getFriend(self):
        response = self.your_class.get_friends()
        self.assertEqual(response, 'Вы не авторизованы')

    # Ошибочное получение сообщений определенным пользователям
    def test92_wrong_getMesByUser(self):
        response = self.your_class.get_messages_by_user('user2')
        self.assertEqual(response, 'Вы не авторизованы')

if __name__ == '__main__':
    unittest.main()