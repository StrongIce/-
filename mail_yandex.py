# -*- coding:utf -8 -*-
#!/usr/bin/python3
import requests
import random


name = input("Имя: ")
fname = input("Фамилия: ")

#Транслит
def make_login(name,fname):
    login = f"{fname}_{list(name)[0]}"
    dict = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e',
      'ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
      'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h',
      'ц':'c','ч':'cz','ш':'sh','щ':'scz','ъ':'','ы':'y','ь':'','э':'e',
      'ю':'u','я':'ja', 'А':'a','Б':'b','В':'v','Г':'g','Д':'d','Е':'e','Ё':'e',
      'Ж':'zh','З':'z','И':'i','Й':'i','К':'k','Л':'l','М':'m','Н':'n',
      'О':'o','П':'p','Р':'r','С':'s','Т':'t','У':'u','Ф':'f','x':'h',
      'Ц':'c','Ч':'cz','Ш':'sh','Щ':'sch','Ъ':'','Ы':'y','Ь':'','Э':'e',
      'Ю':'u','Я':'ya',',':'','?':'',' ':'_','~':'','!':'','@':'','#':'',
      '$':'','%':'','^':'','&':'','*':'','(':'',')':'','-':'','=':'','+':'',
      ':':'',';':'','<':'','>':'','\'':'','"':'','\\':'','/':'','№':'',
      '[':'',']':'','{':'','}':'','ґ':'','ї':'', 'є':'','Ґ':'g','Ї':'i',
      'Є':'e', '—':''}        

    for key in dict:
      login = login.replace(key, dict[key])
    return login

#Получаем логин из имени и фамилии
login = make_login(name,fname)

#Генерируем пароль
def gen_pass():
    chars = '+-/*!&$#?=w@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    lenght = 8
    password = ''
    for i in range(lenght):
        password += random.choice(chars)
    return password

#Создаем юзера на яндекс почте
def create_mail_user(name,fname,login):
    passsord = gen_pass()
    domain = "contoso.com"
    headers = {
    'PddToken': 'Token',
    }
    data = {
        'domain': f"{domain}",
        "page": "2",
        'login': f'{login}',
        'password': f'{passsord}',
        'iname': f'{name}',
        'fname': f'{fname}' 
    }
    response = requests.post('https://pddimp.yandex.ru/api2/admin/email/add', headers=headers, data=data)

    return f"Логин: {response.json()['login']} \nПароль: {passsord}"


print(create_mail_user(name,fname,login))




