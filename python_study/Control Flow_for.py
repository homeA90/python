# 제어문 - 조건문, 반복문


# 1) 반복문_#2(for문)

# 전형적인  for문

test_list = ['one', 'two', 'three']
for i in test_list:   # test_list 의 내용을 순서대로 하나씩 (i)에 집어넣은 것!
    print(i)


print("-----------------------------------------------------------------------")


# 다양한 for문 사용
a = [(1,2), (3,4), (5,6)]
for (first, last) in a:
    print(first + last)


print("-----------------------------------------------------------------------")


# for문 응용
marks = [90, 25, 67, 45, 80]
number = 0

for mark in marks:
    number = number + 1
    
    if mark >= 60:
        print("%d번 학생은 합격입니다." % number)
    
    else:
        print("%d번 학생은 불합격입니다." % number)


print("-----------------------------------------------------------------------")


# for문과 continue
score = [90, 25, 67, 45, 80]
num = 0

for Pass in score:
    num = num + 1
    if Pass < 60:
        continue   # if문 조건에 참이면 continue로 진행됨, 반대로 거짓이면 아래 print로 진행 함
    print("%d번 학생은 합격입니다." % num)


print("-----------------------------------------------------------------------")


# for문과 함께 자주 사용하는 range 함수
add = 0
for r in range(1, 11):  # range함수는 1 이상 11미만의 범위의 숫자를 포함하는 객체 임
    add = add + r
print(add)

# 
jum = [90, 25, 67, 45, 80]

for n in range(len(jum)):  #len 함수는 리스트의 요소를 갯수로 돌려주는 함수
    if jum[n] < 60: continue  # jum[n]은 리스트 인덱싱을 통해 if문 동작
    print("%d번 학생은 합격입니다." % (n + 1))
# jum의 갯수는 5개 이므로 len은 len(5)가 되고, range(5)는 0~4까지되며, 그 값을 n에다 대입한다.
# jum[n]은 jum의 리스트에서 n의 갯수 즉 0~4 인덱싱에 맞게 값을 가지고 오게되고, 그 결과에 따라  print된다. 


print("-----------------------------------------------------------------------")

# 이중 for문_구구단 만들기
for x in range(2, 10):
    for y in range(1,10):
        print(x * y, end=" ") # end를 넣어준 이유는 결과값을 출력할 때 다음줄로 넘기지 않고, 계속출력하기위해
    print("")


print("-----------------------------------------------------------------------")
# for문 리스트 내포
aa = [1,2,3,4]
result = [num * 3 for num in aa if num % 2 == 0]
print(result)
# num *3 을 담은 result를 만드는데, for문을 이용한 num에서 if문을 돌려 나오는 num을 *3하라는 것 


result2 = [xx * yy for xx in range(2,10) for yy in range(1,10)]
print(result2)