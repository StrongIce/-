import requests
import random
# oauth.yandex.ru/authorize?response_type=token&client_id=Ваш_id
#Получить токен своего приложения

tokens = {
    'contoso.com': 'Token',
    'contoso1.com' : "Token"
}

fname = input("Имя: ")
last = input("Фамилия: ")

#Транслитируем в английский и генерируем логин
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


#Получаем логин
login = make_login(fname,last)

#Генерируем пароль
def gen_pass():
    chars = '+-/*!&$#?=w@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    lenght = 8
    password = ''
    for i in range(lenght):
        password += random.choice(chars)
    return password

def get_departaments():
    headers = {
        'Content-type': 'application/json',
        'Authorization': f"OAuth {tokens['contoso.com']}"
    }
    params = {
        'fields': 'name'
    }
    response = requests.get('https://api.directory.yandex.net/v6/departments/',params=params, headers=headers)
    response_data = response.json()
    results = response_data['result']
    results = {
        department['name']: department['id']
        for department in results
    }
    return results

#Создаем пользователя
def creat_user_mail(fname,last,login):
    password = gen_pass()
    headers = {
        'Content-type': 'application/json',
        'Authorization': f"OAuth {tokens['contoso.com']}"
    }
    data = {
        "nickname": f"{login}",
            "name" : {
            "first": f"{fname}",
            "last": f"{last}",
        },
        "department_id": 18,
        "password": f"{password}"
    }

    response = requests.post('https://api.directory.yandex.net/v6/users/', headers=headers, json=data)
    email = response.json()['email']
    info = {'Логин':f'{email}','Пароль': f'{password}'}
    return info

print(creat_user_mail(fname,last,login))
