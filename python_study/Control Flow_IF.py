# 제어문 - 조건문, 반복문


# 1) 조건문(if문)
from email import message


money = False
if money:
    print('택시를 타고 가라')

else:
    print('걸어 가라')

### 조건문에선 들여쓰기!! 해야함 ###

# 2) 비교연산자를 이용한 조건문(if문)
a = 6
b = 2

if a < b:
    print('a가 작네')

else:
    print('아니네! b가 작네')

if a != b:
    print('안같아')
else:
    print('같아!')

if a <= b:
    print('같거나 크네!')
else:
    print('같지 않거나 크지않네!')

if a >= b:
    print('같거나 크네!')
else:
    print('같지 않거나 크지않네!')


money2 = 2000
if money2 >= 3500:
    print('2_택시 타고 가자')
else:
    print('2_걸어가자')


# 3) and, or, not 연산자 이용한 조건문(if문)
# or 사용
money3 = 2000
card = 1
if money3 >= 3500 or card:
    print('3_택시 타고 가자')
else: 
    print('3_걸어가자')

# and 사용
money4 = 2000
card = 1
if money4 >= 3500 and card:
    print('4_택시 타고 가자')
else: 
    print('4_걸어가자')
# and는 둘다 참이어야 함#

# not 사용
if not False:
    print('5_택시 타고 가자')
else: 
    print('5_걸어가자')

if not True:
    print('5_택시 타고 가자')
else: 
    print('5_걸어가자')
# 반대로 됨#


# x in s, x not in s 사용
x1 = [1, 2, 3, 4, 5]
if 1 in x1:   # x1에 1이 있는지 확인하는 조건문_(값이 있어야 True가 됨)
    print('값이 들어있네(True)')
else: 
    print('값이 없네(False)')

x2 = [1, 2, 3, 4, 5]
if 6 not in x2:   # x1에 1이 없는지 확인하는 조건문_(없어야 True 가 됨)
    print('값이 없네(True)')
else: 
    print('값이 있네(False)')


# Test_"주머니에 카드가 없다면 걸어가고, 있다면 버스를 타고가라" 조건문으로 만들기
Pocket = ['card', 'paper', 'cellphone']
if 'card' not in Pocket:
    print("걸어 가자..ㅠㅠ")
else:
    print('버스를 타고 가자!')


# 조건문에서 일부 조건문이 동작하지 않도록 하기
Pocket = ['card', 'paper', 'cellphone']
if 'card' in Pocket:
    pass      # pass를 입력하면 해당 부분은 그냥 넘어간다.
else:
    print('걸어가자...!')


# 다양한 조건을 판단하는 elif
Pocket = ['paper', 'cellphone']
card = False
pay = True
if 'money' in Pocket:
    pass
elif card:
    print('와! 버스타자!!')
elif pay:
    print('휴~ 버스를 탄다')
else:
    print('걸어가자...!')


# if문 한줄로 작성하기
Pocket = ['paper', 'cellphone']
card = False
pay = False
if 'money' in Pocket: pass
elif card: print('카드가 있으니깐 버스타자!')
elif pay: print('삼성페이가 되니깐.. 버스타자!')
else: print('걸어가자...!')

# 조건부 표현식
score1 = 70
if score1 >= 60:
    message1 = "sussess"
else:
    message1 = "failure"
print(message1)
# 위의 형식을 조건부 표현식을 사용하면
score2 = 80
message2 = "sussess" if score2 >= 60 else "failure"
print(message2)
# 성공(참)일때 조건을 먼저 작성 후 뒤에 실패(거짓)을 써준다