# -*- coding: utf-8 -*-
"""4-1 로지스틱 회귀_2023312822 유선아

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1blRFvOFuzvTrfAHHJKH4Ap4-okcSzjQh

# 로지스틱 회귀 (분류 알고리즘)

<table align="left">
  <td>
    <a target="_blank" href="https://colab.research.google.com/github/rickiepark/hg-mldl/blob/master/4-1.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" />구글 코랩에서 실행하기</a>
  </td>
</table>

## 럭키백의 확률

- 럭키백에 들어간 생선의 크기, 무게 등이 주어졌을 때 7개 생선에 대한 확률 출력
- 길이, 높이, 두께 외에도 대각선 길이, 무게 사용 가능

### 데이터 준비하기
"""

import pandas as pd

fish = pd.read_csv('https://bit.ly/fish_csv_data')
# 인터넷에서 csv 파일 읽음

fish.head()
# 상단 5개 항 출력

print(pd.unique(fish['Species']))
# Species 열에서 고유한 값 출력 -> y값

fish_input = fish[['Weight','Length','Diagonal','Height','Width']].to_numpy()
# Species 제외한 5개 열을 입력 데이터(x)로 사용

print(fish_input[:5])
# fish_input의 5개 항 출력

fish_target = fish['Species'].to_numpy()
# Species 열을 타겟(y=생선 종류)으로 사용

from sklearn.model_selection import train_test_split

train_input, test_input, train_target, test_target = train_test_split(
    fish_input, fish_target, random_state=42)
# 훈련 세트와 테스트 세트 나눔

from sklearn.preprocessing import StandardScaler
# StandardScaler 클래스를 통해 훈련 세트, 테스트 세트 표준화 전처리(평균 0, 분산 1)

ss = StandardScaler()
# 객체 생성

ss.fit(train_input)
# 모델 훈련(분포를 객체에 저장)

train_scaled = ss.transform(train_input)
# 훈련 세트 변환

test_scaled = ss.transform(test_input)
# 테스트 세트 변환

"""### k-최근접 이웃 분류기의 확률 예측"""

from sklearn.neighbors import KNeighborsClassifier

kn = KNeighborsClassifier(n_neighbors=3)
kn.fit(train_scaled, train_target)

print(kn.score(train_scaled, train_target))
print(kn.score(test_scaled, test_target))

print(kn.classes_)

print(kn.predict(test_scaled[:5]))

import numpy as np

proba = kn.predict_proba(test_scaled[:5])
print(np.round(proba, decimals=4))

distances, indexes = kn.kneighbors(test_scaled[3:4])
print(train_target[indexes])

"""## 로지스틱 회귀"""

import numpy as np
import matplotlib.pyplot as plt

z = np.arange(-5, 5, 0.1)
phi = 1 / (1 + np.exp(-z))

plt.plot(z, phi)
plt.xlabel('z')
plt.ylabel('phi')
plt.show()

"""### 로지스틱 회귀로 이진 분류 수행하기"""

char_arr = np.array(['A', 'B', 'C', 'D', 'E'])
print(char_arr[[True, False, True, False, False]])
# 불리언 인덱싱 (-> 7 종류의 fish 중 2가지 선택해서 binary 로지스틱 회귀 해보자)
# True인 index 위치의 값만 출력

bream_smelt_indexes = (train_target == 'Bream') | (train_target == 'Smelt')
# bream_smelt_indexes 배열은 훈련 세트 중 'Bream'과 'Smelt'일 때 True ( | (or))
# 이외의 값은 False

train_bream_smelt = train_scaled[bream_smelt_indexes]
# train_scaled 배열에 불리언(True of False) 인덱싱 적용

target_bream_smelt = train_target[bream_smelt_indexes]
# train_target 배열에 불리언(True or False) 인덱싱 적용

from sklearn.linear_model import LogisticRegression
# LogisticRegression 클래스import

lr = LogisticRegression()
# 객체 생성

lr.fit(train_bream_smelt, target_bream_smelt)
# 모델 훈련 (x, y)

