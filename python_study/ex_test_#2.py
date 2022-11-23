

# Q8
a = (1,2,3)
a = (a + (4,))

print(a)

# Q9
a = dict() # 비어있는 딕션너리를 만들때 dict() 를 사용함
a['name'] = 'python'
a[('a',)] = 'is'
a[250] = 'love'
# a[[1]] = 'test' -> 3번이 안되는 이유는 keys 값엔 리스트와 같은 값이 변경되는 것을 사용할 수 없음

print(a)
b = {}
print(b)


# Q10
a = {'A': 90, 'B': 80, 'C': 70}
result = a.pop('B')
print(a)
print(result)


# Q11
a = [1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5]
aSet = set(a)
b = list(aSet)
print(b)

# Q12
a = b = [1, 2, 3]
a[1] = 4
print(id(a))
print(id(b))
print(a)
print(b)
# 변경한 a값과 동일하게 b값이 출력됨, id를 통해 주소를 확인해보면 a=b는 주소를 같이 쓰기때문에 변경된 값도 같아짐