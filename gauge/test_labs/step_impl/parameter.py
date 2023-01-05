from nqplus.gocdlib.nq_python import step
## @step 을 사용하기 위해서 필요한 모듈
from nqplus.gocdlib.nq_env import gtbl_2_dict



@step("simple parameter 테스트 <abc>")
def test(abc):
    print(abc)


@step("dynamic parameter 테스트 <name>과 <number>")
def go(name, number):
    print("%s, %s" %(name, number))

@step("결과-concept 활용 <name>과 <number>")
def who(name, number):
    print(name)
    print(number)


## table 사용 시 @step 뒤에 <table>을 작성해야 인식된다
@step("## 밑에 table 입력하여 테스트 <table>")
def how(table):
    search_log = gtbl_2_dict(table)     ## table 형태를 dictionary로 변환 함수
    print(search_log.items())
    print(search_log["name"])
    print(search_log["number"])