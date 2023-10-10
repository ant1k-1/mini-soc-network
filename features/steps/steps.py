from behave import *
from flask_testing import *
import requests
import sys
sys.path.append("C:\\Users\\Aidar\\OneDrive\\Рабочий стол\\mini-soc-network")
from client import User

@given('пользователь "{username}" уже зарегистрирован')
def step_given_user_already_registered(context, username):
    user = User()
    user.register(username, "defaultpassword")

@given('пользователь "{username}" зарегистрирован с паролем "{password}"')
def step_given_user_registered_with_password(context, username, password):
    user = User()
    user.register(username, password)

@given('пользователь "{username}" авторизован')
def step_given_user_is_logged_in(context, username):
    context.user = User()
    context.user.login(username, "defaultpassword")

@when('я регистрируюсь с именем "{username}" и паролем "{password}"')
def step_register_with_username_and_password(context, username, password):
    context.user = User()
    context.response_message = context.user.register(username, password)

@when('я вхожу с именем "{username}" и паролем "{password}"')
def step_login_with_username_and_password(context, username, password):
    context.user = User()
    context.response_message = context.user.login(username, password)

@when('я добавляю друга с именем "{friend_name}"')
def step_add_friend_with_name(context, friend_name):
    context.response_message = context.user.add_friend(friend_name)

@when('я отправляю сообщение "{message}" пользователю "{receiver}"')
def step_send_message_to_receiver(context, message, receiver):
    context.response_message = context.user.send_message(receiver, message)

@when('я просматриваю все мои сообщения')
def step_view_all_my_messages(context):
    context.response_message = context.user.get_messages()

@when('я просматриваю переписку с пользователем "{target}"')
def step_view_conversation_with_user(context, target):
    context.response_message = context.user.get_messages_by_user(target)

@then('я получаю ответ "{expected_response}"')
def step_check_response_message(context, expected_response):
    assert context.response_message == expected_response, f"Expected '{expected_response}', but got '{context.response_message}'"

