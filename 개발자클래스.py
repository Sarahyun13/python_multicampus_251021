#개발자 클래스를 정의
class Developer:
    def __init__(self, name, phoneNumber, language):
        self.name = name
        self.phoneNumber = phoneNumber
        self.language = language

    def printInfo(self):
        print("Info(Name:{0}, Phone Number: {1}, Language: {2})".format(self.name, self.phoneNumber, self.language))

class WebDeveloper(Developer):
    def __init__(self, name, phoneNumber, language, framework):
        super().__init__(name, phoneNumber, language)
        self.framework = framework

    def printInfo(self):
        super().printInfo()
        print("Framework: {0}".format(self.framework))

#인스턴스 생성
dev = WebDeveloper("홍길동", "010-1234-5678", "JavaScript", "React")
print(dev)