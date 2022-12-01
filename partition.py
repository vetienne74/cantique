from pyqubo import Array
import pprint
import re

# build list of numbers
max=8
numbers = []
x=1
while (x <= max) :
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

# check results
sum1=0
sum2=0
for k, v in best_sample.sample.items():
    #print(k, v)
    s = re.findall(r'\b\d+\b', k)
    val = int(s[0]) + 1
    #print(val)
    if v==0:
        sum1=sum1+val
    else:
        sum2=sum2+val
print('sum1=', sum1)
print('sum2=', sum2)

#end
