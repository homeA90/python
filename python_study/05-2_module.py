# 모듈

## 모듈이란?
# 미리 만들어놓은 .py 파일을 사용하는 것
# module_test 파일 사용

## .py 파일 자체를 가져오기
import module_test
print(module_test.add(100,10))


## .py 파일 내에 필요한 함수만 가져오기
from module_test2 import div
print(div(9,3))


## if __name__ == "__main__": 의미
from module_test3 import mul  
# module_test3에 print 함수가 존재해서 출력 됨
# if __name__ == "__main__": 를 module_test3에 해놓으면 이름과 메인이 일치할때 실행하므로 
# import에선 실행되지 않음



## sys.path.append
# 경로가 다른 .py 불러오기
import sys
sys.path.append("C:/Users/TIGER/Desktop/develop/python/sub_python")
import module_test4