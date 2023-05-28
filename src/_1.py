import time

from classification import classificationExpense

start = time.time()
gasto = 'verduras-verduras para la semana'
result = classificationExpense(gasto)
end = time.time()
print(result)
print(f'Tiempo de ejecucion: {end - start}')
