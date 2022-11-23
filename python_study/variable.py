# 변수


a = 1
b = 'python'
c = [1,2,3]
d = c
c[0] = 6

# 주소의 개념으로 이해해야함. d = c 인 상태에서 c[0]값을 6으로 바꿨더라도 d도 동일하게 값이 변경됨
# d는 c의 동일한 주소를 바라보고 있기 때문임
print(id(c)) #id는 주소값 찍는 함수
print(id(d))
print(c is d) # 같은 주소를 보고있는지 확인_True 또는 False로 출력 됨
print(c)
print(d)


print('-------------------------------------------------------------')

# v1의 값을 v2에게 주고싶을 땐 인덱스 슬라이싱(:) 을 이용하여 전달
v1 = [1,2,3,4]
v2 = v1[:]

v1[0] = 99

print(v1)
print(v2)
print(id(v1))
print(id(v2))


print('-------------------------------------------------------------')

# copy라는 라이브러리를 이용

from copy import copy

v3 = [5,6,7,8]
v4 = copy(v3)

v3[0] = 88 

print(v3)
print(v4)
print(id(v3))
print(id(v4))


print('-------------------------------------------------------------')

# 변수를 만드는 여러가지 방법

a, b = ('python', 'life')
(c, d) = 'tuple2', 'good'
[e, f] = ['list', 'wow']
h = i = 'multi' # h와 i에 동일하게 multi 입력

# j와 k의 값을 변경
j = 3
k = 6
j, k = k, j

print(a, b)
print(c, d)
print(e, f)
print(h, i)
print(j, k)

