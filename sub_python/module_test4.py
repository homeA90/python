


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
    
