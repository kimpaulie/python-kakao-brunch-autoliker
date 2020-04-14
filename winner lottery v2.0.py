import random, time, sys
from pandas import Series, DataFrame
import pandas as pd
import openpyxl
import numpy as np

print('당첨자 추첨 프로그램 by Paulie v1.0\n')

df=pd.read_excel('listfile.xlsx', 'sheet1', index_col=None, na_values=['NA'])

total_participant = len(df) # 참여자 숫자
total_winner_num = 10 # 당첨자 숫자
print('총 참여자 %d명' % total_participant)
print('총 당첨자 수 %d명' % total_winner_num)

#인증 사진 여부 내에서 빈 열 제거하고 'O'가 포함된 애들을 뽑아낸다
cert = df["인증 사진 여부"].dropna(how='any')
#해시태그 #위생 내에서 빈 열 제거하고 #위생 이 포함된 애들을 뽑아낸다
clean = df["해시태그 #위생"].dropna(how='any')
# 두가지 조건을 만족하는 행의 'ID','인증 사진 여부','해시태그 #위생' 칼럼 출력
double_check=df.loc[cert.str.contains('O') & clean.str.contains('#위생'),['ID','인증 사진 여부','해시태그 #위생']]

print('\n※ 사전 당첨 제외자 설정으로 DB 조건에 맞지 않는 참여자 %d명을 제외합니다.' % (total_participant-len(double_check)))
print(' - DB 조건 :인증 사진 / 해시태그 #위생\n')

print('추첨 대상자 %d명의 리스트입니다\n' % len(double_check))

# 임의 번호 부여
double_check['추첨 번호'] = range(1,len(double_check)+1)
print(double_check.loc[:,['ID','추첨 번호']])

print('\n★★★ 추첨 START ★★★')

# 참여자 배열 만들기
participant_num = []  # 참여자 숫자 리스트
for num in range(1, len(double_check) + 1):  # 1-70
	# print(num)
	participant_num.append(num)

print('\n당첨자 번호를 추첨하고 있습니다.',end='')

# for i in range(6):
# 	time.sleep(1)
# 	print('.',end='')

winner_result = sorted(random.sample(participant_num, total_winner_num))
print('\n추첨이 완료되었습니다.\n')

print('총 당첨 번호 %d개' % total_winner_num)
print(winner_result)

print('\n축하합니다! 당첨자는 아래와 같습니다.\n')

#print(double_check)
print(double_check.loc[double_check['추첨 번호'].isin(winner_result),['ID','추첨 번호']])

print('\n프로그램이 종료됩니다.')