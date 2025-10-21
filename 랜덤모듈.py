#랜덤모듈.py
import random

print(random.random())  # 0.0 ~ 1.0 미만의 실수 중에서 랜덤하게 출력
print(random.random())
print(random.randint(2, 5))  # 2 ~ 5 사이의 정수 중에서 랜덤하게 출력
print([random.randrange(20) for i in range(10)])
print([random.randrange(20) for i in range(10)])
print(random.sample(range(20), 10))  # 0 ~ 19 사이의 정수 중에서 10개를 랜덤하게 출력
print(random.sample(range(20), 10)) 

# 로또번호
print(random.sample(range(1, 45), 5))

