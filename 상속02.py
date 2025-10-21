#상속02.py

class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def printInfo(self):
        #f-strings 문법을 사용
        print(f"ID: {self.id}, Name: {self.name}")


class Manager(Person):
    def __init__(self, id, name, title):
        super().__init__(id, name)
        self.title = title

    def printInfo(self):
        super().printInfo()
        print(f"Title: {self.title}")


class Employee(Person):
    def __init__(self, id, name, skill):
        super().__init__(id, name)
        self.skill = skill

    def printInfo(self):
        super().printInfo()
        print(f"Skill: {self.skill}")


if __name__ == "__main__":
    people = [
        Manager(1, "김철수", "팀장"),
        Manager(2, "이영희", "부장"),
        Manager(3, "박민수", "과장"),
        Employee(4, "최지은", "파이썬"),
        Employee(5, "정우성", "자바"),
        Employee(6, "한예린", "자바스크립트"),
        Employee(7, "오세훈", "데이터분석"),
        Employee(8, "강다현", "테스트"),
        Employee(9, "박지성", "네트워크"),
        Employee(10, "유나", "UI/UX"),
    ]

    for p in people:
        p.printInfo()
        print("-" * 30)