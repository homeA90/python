# 제어문 - 조건문, 반복문


# 1) 반복문_#1(while문)


threeHit = 0
while threeHit < 10:
    threeHit = threeHit + 1
    print("나무를 %d번 찍었습니다." % threeHit)

    if threeHit == 10:
        print("나무가 넘어갑니다.")



print("-----------------------------------------------------------------------")


coffee = 10
money = 300

while money:
    print("돈을 받았으니 커피를 줍니다.")
    coffee = coffee - 1

    if not coffee:         # if coffee == 0: 이렇게 표현도 가능
        print("커피가 다 떨어졌습니다. 판매를 중지합니다.")
        break   # break 를 사용하여 while문 빠져나오기!


print("-----------------------------------------------------------------------")

a = 0
while a < 10:
    a = a + 1
    if a % 2 == 0:
        continue   # 조건에 맞지 않아서 while문을 빠져나가지 않고 다시 맨처음으로 돌아가게 하려면 continue 사용
    print(a)


print("-----------------------------------------------------------------------")

# 입력함수 이용하여 while문 작성
number = 0
prompt = """
1. Add
2. Del
3. List
4. Quit

Enter Number: 
"""

while number != 4:
    print(prompt)
    number = int(input())


print("-----------------------------------------------------------------------")

# if문 과 while문 활용하여 코드짜기
coffee = 10

while True:
    money = int(input("돈을 입력해주세요: "))
    if money == 300:
        print("돈을 받았으니 커피를 줍니다.")
        coffee = coffee - 1
        print("현재 남은 커피는 %d 입니다." % coffee)

    elif money > 300:
        print("돈을 받았으니 커피를 줍니다.")
        coffee = coffee - 1
        print("남은 잔돈은 %d원 입니다." % (money - 300))
        print("현재 남은 커피는 %d 입니다." % coffee)

    else:  
        print("입력한 금액이 부족합니다. 금액을 확인해주세요.")
        
    if coffee == 0:     
        print("커피가 다 떨어졌습니다. 판매를 중지합니다.")
        break   # break 를 사용하여 while문 빠져나오기!
    


'''
## 무한루프 
while True:
    print("Ctrl + c를 눌러야 while문을 빠져나갈 수 있습니다.")
'''