# 집합 자료형


s1 = set([1,2,3,4,5,6])
s2 = set([4,5,6,7,8,9])

# 교집합
print(s1 & s2)
print(s1.intersection(s2))

# 합집합
print(s1 | s2)
print(s1.union(s2))

# 차집합
print(s1 - s2)
print(s2 - s1)
print(s1.difference(s2))
print(s2.difference(s1))

# add 를 이용하여 1개의 값 추가
s3 = set([1,2,3,4,5,6])
s3.add(7)

print(s3)

#  update 를 이용하여 여러개의 값 추가
s4 = set([1,2,3,4])
s4.update([5,6,7,8])

print(s4)

# remove 를 이용하여 값 삭제(1개만 삭제되는것 같음)
s5 = set([1,2,3])
s5.remove(3)

print(s5)
