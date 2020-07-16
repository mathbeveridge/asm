# This code generates inverted SSTs with exactly one 1 per diagonal
# Equivalently, we are searching for SSTs with exactly one 0 per diagonal
#
# To start, a troubling observation. If we take a valid SST of this form and shave off one of its diagonals, we do *not*
# necessarily get a valid SST of size one below. Eg:
# 1
# 1 0
# 0 0 1
# is valid but if we shave off the outermost diagonal, we get
# 1
# 0 0
# which is invalid. So we cannot recursively build on smaller SSTs to get bigger ones.
# Instead, what I'm going to try is just recursively making all triangles with one 0 per diagonal and filtering out
# all the ones that are not SSTs

valid_one_layer = [[[0]]]


def generate_next_layer_unfiltered(previous_layer):
    next_layer_unfiltered = []

    for entry in previous_layer:
        base = []
        for i in range(len(entry)):
            base += [list(entry[i])]
        base = [[1]] + base
        for i in range(len(base) - 1):
            base[i+1] += [1]
        for i in range(len(base)):
            variant = []
            for j in range(len(base)):
                variant += [list(base[j])]
            variant[i][i] = 0
            next_layer_unfiltered += [variant]

    return next_layer_unfiltered


unfiltered_two_layer = generate_next_layer_unfiltered(valid_one_layer)
unfiltered_three_layer = generate_next_layer_unfiltered(unfiltered_two_layer)
unfiltered_four_layer = generate_next_layer_unfiltered(unfiltered_three_layer)
unfiltered_five_layer = generate_next_layer_unfiltered(unfiltered_four_layer)
unfiltered_six_layer = generate_next_layer_unfiltered(unfiltered_five_layer)
unfiltered_seven_layer = generate_next_layer_unfiltered(unfiltered_six_layer)
unfiltered_eight_layer = generate_next_layer_unfiltered(unfiltered_seven_layer)


def filter_ssts(potential_ssts):
    made_it = []
    for entry in potential_ssts:
        passed = 0
        for j in range(len(entry)-1):
            current_layer = list(entry[j])
            next_layer = list(entry[j+1])
            ones = [i for i, x in enumerate(current_layer) if x == 1]
            num_passed = 0
            for i in ones:
                if sum(next_layer[i:len(next_layer)]) >= sum(current_layer[i:len(current_layer)]):
                    num_passed += 1
            if num_passed == sum(current_layer):
                passed += 1
        if passed == len(entry) - 1:
            made_it += [entry]
    return made_it


print(filter_ssts(valid_one_layer))
print(filter_ssts(unfiltered_two_layer))
print(filter_ssts(unfiltered_three_layer))
print(filter_ssts(unfiltered_four_layer))
print(len(filter_ssts(valid_one_layer)))
print(len(filter_ssts(unfiltered_two_layer)))
print(len(filter_ssts(unfiltered_three_layer)))
print(len(filter_ssts(unfiltered_four_layer)))
print(len(filter_ssts(unfiltered_five_layer)))
print(len(filter_ssts(unfiltered_six_layer)))
print(len(filter_ssts(unfiltered_seven_layer)))
print(len(filter_ssts(unfiltered_eight_layer)))
