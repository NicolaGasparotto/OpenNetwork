var = 'Bob'
print(type(var))

msg = "I'm not so good at it " + str(21)
print(msg)

tot = 10.9  # i numeri con la virgola -> il punto
print(tot)
tot = int(tot)
print(tot, type(tot))

# age = int(input("Enter your age: "))
# print(age, type(age))

int_value = 12
float_value = float(int_value)
print(float_value, "\n", type(float_value))

winner = None
print(winner is None)

print()
weather = 'sunny'
temperature = 'cold'
status = ("happy" if weather == 'sunny' and temperature == 'hot' else "in a bad mood")
print(status)

for i in range(0, 10):
    print(i, ' ', end='')
print('\nDone')

print('With an increment of 2 each step')
for i in range(0, 10, 2):
    print(i, ' ', end='')
print('\nDone')

# if not interested in hte value of the loop but only in looping itself a NTIMES
for _ in range(1, 11):
    # stampa 10 valori perchè iterna N volte - 1 estremo a dx escluso
    print('.', end='')
print('\nDone')


def funct_prov():
    """This is a doc string
       write the body of a function 4 space after the start -> NOT USE TAB"""
    """It can be used also 
       to do comment on multiple lines at will """


def multiply(a, b):
    return a * b


def multby(func, num):
    return lambda y: func(num, y)


double = multby(multiply, 2)
triple = multby(multiply, 3)

print(double(5))
print(triple(5))