print(lr.predict(train_bream_smelt[:5]))
# train_bream_smelt 의 처음 5개 샘플 출력

print(lr.predict_proba(train_bream_smelt[:5]))
# predict_proba() 메서드로 처음 5개 샘플의 예측 확률 출력
# 첫번째 열(왼쪽)이 음성 클래스(0)에 대한 확률, 두 번째 열이 양성 클래스(1)에 대한 확률

print(lr.classes_)
# 타깃값을 어떻게 갖고 있는지 알기 위해 출력
# -> 사이킷런은 타깃값을 알파벳순으로 정렬하여 사용함
# 두 번째 샘플만 양성클래스인 빙어(smelt)의 확률이 높음
# 나머지는 모두 도미(bream)로 예측

print(lr.coef_, lr.intercept_)
# 로지스틱 회귀가 학습한 계수(coef), 절편(intercept) 출력
# 5종류의 x 갖고 있으므로 계수 5개
# z = -0.404 x (weight) - 0.576 x (Length) - 0.663 x (Diagonal) - 1.-13 x (Height) - 0.732 x (Width) -2.161
# z를 이용하여 Sigmoid func으로 확률값으로 변환

decisions = lr.decision_function(train_bream_smelt[:5])\
# 양성 클래스에 대한 z값 계산
# train_bream_smelt의 처음 5개 샘플의 z값 출력

print(decisions)
# 정답이 1인 smelt 양의 값 / bream 음의 값

from scipy.special import expit
# Sigmoid 함수인 expit import

print(expit(decisions))
# z값(decisions)를 넣어 시그모이드 함수를 통과한 값 출력
# -> predict_proba() 메서드 출력의 두번째 열의 값과 동일

"""### 로지스틱 회귀로 다중 분류 수행하기"""

lr = LogisticRegression(C=20, max_iter=1000)
# max_iter=1000으로 반복횟수 1000으로 설정(max_iter 기본값=100)
# LogisticRegression 에서 규제를 제어하는 매개변수 C(하이퍼파라미터)
# C가 작을수록 규제가 커짐, C의 기본값은 1 <- alpha 값과 반비례

lr.fit(train_scaled, train_target)
# 모델 훈련

print(lr.score(train_scaled, train_target))
# 훈련 세트 score 출력
print(lr.score(test_scaled, test_target))
# 테스트 세트 score 출력

print(lr.predict(test_scaled[:5]))
# 테스트 세트의 처음 5개 샘플에 대한 예측 출력

proba = lr.predict_proba(test_scaled[:5])
# 테스트 세트의 처음 5개 샘플에 대한 예측 확률

print(np.round(proba, decimals=3))
# 소수점 3째 자리 유지, 4째 자리에서 반올림
# 5개 샘플에 대한 예측 -> 5개 행 / 7개 생선에 대한 확률 -> 7개 열

print(lr.classes_)
# 클래스 정보 출력
# 첫번째 샘플은 Perch를 가장 높은 확률로 예측함을 알 수 있음
# 두번째 샘플은 Smelt를 가장 높은 확률로 예측함을 알 수 있음

print(lr.coef_.shape, lr.intercept_.shape)
# coef_(계수, 기울기)와 intercept_(절편)의 크기 출력
# 다중분류는 클래스마다 z값을 계산하므로 7행
# 5개의 특성을 사용하므로 5열

decision = lr.decision_function(test_scaled[:5])
# decision_function() 메서드로 z1~z7 까지의 값을 구함
print(np.round(decision, decimals=2))
# 소수점 2째 자리 유지, 소수점 3째 자리에서 반올림

from scipy.special import softmax
# softmax import -> z값으로 확률 변환
# softmax func(다항 로지스틱 회귀) : 여러 개의 선형 방정식 출력값을 0~1 사이로 압축하고 전체 합이 1이 되도록 만듦 -> 정규화된 지수함수

proba = softmax(decision, axis=1)
# 각 샘플에 대해 softmax 계산
print(np.round(proba, decimals=3))
# 소수점 3째 자리 유지, 4째 자리에서 반올림