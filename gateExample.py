import logicgate

'''
-------------------------Start Here-----------------------
'''

x = [8, 18]
y = [9, 16]
data_streams = [x, y]
print(x)
print(y)
res = logicgate.evaluate('AND', data_streams)
print('Result:')
print(res)

print('--------------------')

x = [8.618904143724958, 18.760026889953128]
y = [9.754214745654227, 16.54121097802728]
data_streams = [x, y]
print(x)
print(y)
res = logicgate.evaluate('AND', data_streams)
print('Result:')
print(res)
