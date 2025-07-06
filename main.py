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
# print(os.listdir('.'))
#
# def recreate_file(fileName):
#     with open(fileName, 'w', encoding='utf-8') as f:
#         f.write('Да ну!\n')
#         f.write('Это пример\n')
#
# def read_file(fileName):
#     with open(fileName, 'r', encoding='utf-8') as f:
#         content = f.read()
# def read_file_by_rows(fileName):
#     with open(fileName, 'r', encoding='utf-8') as f:
#         print('Построчное чтение')
#         for line in f:
#             print(line.strip())
#
# def walk_directory(path):
#     for root, dirs, files in os.walk(path):
#         print(f'\nТекущая Директория: {root}')
#         print('Поддиректории:', dirs)
#         print('Фалы:', files)
#
# recreate_file('example')
# walk_directory('/Users/anna/PycharmProjects/pythonProject')
# #github3

class Person:
  def __init__(self,name,age):
    self.__name = name
    self.__age = age

  def print_Person(self):
    print(f"Иия:{self.__name}\tВозраст:{self.__age}")

  @property
  def age(self):
    return self.__age

  @age.setter
  def age(self,age):
    if 0<age<110:
      self.__age = age
    else:
      print("не тот возраст")

  @property
  def name(self):
    return self.__name
  @property
  def grade(self):
    return self.__grade

  def display_info(self):
    print(f"Name:{self.__name} age:{self.__age}")




  # @name.setter
  # def name(self,name)



tom = Person("Tom",45)
tom.age = 89
tom.print_Person()
tom.display_info()
print(tom.age)


class Employee(Person):
    def __init__(self, name, age, compani):
        super().__init__(name, age)
        self.__age = age
        self.__compani = compani
    def work(self):
      print(f"{self.name}work")

    def display_info(self):
      print(f'age:{self.__age} work{self.__compani}')

bob = Employee("Bob", 35, "shop")
bob.work()
bob.display_info()

class Student(Person):
  def __init__(self, name, age, grade):
    super().__init__(name, age)
    self.__grade = grade

  def display_info(self):
    super().display_info()
    print(f'grade{self.__grade}')

