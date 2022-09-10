# Python function to validate an Email
import datetime
import re


def email_check(email: str):
    # pass the regular expression and the string into the fullmatch() method
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(pattern, email)):
        return email
    else:
        print("Invalid Email")


def phone_check(phone: str):
    pattern = re.compile("[+](380)?[5-9][0-9]{8}")
    if(pattern.match(phone)):
        return phone
    else:
        print("Invalid Number")


def email_extractor(target):
    lst = re.findall('\S+@\S+', target)
    print(lst)
    return lst


# if __name__ == '__main__':

#     # calling run function
#     email_check("ankitrai326@gmail.com")
#     email_extractor("Ghheh ksds khhh@i.ua sdsd ks sdsdfdf15 yuko123@gm.com")
#     phone_check("+380968585858")


x = datetime.datetime.now().date()
print(x)
