class Person:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return self.name + ', ' + str(self.age)


p1 = Person('mario', 12)
print(p1)


# non si puo' mettere una classe e una sua subclass in un unico file

class Employee(Person):

    def __init__(self, name, age, id):
        super().__init__(name, age)
        self.id = id

    def __str__(self):
        return super().__str__() + ' - ' + str(self.id)


if __name__ == '__main__':
    e1 = Employee('marco', 41, 120)
    print(e1)