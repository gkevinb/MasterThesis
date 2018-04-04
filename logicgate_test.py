import logicgate


HIGH = 'HIGH'
LOW = 'LOW'

slice_ = [LOW, HIGH, LOW, HIGH, LOW]
k = 3

print(logicgate._is_k_down(slice_, k))


print(logicgate._k_voting_evaluate_slice(slice_, k))

s1 = [1, 4]
s2 = [3, 5, 6, 8, 9]
s3 = [2, 7]
streams = [s1, s2, s3]
print(logicgate.evaluate(2, streams))
result = [2, 5, 6, 7]
