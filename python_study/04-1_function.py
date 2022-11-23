# 함수
'''
def 함수명(매개변수):
    <수행할 문장1>
    <수행할 문장2>
    
    return 리턴 값
'''

## return 값 존재
def sum(a, b):
    result = a + b
    return result
print(sum(1,2))

print("-----------------------------------------------------------------------")

## 입력값이 없는 함수
def say():
    return 'Hi'
print(say())

print("-----------------------------------------------------------------------")

## 결과값이 없는 함수_return 없음
def add(a,b):
    print("%d, %d의 합은 %d입니다." % (a, b, a+b))
print(add(3,4))
# return값이 없으므로 print를 입력해도 none으로 출력됨
# 함수별로 return값이 있고, 없는게 존재해서 none으로 출력 됨
# 결과값(return)이 없는 함수를 출력하기 위해선 정의한 함수를 직접 실행해야함
add(3,4) # 함수를 직접 실행 시 none값 출력 안됨, 단 함수 안에 print 함수가 있으면 출력이 가능

print("-----------------------------------------------------------------------")

## 입력값도 결과값도 없는 함수
def tell():
    print('Hi')
print(tell())

print("-----------------------------------------------------------------------")

## 여러개의 입력값 함수
# #1
def sum_many(*args): # *args 여러개의 입력값을 넣고 싶을 때 사용
    sum = 0
    for i in args:
        sum += i
    return sum
print(sum_many(1,2,3))

# #2
def add_mul(choice, *args):
    if choice == "add":
        result = 0
        for i in args:
            result += i
    elif choice == "mul":
        result = 1
        for i in args:
            result *= i
    return result
#result = add_mul('mul', 1,2,3,4,5)
#print(result)
print(add_mul("mul", 1,2,3,4))

# #3_kwargs 이용
def print_kwargs(**kwargs):
    for k in kwargs.keys():  # kwargs.keys 딕셔너리 key값 인덱싱
        if (k == "name"):
            print("당신의 이름은 :" + kwargs[k])
print(print_kwargs(name="강지훈", b = "조규리")) 

print("-----------------------------------------------------------------------")

## 함수의 결과값은 언제나 하나이다
def sum_and_mul(a,b):
    return a+b, a*b, a-b  # return값이 여러개로 정의되어 있더라도 출력값은 하나의 튜플로 출력됨
print(sum_and_mul(4,5))
print(sum_and_mul(4,5)[0])  # 입력값 옆에 [] 인덱스번호 입력시 return 인덱스에 맞는것만 출력됨

print("-----------------------------------------------------------------------")

## 매개변수에 초기값 미리 설정하기
def say_myself(name, old, man=True): # 매개변수를 이미 설정해놓을 수 있음
    print("나의 이름은 %s 입니다." % name)
    print("나이는 %d 입니다." % old)
    if man:
        print("남자입니다.")
    else:
        print("여자입니다.")
say_myself("강지훈", 16, False) 
# man에 대해 매개변수를 이미 설정해놔서 입력할 필요없음
# 단, 미리 설정한 매개변수가 중간에 있으면 매칭이 되지 않아 실행되지 않음
# 매개변수가 설정되어 있더라도 값이 입력되면 입력한 값대로 동작함
say_myself(old = 20, name = '조규리', man=False)
# 입력값 순서를 안맞추고 진행하려면 매개변수와 입력값을 매칭시켜야함

print("-----------------------------------------------------------------------")

## 함수 안에서 선언된 변수의 효력 범위
a = 1
def vartest(a):  # 함수에 있는 변수는 지역변수로 함수내에서만 영향이 있음 
    a = a + 1
vartest(a)
print(a)

# 변수 변경방법_#1_return 사용
b = 3
def vartest2(b):
    b = b + 1
    return b
b = vartest2(b)
print(b)

# 변수 변경방법_#2_global 사용
c = 8
def vartest3():
    global c
    c = c + 1
vartest3()  # 중간에 함수를 적어논 이유는 해당함수가 실행되야 c의 값이 vartest3값으로 출력됨
print(c)

print("-----------------------------------------------------------------------")

## lambda 함수 사용_축약모드
# def를 사용할 만큼 복잡하지 않거나, def를 사용하지 못하는 곳에 사용

def aaa(a,b):
    return a + b
print(aaa(11,11))

aaaa = lambda a, b: a+b # 위의 def와 동일한 코딩, return이 없어도 결과값 돌려줌
print(aaaa(20,30))

# lambda 응용
myList = [lambda a, b: a+b, lambda a, b: a*b]
print(myList[0](4,5))  # myList의 리스트에서 0번 인덱스를 불러와 4,5값을 넣음
print(myList[1](4,5))