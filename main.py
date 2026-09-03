import json
from pathlib import Path
from abc import ABC , abstractmethod

"""database"""

database = "school_data.json"

data ={"students" : []  , "teachers" : []  }

if Path(database).exists():
    with open(database,'r') as f:
        content = f.read()
        if content:
            data = json.loads(content)
            print(" database loaded ")
        else:
            print("database is empty ")

def save():
    with open(database,'w') as f:
        json.dump(data,f,indent=4)
        print("data saved")



class person(ABC):
    @abstractmethod
    def set_roles(self):
        pass

    @abstractmethod
    def register(self):
        pass
    
    @abstractmethod
    def show_details(self):
        pass

    @staticmethod
    def validate_email(email):
        if '@' in email and '.' in email:
            return True  
        else:
            return False


   

class student(person):
    def set_roles(self):
        return "student"

    def register(self):
        name = input("enter your name :-")
        age = int(input("enter your age :- "))
        email = input("enter your email :- ")
        roll_no = input("enter your roll_no :- ")

        if not person.validate_email(email):
            print("invalid email")
            return 
        
        for i in data["students"]:
            if i["roll_no"] == roll_no:
                print("already registered")
                return
            else:
                pass
        data["students"].append({
            "name" : name,
            "age" : age,
            "email" : email,
            "roll_no" :roll_no,
            "grades" : {} 
            })
        save()
        print(f" student {name} has registered")
    
    def show_details(self):
        pass
        
    
    



stud = student()

print("press 1 to register student")
print("press 2 to register teacer ")
print("press 3 to  add grades")
print("press 4 to view student grades")
print("press 5  to view teacher info")

choice = int(input("please tell your choice :- "))

if choice ==1:
    stud.register()