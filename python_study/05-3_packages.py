# 패키지

## 패키지 = 라이브러리 == 모듈 여러개 모아놓은 것

# 패키지 불러오기
import game.sound.echo
game.sound.echo.echo_test()

# 한개 모듈만 불러오기
from game.sound import echo
echo.echo_test()

# 원하는 함수만 불러오기
from game.sound.echo import echo_test
echo_test()


# 원하는 함수이름 변경하여 사용하기
from game.sound.echo import echo_test as a # as라는 의미는 echo_test를 변경하는 의미
a()

# 폴더에 있는 패키지 전부 다 불러오기
from game.sound import *
echo.echo_test()
# *를 사용하여 가져올땐 init 폴더에 __all__ = ['가져올 모듈명'] 을 작성해둔다.


# render 모듈에서 echo 모듈 사용하기
from game.graphic.render import render_test
render_test()
# render.py 모듈에 해당 echo.py 경로 작성하고 실행하면 됨
# 또 리눅스의 .. 처럼 디렉터리 이동식으로도 가능