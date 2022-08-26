from keras.metrics import BinaryAccuracy

m= BinaryAccuracy(threshold=0.6)
m.update_state([[1], [1], [0], [0]], [[0.98], [1], [0], [0.6]])
print(m.result().numpy())
l= BinaryAccuracy(threshold=1)
l.update_state([[1], [1], [1], [1]], [[0.98], [1], [0], [0.6]])
print(l.result().numpy())