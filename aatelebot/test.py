from tg_bot import Group
import shelve
path_ =  'D:\\py3eg\\tgbots\\aatelebot\\aatelebot\\'

obj = {
"id": 179161054,
"name": "мемы для любителей лизать пизду",
"screen_name": "pussyloverz",
"is_closed": 0,
"type": "page",
"is_admin": 0,
"is_member": 1,
"is_advertiser": 0
}
a = Group(obj)
print(a)
with shelve.open(path_ + 'test', flag = 'n') as file:
    file['group'] = a
print(a)
a = None

with shelve.open(path_ + 'test', flag = 'r') as file:
    a = file['group']

print(a)