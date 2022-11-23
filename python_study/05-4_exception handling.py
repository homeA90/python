# 예외처리

## 예외처리 기본구조
'''
1) try:   #오류가 발생할 수 있는 구문
2) except Exception as e:   # 오류발생 시 확인
3) else:    # 오류발생하지 않음
4) finally:   #무조건 마지막에 실행
'''

## 예외처리 기법_try, except, else, finally
try:
    4 / 0
except ZeroDivisionError as e:
    print(e)
# 위의 예외처리로 인해 다음 코드들이 정상적으로 실행 됨


try:
    f = open('새파일.txt', 'r', encoding = 'UTF-8')
except FileNotFoundError as ee:
    print(str(ee))
else:    # 에러가 없을 때 else가 실행 됨
    data = f.read()
    print(data)
    f.close()

f = open('구구단.txt', 'r', encoding = 'UTF-8')
try:
    data = f.read()
    print(data)
except Exception as eee:   # 모든 종류의 에러는 Exception으로 확인 가능
    print(eee)
finally:  # 마지막에 실행하고 싶을 때
    f.close()


## 여러개 예외처리 가능
try:
    a = [1,2]
    print(a[3])
    4/0
except ZeroDivisionError:  
    print("0으로 나눌 수 없습니다.")
except IndexError:
    print("인덱싱 할 수 없습니다.")    
# except를 변수로 바꾸지 않고 오류 발생 시 에러팝업을 print로 나타내줄수도 있음