#부모 클래스 정의
class Person:
    def __init__(self, name, phoneNumber):
        self.name = name
        self.phoneNumber = phoneNumber

    def printInfo(self):
        print("Info(Name:{0}, Phone Number: {1})".format(self.name, self.phoneNumber))

#자식 클래스 정의
class Student(Person):
    def __init__(self, name, phoneNumber, subject, studentID):
        #super()로 부모 생성자 호출
        super().__init__(name, phoneNumber)
        self.subject = subject
        self.studentID = studentID

    #자식 클래스에서 부모 메서드 오버라이딩
    def printInfo(self):
        print("Info(Name: {0}, Phone Number: {1})".format(self.name, self.phoneNumber))
        print("Info(학과: {0}, 학번: {1})".format(self.subject, self.studentID))


#인스턴스 생성
p = Person("전우치", "010-222-1234")
s = Student("이순신", "010-111-1234", "컴공", "2412345")
p.printInfo()
s.printInfo()  # 오류 발생


