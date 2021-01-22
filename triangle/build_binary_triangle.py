

row_dict = dict();
row_dict[1] = [[k, ] for k in range(0, 2)]

def get_row(size):
    if not size in row_dict:
        prev_list = get_row(size-1)
        new_list1 = [ [0, ] + p for p in prev_list]
        new_list2 = [ [1, ] + p for p in prev_list]
        new_list = new_list1 + new_list2

        row_dict[size] = new_list

    return row_dict[size]

triangle_dict = dict()
triangle_dict[1] = [[[k, ],  ] for k in range(0, 2)]


def get_binary_triangle(size):
    print('gbt', size)
    if not size in triangle_dict:
        prev_list = get_binary_triangle(size-1)
        row_list = get_row(size)
        triangle_list = []

        for row in row_list:
            for prev in prev_list:
                triangle_list.append([row, ] + prev)


        triangle_dict[size] = triangle_list
    else:
        print('size ok', size)

    return triangle_dict[size]


temp = get_binary_triangle(3)

for t in temp:
    print(t)

print(len(temp))

