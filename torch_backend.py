import torch as t

x = t.tensor([1, 2, 3])
y = t.tensor([[1], [2], [3]])

z = x - y

compare_matrix = t.where(z == 0, 1, 0)
print(compare_matrix)

clues = t.tensor([0, 1, 2])

output = t.empty(3)
output = t.where(clues == 0, x, output)


# cond_list = [arr < 3, arr > 4]
# choice_list = [arr, arr**3]

# gfg = geek.select(condlist, choicelist)
