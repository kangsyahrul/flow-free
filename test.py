import itertools

a = [1, 2]
b = ['a', 'b', 'c']
c = [4, 5, 6]

for comb in list(itertools.product(a, b, c)):
    print(comb)
    # print((x,y, z))
