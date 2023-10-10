from flask import Flask, request, jsonify
import os
import pickle
app = Flask(__name__)

# Имитация базы данных

users = []

# Регистрация пользователя
@app.route('/register', methods=['POST'])
def register():
    # Получение данных пользователя из запроса
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    # Проверка уникальности имени пользователя
    for user in users:
        if user['username'] == username:
            return jsonify({'message': 'Имя пользователя уже занято'})
          
    # Добавление пользователя в базу данных
    users.append({'username': username, 'password': password, 'friends': [], 'messages':[], 'online':False})
    
    return jsonify({'message': 'Регистрация прошла успешно'})

# Авторизация пользователя
@app.route('/login', methods=['POST'])
def login():
    # Получение данных пользователя из запроса
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    # Поиск пользователя в базе данных
    for user in users:
        if user['username'] == username and user['password'] == password and user['online'] == False:
            user['online']=True
            return jsonify({'status':True})
    
    return jsonify({'status':False})

@app.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    username = data['username']
    for user in users:
        if user['username'] == username and user['online'] == True:
            user['online']=False
            return jsonify({'status':True})
    return jsonify({'status':False})
# Добавление друзей
@app.route('/add_friend', methods=['POST'])
def add_friend():
    # Получение данных пользователя из запроса
    data = request.get_json()
    user1 = data['user1']
    user2 = data['user2']
    
    # Поиск пользователей в базе данных
    user1_found = False
    user2_found = False
    for user in users:
        if user['username'] == user1:
            user1_found = True
        if user['username'] == user2:
            user2_found = True
            
    # Проверка существования пользователей
    if not user1_found or not user2_found:
        return jsonify({'message': 'Один или оба пользователя не найдены'})
    
    # Добавление друзей
    for user in users:
        if user['username'] == user1:
            if user2 in user['friends']:
                return jsonify({'message': 'Пользователь уже в друзьях с вами'})
            user['friends'].append(user2)
        if user['username'] == user2:
            user['friends'].append(user1)
    return jsonify({'message': 'Друг добавлен успешно'})

# Отправка сообщения
@app.route('/send_message', methods=['POST'])
def send_message():
    # Получение данных сообщения из запроса
    data = request.get_json()
    sender = data['sender']
    receiver = data['receiver']
    message = data['message']
    
    # Поиск отправителя и получателя в базе данных
    sender_found = False
    receiver_found = False
    for user in users:
        if user['username'] == sender:
            sender_found = True
        if user['username'] == receiver:
            receiver_found = True
    
    # Проверка существования отправителя и получателя
    if not sender_found or not receiver_found:
        return jsonify({'message': 'Один или оба пользователя не найдены'})
    for user in users:
        if user['username'] == sender:
            user['messages'].append({'sender':sender, 'message': message, 'receiver': receiver})
        if user['username'] == receiver:
            user['messages'].append({'sender':sender, 'message': message, 'receiver': receiver})

    # Здесь можно добавить операции для сохранения сообщения
    
    return jsonify({'message': 'Сообщение отправлено успешно'})

@app.route('/get_messages', methods=['POST'])
def get_messages():
    data = request.get_json()
    username = data['username']
    for user in users:
        if user['username'] == username:
            user_messages = user['messages']
            return jsonify({'messages': user_messages})
    return jsonify({'message': 'Пользователь не найден'})

@app.route('/get_friends', methods=['POST'])
def get_friends():
    data = request.get_json()
    username = data['username']
    for user in users:
        if user['username'] == username:
            user_friends = user['friends']
            return jsonify({'friends': user_friends})
    return jsonify({'message': 'Пользователь не найден'})
    
@app.route('/get_messages_by_user', methods=['POST'])
def get_messages_by_user():
    data = request.get_json()
    username = data['username']
    target = data['target']
    messages = []
    flag = False

    for user in users:
        if user['username'] == username:
            user_messages = user['messages']
            flag = True
            break
    if flag:
        for msg in user_messages:
            if msg['sender'] == username or msg['receiver'] == target or msg['sender'] == target or msg['receiver'] == username:
                messages.append(msg)
        return jsonify({'messages': messages})
    else:
        return jsonify({'message': 'Пользователь не найден'})
    
def init_db(filename):
    if os.path.exists(filename):
        # Если файл существует, читаем из него список пользователей
        with open(filename, 'rb') as file:
            return pickle.load(file)
    else:
        # Если файла нет, создаем пустой список пользователей
        return []
    
def safe_db(filename, users):
    with open(filename, 'wb') as file:
        pickle.dump(users, file)

if __name__ == '__main__':
    db = 'db.txt'
    users = init_db(db)
    app.run()
    safe_db(db, users)
