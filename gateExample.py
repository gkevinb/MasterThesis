import logicgate

'''
-------------------------Start Here-----------------------
'''

x = [3, 5, 7, 9]
y = [2, 4, 8]
z = [1, 6, 10]
data_streams = [x, y, z]
print(x)
print(y)
print(z)

res = logicgate.evaluate('OR', data_streams)
print('Result:')
print(res)
