import MySQLdb
import pickle


class db(object):
    __config = {'dbname': "", "dbuser": "", "dbpwd": "", "dburl": "", "a_year": "", "batch": ""}

    def __init__(self):
        try:
            fp = open("dbconfig.txt", "r")
            settings = fp.readlines()
            fp.close()
        except:
            print"dbconfig.txt file missing"

        self.__conn = self.__configure_db(settings)
        self.a_year = db.__config['a_year']
        self.batch = db.__config['batch']

    def __configure_db(self, settings):
        for row in settings:
            if row != "\n" and row.strip()[0] != "#":
                data = row.strip().split("=")
                db.__config[data[0]] = data[1]

        return MySQLdb.connect(db.__config['dburl'], \
                               db.__config['dbuser'],
                               db.__config['dbpwd'],
                               db.__config['dbname'])

    def execute(self, ty, sql):
        try:
            cursor = self.__conn.cursor()
            if ty == "S":
                cursor.execute(sql)
                result = cursor.fetchall()

                return result

            elif ty in ["I", "U", "D"]:
                res = cursor.execute(sql)
                self.__conn.commit()

                return res
        except MySQLdb.Error,MySQLdb.IntegrityError:
            print "MySQL error occured: Please check your values or try again later."


class Student(db):

    __sconfig = {'a_year': "", "prn_count": ""}

    def __init__(self):
        db.__init__(self)
        Student.load_data()
        if self.a_year != Student.__sconfig['a_year']:
            Student.__sconfig['prn_count'] = 0
            Student.__sconfig['a_year'] = self.a_year
            Student.save_data(Student.__sconfig)
        self.prn_no = None
        self.seat_no = None
        self.Name = None
        self.age = None
        self.year = None
        self.Dept_id = None

    def display(self):
        data = ""
        sql = "select * from student order by prn_no"
        res = super(Student,self).execute("S", sql)
        print "prn_no\tseat_no\tName\tage\tYear\tDept_id\n"
        for x in res:
            for d in x:
                data = data + str(d) + " "
            data = data + "\n"
        print data

    def add_student(self):
        self.prn_no = self.gen_prn()
        print self.prn_no
        self.seat_no = raw_input("Enter seat no of new student: ")
        self.Name = raw_input("Enter name of new student: ")
        self.age = int(input("Enter age: "))
        self.year = raw_input("Enter anyone of F.Y/S.Y/T.Y/B.E: ")
        self.Dept_id = int(input("Enter Department id: "))
        try:
            sql = "insert into student values ({pn},'{sn}','{nn}',{ag},'{yr}',{did})".\
                format(pn=self.prn_no,sn=self.seat_no,nn=self.Name,ag=self.age, yr=self.year, did=self.Dept_id)
            super(Student,self).execute("I", sql)
        except MySQLdb.DataError:
            print "Insertion failed.Improper data spotted."
        except MySQLdb.IntegrityError:
            print "Integrity Error please check your values again."
        else:
            self.display()

    def update_student(self):
        self.display()
        self.prn_no = input("Enter the prn no of the student: ")
        self.seat_no = raw_input("Enter seat no of student: ")
        self.Name = raw_input("Enter name of student: ")
        self.age = int(input("Enter age: "))
        self.year = raw_input("Enter anyone of F.Y/S.Y/T.Y/B.E: ")
        self.Dept_id = int(input("Enter Department id: "))
        try:
            sql = "update student set seat_no = '{sn}',Name = '{nn}',age = {ag},year = '{yr}', Dept_id = {did} where " \
                  "prn_no={pn}".format(sn=self.seat_no, nn=self.Name, ag=self.age, yr=self.year, did=self.Dept_id,
                                       pn=self.prn_no)
            super(Student,self).execute("U", sql)
        except MySQLdb.IntegrityError:
            print("Integrity Error please check your values again.")
        except MySQLdb.DataError:
            print "Improper data spotted."
        else:
            self.display()

    def del_student(self):
        self.prn_no = input("Enter the prn no of the student: ")
        try:
            sql = "delete from student where prn_no = {pn}".format(pn=self.prn_no)
            super(Student, self).execute("D", sql)
        except MySQLdb.IntegrityError:
            print "Integrity Error please remove the related data from the table enrollment."
        else:
            self.display()

    @staticmethod
    def load_data():
        # Function to save the list of user objects to a file
        try:
            with open("studentconfig.txt", "rb") as f:
                Student.__sconfig=pickle.load(f)
        except:
            Student.__sconfig = {'a_year': "", "prn_count": ""}
        return Student.__sconfig

    @staticmethod
    def save_data(data):
        # Function to retrieve the user object data from a file
        with open("studentconfig.txt", "wb") as f:
            pickle.dump(data, f)

    def gen_prn(self):
        p = self.batch + self.a_year + "0000"
        prn = int(p) + int(Student.__sconfig['prn_count'])+1
        Student.__sconfig['prn_count'] = str(int(Student.__sconfig['prn_count'])+1)
        Student.save_data(Student.__sconfig)
        return prn


