import time

from classification import classificationExpense

start = time.time()
gasto = 'carne - carne de res'
result = classificationExpense(gasto)
end = time.time()
print(result)
print(f'Tiempo de ejecucion: {end - start}')
