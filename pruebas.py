from cluster import Server

v = ['aaa']

s1 = Server(v)
s2 = Server(v)

a = s1.incr_by('aaa',5)
b = s2.incr_by('aaa',10)

print(a)
print(b)

s1.merge(s2)
s2.merge(s1)

print("=========")
print(s1.count('aaa'))
print(s2.count('aaa'))

s1 = Server(v)
s2 = Server(v)

a = s1.incr_by('aaa',100)
b = s2.incr_by('aaa',200)

print(a)
print(b)

s1.merge(s2)
s2.merge(s1)

print("=========")
print(s1.count('aaa'))
print(s2.count('aaa'))

s1 = Server(v)
s2 = Server(v)

a = s1.incr_by('aaa',1)
b = s2.incr_by('aaa',2)

print(a)
print(b)

s1.merge(s2)
s2.merge(s1)

print("=========")
print(s1.count('aaa'))
print(s2.count('aaa'))
