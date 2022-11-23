# 클래스


## 클래스가 필요한 이유?
result = 0
def add(num):
    global result
    result += num
    return result

print(add(3))
print(add(4))


# 그런데 만약 2대의 계산기가 필요하다면 def를 2개 만들어야 함
# 이런 반복된 함수를 사용하지 않기 위해서 클래스를 사용함
result1 = 0
result2 = 0
def add1(num):
    global result1
    result1 += num
    return result1

def add2(num):
    global result2
    result2 += num
    return result2

print(add1(3))
print(add1(4))
print(add2(3))
print(add2(7))

print("-----------------------------------------------------------------------")


## 클래스 사용 방법
'''
1. class 입력하고
2. 대문자로 시작하는 클래스의 이름 작성
3. 안에 들어갈 함수와 변수 설정
'''
class FourCal:
    pass

a = FourCal()
print(type(a))


class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, num):
        self.result += num
        return self.result

cal1 = Calculator()
cal2 = Calculator()
# 클래스로 만든 객체의 객체변수는 독립적인 값을유지 함

print(cal1.add(3))
print(cal1.add(4))
print(cal2.add(3))
print(cal2.add(7))



print("-----------------------------------------------------------------------")

## 사칙연산 클래스 2
# 클래스는 self라고 해서 맨앞에 인스턴스를 만들수 있음. self는 호출한 객체 a로 자동 전달됨
class FourCal:
    def setdata(self, first, second):  
        self.first = first
        self.second = second

a = FourCal()
a.setdata(1,2)
print(a.first)
print(a.second)

print("-----------------------------------------------------------------------")

## 사칙연산 클래스 3
class FourCal:
    def setdata(self, first, second):  
        self.first = first
        self.second = second
    def add(self):
        result = self.first + self.second
        return result

a = FourCal()
a.setdata(4,2)
print(a.add())


print("-----------------------------------------------------------------------")

## 생성자(Constructor)
# __(언더바) 2개를 선언하면 해당클래스에선 무조건 맨처음에 실행됨
class FourCal_cons:
    def __init__(self, first, second):
        self.first = first
        self.second = second
    def setdata(self, first, second):  # init을 선언했으므로 setdata는 없어도 됨
        self.first = first
        self.second = second
    def add(self):
        result = self.first + self.second
        return result

a = FourCal_cons(1,2)
print(a.add())


print("-----------------------------------------------------------------------")


## 클래스 상속(Inheritance)
# 기존에 만든 클래스를 다른 클래스로 가져와 사용하는 것을 말함
class FourCal_In:
    def __init__(self, first, second):
        self.first = first
        self.second = second
    def setdata(self, first, second):  # init을 선언했으므로 setdata는 없어도 됨
        self.first = first
        self.second = second
    def add(self):
        result = self.first + self.second
        return result
    def mul(self):
        result = self.first * self.second
        return result
    def sub(self):
        result = self.first - self.second
        return result 
    def div(self):
        result = self.first / self.second
        return result

class MoreFourCal1(FourCal_In):
    pass

m1 = MoreFourCal1(50,50)
print(m1.add())

print("-----------------------------------------------------------------------")

## 클래스 상속 매서드 추가
class MoreFourCal2(FourCal_In):
    def pow(self):
        result = self.first ** self.second
        return result
m2 = MoreFourCal2(9,2)
print(m2.pow())
print(m2.add())
print(m2.div())

print("-----------------------------------------------------------------------")

## 클래스 상속 매서드 오버라이딩(부모 클래스 변형)
# 상속 클래스 간 동일한 매서드 존재 시 자식 매서드가 우선순위 높음
class MoreFourCal3(FourCal_In):
    def div(self):
        if self.second == 0:
            return 0
        else:
            return self.first / self.second
m3 = MoreFourCal3(10,2)
m4 = MoreFourCal3(5,0)
print(m3.div())
print(m4.div())

print("-----------------------------------------------------------------------")

## 클래스 변수, 객체 변수 차이점
class FourCal11:
    first11 = 2 # 클래스 변수
    second11 = 3 # 클래스 변수
    def __init__(self, first11, second11):  # 객체 변수
        self.first11 = first11
        self.second11 = second11
    def setdata11(self, first11, second11): # 객체 변수
        self.first11 = first11
        self.second11 = second11
    def add11(self):  # 객체 변수
        result = self.first11 + self.second11
        return result
             