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
        roll_no = input("enter roll_no to get details :-")
        for i in data["students"]:
            if i["roll_no"]== roll_no:
                print("name : ", i["name"])
                print("age : ", i["age"])
                print("email : ", i["email"])
                print("roll_no : ", i["roll_no"])
                print("grades : ", i["grades"])
                avg =sum(i["grades"].values())/len(i["grades"]) if i["grades"] else 0
                print("average = " ,avg)
                return
        print("student not found")


    def add_grade(self):
        roll_no = input("enter your roll_no :- ")
        subject = input("subject :- ")
        marks = int(input("mark :-")) 
        
        for i in data["students"]:
            if i["roll_no"] == roll_no:
                i["grades"][subject] = marks
                save()
                print("grade added succesfully")
                return
        print("student not found")

            

        

class Teacher(person):
    def set_roles(self):
        return "teacher"
    
    def register(self):
        name = input("enter your name :-")
        age = int(input("enter your age :- "))
        email = input("enter your email :- ")
        subject = input("enter subject :- ")
        emp_id = input("enter your emp_id :- ")

        if not person.validate_email(email):
            print("invalid email")
            return 
        for i in data["teachers"]:
            if i["emp_id"] == emp_id:
                print("already registered")
                return
            else:
                pass
        
        data["teachers"].append({
            "name" : name,
            "age" : age,
            "email" : email,
            "subject" : subject,
            "emp_id" : emp_id 
            })
        save()
        print(f" teacher {name} has registered")



    def show_details(self):
        emp_id = input("enter empid :- ")
        for i in data["teachers"]:
            if i["emp_id"] == emp_id:
                print("name : ", i["name"])
                print("age : ", i["age"])
                print("email : ", i["email"])
                print("emp_id : ", i["emp_id"])
                return
        print("teacher not found")
    
    



stud = student()
teacher = Teacher()

print("press 1 to register student")
print("press 2 to register teacer ")
print("press 3 to  add grades")
print("press 4 to view student grades")
print("press 5  to view teacher info")

choice = int(input("please tell your choice :- "))

if choice ==1:
    stud.register()
elif choice ==2:
    teacher.register()
elif choice == 3:
    stud.add_grade()
elif choice == 4:
    stud.show_details()
elif choice == 5:
    teacher.show_details()