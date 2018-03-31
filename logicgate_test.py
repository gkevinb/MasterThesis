import logicgate


HIGH = 'HIGH'
LOW = 'LOW'

slice_ = [LOW, HIGH, LOW, HIGH, LOW]
k = 3

print(logicgate._is_k_down(slice_, k))


print(logicgate._k_voting_evaluate_slice(slice_, k))
