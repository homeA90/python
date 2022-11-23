# 파일 읽고 쓰기

## 파일 생성 및 쓰기_open함수
# w는 write(저장), r은 read(읽기), a는 append(추가)
# 현재 폴더에 저장하고 싶으면 주소 없이 파일명만 작성하면 됨

f = open("새파일.txt", 'w', encoding="UTF-8")  
for i in range(1, 11):
    data = "%d번째 줄입니다. \n" % i
    f.write(data)
f.close()


print("-----------------------------------------------------------------------")


## 파일 읽기_readline 함수
f = open("새파일.txt", 'r', encoding = 'UTF-8')
line = f.readline()
print(line)
f.close()
# 한줄씩 출력됨_그러므로 while문을 사용해야 전체 문장이 출력됨

# 한번에 여러줄 출력하기_while문 사용
f = open("새파일.txt", 'r', encoding = 'UTF-8')
while True:
    line = f.readline()
    if not line:
        break
    print(line)
f.close()

# readlines를 이용하여 리스트 형식으로 글을 출력하기
f = open("새파일.txt", 'r', encoding = 'UTF-8')
lines = f.readlines()
for line in lines:   # for문을 사용하여 리스트 내용을 출력한다
    print(line, end = '')  # \n 때문에 한줄이 띄어지고, print에 의해 한줄이 띄어져서 총 2번됨 
                           # 그래서 end 사용함 
f.close()

# read를 이용하여 내용 전체를 문자열로 출력하기
f = open("새파일.txt", 'r', encoding = 'UTF-8')
data = f.read()
print(data)
f.close


print("-----------------------------------------------------------------------")

## 파일 추가
f = open("새파일.txt", 'a', encoding="UTF-8")
for ii in range(11,40):
    data2 = "[추가입력] %d번째 줄입니다. \n" % ii
    f.write(data2)
f.close()

## close 없이 파일 저장하기_with ~ as 함수 사용
with open("foo.txt", 'w') as f: # foo.txt를 열어서 f라는 f라는 변수에 저장
    f.write("Life is short, you need python")

with open("foo.txt", 'r') as f:
    print(f.read())  # read는 return이 존재함

print("-----------------------------------------------------------------------")




