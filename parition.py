from pyqubo import Array
import pprint

# build list of numbers
max=6
numbers = []
x=0
while (x < max) :
    numbers.append(x)
    x=x+1
pprint.pprint(numbers)

s = Array.create('s', shape=max, vartype='SPIN')
H = sum(n * s for s, n in zip(s, numbers))**2
model = H.compile()
qubo, offset = model.to_qubo()
print('QUBO matrix:')
pprint.pprint(qubo) # doctest: +SKIP

bqm = model.to_bqm()
import neal
sa = neal.SimulatedAnnealingSampler()
sampleset = sa.sample(bqm, num_reads=10)
decoded_samples = model.decode_sampleset(sampleset)
best_sample = min(decoded_samples, key=lambda x: x.energy)
print('Solution:')
pprint.pprint(best_sample.sample)

