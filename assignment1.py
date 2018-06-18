# Assignment #1

user_age = 0
user_name = ""

def user_info(u_age=1, u_name="Nobody"):
    print ("Hello " + u_name + ". I see that your age is " + u_age)
    print ("I see that you have lived " + str(decades(u_age)) + " decades.")

def decades(u_age):
    decades_lived = int(u_age) // 10
    return decades_lived

u_name = input("What is your name? ")
u_age = input("How are you? ")

user_info(u_age, u_name)
#decades(u_age)