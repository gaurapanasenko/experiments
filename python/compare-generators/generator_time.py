#!/usr/bin/env python3

import timeit

def test():
	for i in range(10000):
		if i > 30:
			yield i

mysetup = '''
def test():
	for i in range(100000):
		if i > 30:
			yield i
'''

mycode = '''set(test())'''

print(timeit.timeit(setup = mysetup, stmt = mycode, number = 100))

mycode = '''{i for i in range(100000) if i > 30}'''
print(timeit.timeit(stmt = mycode, number = 100))

mycode = '''
s = set()
for i in range(100000):
	if i > 30:
		s.add(i)
'''
print(timeit.timeit(stmt = mycode, number = 100))

mycode = '''
s = []
for i in range(100000):
	if i > 30:
		s.append(i)
set(s)
'''
print(timeit.timeit(stmt = mycode, number = 100))