class Subject(db):

    def __init__(self):
        db.__init__(self)
        self.S_id = None
        self.S_name = None
        self.Credits = None
        self.Dept_id = None

    def add_sub(self):
        self.S_id = int(input("Enter the subject id: "))
        self.S_name = raw_input("Enter the subject name: ")
        self.Credits = int(input("Enter the subject credits: "))
        self.Dept_id = int(input("Enter the Department id: "))
        try:
            sql = "insert into subject values({sid},'{sn}',{cr},{did})".\
                format(sid=self.S_id, sn=self.S_name,cr=self.Credits, did=self.Dept_id)
            super(Subject,self).execute("I", sql)
        except MySQLdb.DataError:
            print "Improper data spotted."
        except MySQLdb.IntegrityError:
            print("Integrity Error please check your values again.")

    def display(self):
        data = ""
        sql = "select * from subject order by S_id"
        res = super(Subject, self).execute("S", sql)
        print "S_id\tS_name\tCredits\tDept_id\n"
        for x in res:
            for d in x:
                data = data + str(d) + " "
            data = data + "\n"
        print data

    def update_sub(self):
        self.display()
        self.S_id = int(input("Enter the subject id: "))
        self.S_name = raw_input("Enter the subject name: ")
        self.Credits = int(input("Enter the subject credits: "))
        self.Dept_id = int(input("Enter the Department id: "))
        try:
            sql = "update subject set S_id = {sid},S_name = '{sn}',Credits = {cr},Dept_id = {did} where S_id = {sid}".\
                format(sid=self.S_id, sn=self.S_name, cr=self.Credits, did=self.Dept_id)
            super(Subject, self).execute("U", sql)
        except MySQLdb.IntegrityError:
            print("Integrity Error please check your values again.")
        except MySQLdb.DataError:
            print "Improper data spotted."
        else:
            self.display()

    def del_sub(self):
        self.display()
        self.S_id = int(input("Enter the subject id: "))
        try:
            sql = "delete from subject where S_id = {sid}".format(sid=self.S_id)
            super(Subject, self).execute("D", sql)
        except MySQLdb.IntegrityError:
            print "Integrity Error please remove the related data from the table enrollment."
        else:
            self.display()


class Enrollment(db):

    def __init__(self):
        db.__init__(self)

        self.p_no = None
        self.Sub1 = None
        self.Sub2 = None
        self.Sub3 = None

    def display(self):
        data = ""
        sql = "select * from enrollment"
        res = super(Enrollment, self).execute("S", sql)
        print "p_no\tSub1\tSub2\tSub3\n"
        for x in res:
            for d in x:
                data = data + str(d) + " "
            data = data + "\n"
        print data

    def enroll(self):
        flag = 0

        self.p_no = input("Enter prn no of student: ")

        sql1 = "select s.S_id,s.S_name from subject s,Department d, student su where su.prn_no = {pn} and d.D_id = " \
               "su.Dept_id and d.D_id = s.Dept_id".format(pn=self.p_no)
        res1 = super(Enrollment, self).execute("S", sql1)
        data = ""
        print "List of subjects:\n\n"
        print "SUB id\tSUB Name\n"
        for x in res1:
            for s in x:
                data = data + str(s) + " "
            data = data + "\n"
        print data

        count = int(input("Enter no of subjects to enroll (max:3): "))
        if count == 1:
            flag = 1
            self.Sub1 = raw_input("Enter the 1st Subject id: ")
            sql = "insert into enrollment (p_no,Sub1) values({pn},{s1})".format(pn=self.p_no, s1=self.Sub1)
        elif count == 2:
            flag = 1
            self.Sub1 = raw_input("Enter the 1st Subject id: ")
            self.Sub2 = raw_input("Enter the 2nd Subject id: ")
            sql = "insert into enrollment (p_no,Sub1,Sub2) values({pn},{s1},{s2})".format(pn=self.p_no, s1=self.Sub1,
                                                                                          s2=self.Sub2)
        elif count == 3:
            flag = 1
            self.Sub1 = raw_input("Enter the 1st Subject id: ")
            self.Sub2 = raw_input("Enter the 2nd Subject id: ")
            self.Sub3 = raw_input("Enter the 3rd Subject id: ")
            sql = "insert into enrollment values({pn},{s1},{s2},{s3})". \
                format(pn=self.p_no, s1=self.Sub1,s2=self.Sub2, s3=self.Sub3)
        else:
            print "Invalid count."
        if flag == 1:
            try:
                super(Enrollment, self).execute("I", sql)
            except MySQLdb.IntegrityError:
                print("Integrity Error please check your values again.")
            except MySQLdb.DataError:
                print "Improper data spotted."
            else:
                self.display()

    def update_enroll(self):
        print "List of subjects:\n\n"
        s = Subject()
        s.display()
        self.display()
        self.p_no = input("Enter prn no of student to update: ")
        self.Sub1 = raw_input("Enter the 1st Subject id: ")
        self.Sub2 = raw_input("Enter the 2nd Subject id: ")
        self.Sub3 = raw_input("Enter the 3rd Subject id: ")
        sql = "update enrollment set Sub1={s1},Sub2={s2},Sub3={s3} where p_no = {pn}".\
            format(pn=self.p_no,s1=self.Sub1,s2=self.Sub2,s3=self.Sub3)
        try:
            super(Enrollment, self).execute("U", sql)
        except MySQLdb.IntegrityError:
            print("Integrity Error please check your values again.")
        except MySQLdb.DataError:
            print "Improper data spotted."
        else:
            self.display()

    def del_enroll(self):
        self.display()
        self.p_no = input("Enter prn no of student to be removed: ")
        sql = "delete from enrollment where p_no = {pn}".format(pn=self.p_no)
        try:
            super(Enrollment, self).execute("D", sql)
        except MySQLdb.IntegrityError:
            print "Integrity Error please remove the related data from other tables."
        else:
            self.display()


