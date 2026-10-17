import random
import string

def chek_in(username, passworld):
    true_user = 'Wandee'
    true_pass = '123456'

    if username == true_user and passworld == true_pass:
        return ("Passworld is correct and wellcom to your email")
    else:
        return("Sorry your passworld is not correct")

print('====Pleas login====')
my_username = input('Enter your username')
my_passworld = input('Enter your passworld')


result = chek_in(my_username, my_passworld)
print(result)
