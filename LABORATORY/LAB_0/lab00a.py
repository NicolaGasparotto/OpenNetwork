def ex1():
    num1 = int(input('Enter first number: '))
    num2 = int(input('Enter second number: '))
    prod = num1*num2
    result = ( prod if prod < 1000 else num1+num2 )
    print(result)

def ex2():
    start  = 0
    sum = 0
    for i in range(start, 10):
        print(i, sum)
        sum += i
    print(sum)

def ex3():
    int_list = [1, 3, 4, 6, 9, 1, 10]
    same = (True if int_list[0] == int_list[-1] else False)
    print(same)

def ex4():
    int_list = [1, 20, 5, 33, 41]
    for num in int_list:
        if num % 5 == 0:
            print(num)

def ex5():
    s1 = "Emma is a good developer. Emma is also a writer"
    search = "Emma"
    str_list = s1.split() # di default lo split e' lo space
    count = 0

    for str in str_list:
        #print(str)
        if str == search:
            count += 1

    print("String ", search, " appeared ", count, " times")

def ex6():
    list1 = [12, 43, 3, 2, 10]
    list2 = [6, 1, 89, 12, 17]
    list3 = []

    for num in list1:
        if num % 2 != 0:
            list3.append(num)
    for num in list2:
        if num % 2 == 0:
            list3.append(num)
    print(list3)

def ex7():
    s1 = "Propro"
    s2 = "Miao"
    mezzoIstr = int(len(s1)/2)   # sarebbe un float di default
    #print(type(mezzIstr))
    s3 = s1[:mezzoIstr] + s2 + s1[mezzoIstr:]
    print(s3)

def ex8():
    s1 = "Casa"
    s2 = "Merio"
    middle1 = int(len(s1)/2)
    middel2 = int(len(s2)/2)
    s3 = s1[0] + s2[0] + s1[middle1] + s2[middel2] + s1[-1] + s2[-1]
    print(s3)

def ex9():
    s1 = input("Enter a string: ")
    lower_count = 0
    upper_count = 0
    digit_count = 0
    special_count = 0

    for c in s1:
        if c.islower():
            lower_count+=1
        elif c.isupper():
            upper_count+=1
        elif c.isnumeric():
            digit_count+=1
        else:
            special_count+=1
    print(f"Lower Case = {lower_count}\t Upper = {upper_count}\t "
          f"Digits = {digit_count}\t Special = {special_count}")

def ex10():
    s1 = "Welcome to USA. aWESOME uSA, isn't it?"
    substr = "usa"
    #s1 = s1.lower()
    # substr.lower()
    countRip = s1.lower().count(substr.lower())
    print(f"{substr} is repeated {countRip} times")


# in questo modo questo pezzo di codice viene runnato solo dentro questo modulo e non anche da altri moduli
# nel caso in cui dovessi importarlo in altri
if __name__ == "__main__":
    ex10()


