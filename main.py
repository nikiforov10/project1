# name = input()
# result = {}
# spisok = []
# for i in range(len(name)):
#     spisok.append(name[i])
# for elem in spisok:
#     result[elem] = spisok.count(elem)
# print(result)

#глобальная локальная нелокальная встроенная
# l = int(input())
# r = int(input())
# result = 0
# def rec_fib(n):
#     if 0 < n <= 2:
#         return 1
#     else:
#         return rec_fib(n - 1) + rec_fib(n - 2)
#
#
# def f2(l, r):
#     global result
#     for i in range(r - l + 1):
#         result += rec_fib(l + i)
# print(result)
import os


# current_dir = os.getcwd()
# print(current_dir)
# os.chdir('/Users/anna/PycharmProjects')
# print(os.getcwd())
print(os.listdir('.'))

def recreate_file(fileName):
    with open(fileName, 'w', encoding='utf-8') as f:
        f.write('Да ну!\n')
        f.write('Это пример\n')

def read_file(fileName):
    with open(fileName, 'r', encoding='utf-8') as f:
        content = f.read()
def read_file_by_rows(fileName):
    with open(fileName, 'r', encoding='utf-8') as f:
        print('Построчное чтение')
        for line in f:
            print(line.strip())

def walk_directory(path):
    for root, dirs, files in os.walk(path):
        print(f'\nТекущая Директория: {root}')
        print('Поддиректории:', dirs)
        print('Фалы:', files)

recreate_file('example')
walk_directory('/Users/anna/PycharmProjects/pythonProject')