class Examination(db):
    def __init__(self):
        db.__init__(self)
        self.E_id = None
        self.Sub_id = None
        self.Date = None
        self.Start_time = None
        self.End_time = None
        self.year = None

    def display(self):
        data = ""
        sql = "select * from examination"
        res = super(Examination, self).execute("S", sql)
        print "E_id\tSub_id\tDate\tS_time\tE_time\tYear\n"
        for x in res:
            for d in x:
                data = data + str(d) + " "
            data = data + "\n"
        print data

    def add_exam(self):
        self.E_id = raw_input("Enter the exam id(max:5 char): ")
        self.Sub_id = raw_input("Enter the subject id: ")
        self.Date = raw_input("Enter the date {yyyy/mm/dd}: ")
        self.Start_time = raw_input("Enter start time: ")
        self.End_time = raw_input("Enter end time: ")
        self.year = raw_input("Enter anyone of F.Y/S.Y/T.Y/B.E: ")
        sql = "insert into examination values('{eid}',{sid},'{d}','{st}','{et}','{yr}')".\
            format(eid=self.E_id,sid=self.Sub_id,d=self.Date,st=self.Start_time,et=self.End_time, yr=self.year)
        try:
            super(Examination, self).execute("I", sql)
        except MySQLdb.IntegrityError:
            print("Integrity Error please check your values again.")
        except MySQLdb.DataError:
            print "Improper data spotted."
        else:
            self.display()

    def update_exam(self):
        self.E_id = raw_input("Enter the exam id to update(max:5 char): ")
        self.Sub_id = raw_input("Enter the subject id: ")
        self.Date = raw_input("Enter the date {yyyy/mm/dd}: ")
        self.Start_time = raw_input("Enter start time: ")
        self.End_time = raw_input("Enter end time: ")
        self.year = raw_input("Enter anyone of F.Y/S.Y/T.Y/B.E: ")
        sql = "update examination set Date='{d}',Start_time='{st}',End_time='{et}' where E_id='{eid}' and Sub_id={" \
              "sid} and year='{yr}'".format(eid=self.E_id, sid=self.Sub_id,d=self.Date,st=self.Start_time,
                                            et=self.End_time,yr=self.year)
        try:
            super(Examination, self).execute("U", sql)
        except MySQLdb.IntegrityError:
            print("Integrity Error please check your values again.")
        except MySQLdb.DataError:
            print "Improper data spotted."
        else:
            self.display()

    def del_exam(self):
        self.E_id = raw_input("Enter the exam id to delete(max:5 char): ")
        self.Sub_id = raw_input("Enter the subject id: ")
        self.year = raw_input("Enter anyone of F.Y/S.Y/T.Y/B.E: ")
        sql = "delete from examination where E_id = '{eid}' and Sub_id={sid}".format(eid=self.E_id,sid=self.Sub_id)
        try:
            super(Examination, self).execute("D", sql)
        except MySQLdb.IntegrityError:
            print"Integrity error"
        else:
            self.display()

    def gen_time_table(self):
        data = ""
        self.E_id = raw_input("Enter the exam id (max:5 char): ")
        self.year = raw_input("Enter anyone of F.Y/S.Y/T.Y/B.E: ")
        sql = "select * from examination where E_id='{eid}' and year='{yr}'".format(eid=self.E_id, yr=self.year)
        res = super(Examination, self).execute("S", sql)
        for x in res:
            for d in x:
                data = data + str(d) + " "
            data = data + "\n"
        print data