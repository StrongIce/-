from ldap3 import Server, Connection, SIMPLE, SYNC, ASYNC, SUBTREE, ALL, MODIFY_REPLACE,extend
import requests
import random
# oauth.yandex.ru/authorize?response_type=token&client_id=Ваш_id
#Получить токен своего приложения
tokens = {
    'contoso.com': 'token',
    'contoso2.com' : "token"
}

fname = input("Имя: ")
last = input("Фамилия: ")
group = int(input("Группа: \n1. Воробьев \n2. Титов \n3. Шимин \n4. Юсупова \n5. Дайлер \n"))
phone = input('Номер телефона: ')
base_ou = 'ou=Взыскание,ou=3,ou=EKA,dc=corp,dc=ru'

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

mail = creat_user_mail(fname,last,login)
print(mail)

if group == 1:
        base_dn = f"ou=Группа Воробьева,{base_ou}"
        base_adgroup = {
                'Взыскание JM' : 'cn=Взыскание JM,cn=Builtin,dc=corp,dc=ru',
                '2 ступень (Воробьев)' : f'cn=2 ступень (Воробьев),{base_dn}'
        }
elif group == 2:
        base_dn = f'ou=Группа Титова,{base_ou}'
        base_adgroup = {
                'Взыскание JM' : 'cn=Взыскание JM,cn=Builtin,dc=corp,dc=ru',
                '1 ступень Титов' : f'cn=1 ступень(Титов),{base_dn}'
        }
elif group == 3:
        base_dn = f'ou=Группа Шимина,{base_ou}'
        base_adgroup = {
                'Взыскание JM' : 'cn=Взыскание JM,cn=Builtin,dc=corp,dc=ru',
                '2 ступень (Шимин)' : f'cn=2 ступень (Шимин),{base_dn}'
        }
elif group == 4:
        base_dn = f'ou=Группа Юсуповой,{base_ou}'
        base_adgroup = {
                'Взыскание JM' : 'cn=Взыскание JM,cn=Builtin,dc=corp,dc=ru',
                '1 ступень (Юсупова)' : f'cn=1 ступень (Юсупова),{base_dn}'
        }
elif group == 5:
        base_dn = f'ou=Дайлер,{base_ou}'
        base_adgroup = {
                'Взыскание JM' : 'cn=Взыскание JM,cn=Builtin,dc=corp,dc=ru',
                '1 ступень Титов' : 'cn=1 ступень(Титов),ou=Группа Титова,ou=Взыскание,ou=3,ou=EKA,dc=corp,dc=ru'
        }



user_data = {
        "login": login,
        'mail': mail['Логин'],
        'firstname': fname,
        'lastname' : last,
        'dn': f"cn={last} {fname},{base_dn}",
        'phone': phone
}



def create_ad_user(data,group):
        ad_domain = '1.1.1.1'
        ad_admin = 'CONtOSO\g_admin'
        ad_password = "admin"
        srv = Server(ad_domain, use_ssl=True, port=636)  # Адрес домена, шифрование, порт
        c = Connection(srv, ad_admin, ad_password)
        c.bind() 
        #Создаем юзвера
        useradd = c.add(data['dn'], 'user', 
                {'sAMAccountName': data['login'], 
                'userPrincipalName': data['login'] + "@corp.ru",
                'givenName': data['firstname'], 
                'sn': data['lastname'], 
                'displayName': f"{data['lastname']} {data['firstname']}",
                'telephoneNumber': data['phone'],
                'mail': data['mail']
                })

        if useradd == True:
                passwd = c.extend.microsoft.modify_password(data['dn'], old_password=None, new_password='345ERTert')
                for cn_group in group.values():
                        c.extend.microsoft.add_members_to_groups(data['dn'],cn_group)
                if passwd == True:
                        c.modify(data['dn'], {'userAccountControl': (MODIFY_REPLACE, [512])})
                        c.modify(data['dn'], {'pwdLastSet': (MODIFY_REPLACE, [0])})
                        c.unbind()
                        return True
                else:
                        return 'Не удалось задать пароль'
        else:
                return useradd


print(create_ad_user(user_data,base_adgroup))



       

