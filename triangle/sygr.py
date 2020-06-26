one_sygr = [[[0]], [[1]]]


def add_sygr_layer_two(one_triangles):
    two_triangles = []
    for triangle in one_triangles:
        for x in range(0, 1 + 1):
            for y in range(max(0, x, triangle[0][0]), min(x + 1, 2) + 1):
                new_triangle = [[x, y]] + triangle
                two_triangles = two_triangles + [new_triangle]
    return two_triangles


print('The two-layer (s, y, (g), r) triangles are: ' + str(add_sygr_layer_two(one_sygr)))
print('There are ' + str(len(add_sygr_layer_two(one_sygr))) + ' of them.')

two_sygr = add_sygr_layer_two(one_sygr)


def add_sygr_layer_three(two_triangles):
    three_triangles = []
    for triangle in two_triangles:
        for x in range(0, 1 + 1):
            for y in range(max(0, x, triangle[0][0]), min(x + 1, 2) + 1):
                for z in range(max(0, y, triangle[0][1]), min(y + 1, 3) + 1):
                    new_triangle = [[x, y, z]] + triangle
                    three_triangles = three_triangles + [new_triangle]
    return three_triangles


print('The three-layer (s, y, (g), r) triangles are: ' + str(add_sygr_layer_three(two_sygr)))
print('There are ' + str(len(add_sygr_layer_three(two_sygr))) + ' of them.')

three_sygr = add_sygr_layer_three(two_sygr)


def add_sygr_layer_four(three_triangles):
    four_triangles = []
    for triangle in three_triangles:
        for x in range(0, 1 + 1):
            for y in range(max(0, x, triangle[0][0]), min(x + 1, 2) + 1):
                for z in range(max(0, y, triangle[0][1]), min(y + 1, 3) + 1):
                    for a in range(max(0, z, triangle[0][2]), min(z + 1, 4) + 1):
                        new_triangle = [[x, y, z, a]] + triangle
                        four_triangles = four_triangles + [new_triangle]
    return four_triangles


four_sygr = add_sygr_layer_four(three_sygr)

#print('The four-layer (s, y, (g), r) triangles are: ' + str(four_sygr))
print('# four-layer  (s, y, (g), r) triangles =  ', len(four_sygr))


def add_sygr_layer_five(four_triangles):
    five_triangles = []
    for triangle in four_triangles:
        for x in range(0, 1 + 1):
            for y in range(max(0, x, triangle[0][0]), min(x + 1, 2) + 1):
                for z in range(max(0, y, triangle[0][1]), min(y + 1, 3) + 1):
                    for a in range(max(0, z, triangle[0][2]), min(z + 1, 4) + 1):
                        for b in range(max(0, a, triangle[0][3]), min(a+1,5)+1):
                            new_triangle = [[x, y, z, a, b]] + triangle
                            five_triangles = five_triangles + [new_triangle]
    return five_triangles


five_sygr = add_sygr_layer_five(four_sygr)

print('# five-layer  (s, y, (g), r) triangles =  ', len(five_sygr))
