from appclasses import *
import sys
import os
d = db()
while True:
    print "\n" + "*" * 30 + "\nMenu" + "\n" + "*" * 30
    print "\n1) Use Student table\n2) Use Subject table\n3) Use " \
          "Enrollment table\n4) Use Examination table\n5) Formulate time table\n6) EXIT "

    choice_1 = int(input("Enter Your choice: "))
    os.system("clear")
    if choice_1 == 1:
        s = Student()
        print "\n" + "*" * 30 + "\nMenu" + "\n" + "*" * 30
        print "\n1)Insert element in student\n2)Update a student\n3)Delete a student\n4)Show students."
        choice_2 = int(input("Enter Your choice: "))
        os.system("clear")
        if choice_2 == 1:
            s.add_student()
        elif choice_2 == 2:
            s.update_student()
        elif choice_2 == 3:
            s.del_student()
        else:
            s.display()

    elif choice_1 == 2:
        s = Subject()
        print "\n1)Insert element in subject\n2)Update a subject detail\n3)Delete a subject\n4)Show subjects."
        choice_2 = int(input("Enter Your choice: "))
        os.system("clear")
        if choice_2 == 1:
            s.add_sub()
            s.display()
        elif choice_2 == 2:
            s.display()
            s.update_sub()
            s.display()
        elif choice_2 == 3:
            s.display()
            s.del_sub()
            s.display()
        else:
            s.display()

    elif choice_1 == 3:
        print "\n1)Enroll a student\n2)Update enrollment details\n3)Remove a student enrollment\n4)Show all " \
              "enrollments. "
        choice_2 = int(input("Enter Your choice: "))
        os.system("clear")
        e = Enrollment()
        if choice_2 == 1:
            e.enroll()
        elif choice_2 == 2:
            e.update_enroll()
        elif choice_2 == 3:
            e.del_enroll()
        else:
            e.display()

    elif choice_1 == 4:
        print "\n1)Enter exam details\n2)Update exam details\n3)Remove an exam\n4)Show all examinations"
        choice_2 = int(input("Enter Your choice: "))
        os.system("clear")
        e = Examination()
        if choice_2 == 1:
            e.add_exam()
        elif choice_2 == 2:
            e.update_exam()
        elif choice_2 == 3:
            e.del_exam()
        else:
            e.display()

    elif choice_1 == 5:
        os.system("clear")
        e = Examination()
        e.gen_time_table()
    else:
        sys.exit()
