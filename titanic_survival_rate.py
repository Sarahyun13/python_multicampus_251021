import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 타이타닉 데이터셋 로드 (seaborn에 내장된 데이터셋 사용)
titanic = sns.load_dataset('titanic')

# 성별에 따른 생존율 계산
survival_rate = titanic.groupby('sex')['survived'].mean()

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 막대 그래프 생성
plt.figure(figsize=(10, 6))
survival_rate.plot(kind='bar')

# 그래프 꾸미기
plt.title('타이타닉 성별 생존율', fontsize=15)
plt.xlabel('성별', fontsize=12)
plt.ylabel('생존율', fontsize=12)

# 각 막대 위에 생존율 표시 (백분율로)
for i, v in enumerate(survival_rate):
    plt.text(i, v, f'{v:.1%}', ha='center', va='bottom')

# y축 범위 설정 (0~1)
plt.ylim(0, 1)

# 격자 추가
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()