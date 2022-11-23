# 3장 연습문제

'''
# Q1_다음 코드의 결과 값은?
a = "Life is too short, you need python"
if "wife" in a: print("wife") # 1번
elif "python" in a and "you" not in a: print("python") # 2번
elif "shirt" not in a: print("shirt") # 3번
elif "need" in a: print("need") # 4번
else: print("NONE") # 5번
# #3번이 출력됨
'''


print("-----------------------------------------------------------------------")

# Q2_while문을 이용하여 1부터 1000까지의 자연수 중 3의 배수의 합을 구해보자
Q2 = 1
N3 = 0
while Q2 <= 1000:
    if Q2 % 3 == 0:
        N3 += Q2 # a+=b 연산자는 a = a+b를 의미함
    Q2 += 1
print(N3)


print("-----------------------------------------------------------------------")

# Q3_while문을 사용하여 다음과 같이 별(*)을 표시하는 프로그램을 작성해보자
Q3 = 0
while True:
    Q3 += 1
    if Q3 == 6: break
    print("*" * Q3)


print("-----------------------------------------------------------------------")

# Q4_for문을 이용하여 1부터 100까지 숫자를 출력해보자
for Q4 in range(1,101):
    print(Q4)

print("-----------------------------------------------------------------------")

# Q5_A학급에 총 10명의 학생이 있다. 이 학생들의 중간고사 점수는 다음과 같다.
# [70, 60, 55, 75, 95, 90, 80, 80, 85, 100]
# for문을 사용하여 A 학급의 평균 점수를 구해보자
Q5 = [70, 60, 55, 75, 95, 90, 80, 80, 85, 100]
total = 0

for score in Q5:
    total += score
average = total / len(Q5)
print(average)

# Q6_리스트 중에서 홀수에만 2를 곱하여 저장하는 다음 코드가 있다.
'''
numbers = [1, 2, 3, 4, 5]

result = []
for n in numbers:
    if n % 2 == 1
        result.append(n*2)
'''
# 위 코드를 리스트 내포를 사용하여 표현해보자
numbers = [1, 2, 3, 4, 5]

result = [n * 2 for n in numbers if n % 2 == 1]
print(result)