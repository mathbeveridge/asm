import triangle.array_util as util
import itertools

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
    #print('gbt', size)
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


def get_binary_triangle_with_subset_order(size):
    num_elements = int((size+1) * size /2)
    elements = range(num_elements)

    tri_list = [ util.get_all_zero_triangle(size)]

    for i in range(1, num_elements+1):
        subset_list = itertools.combinations(elements,i)

        for subset in subset_list:
            data = [0] * num_elements

            for x in subset:
                data[x]=1

            triangle = []
            start_idx = 0
            for j in range(size):
                end_idx = start_idx + j+1
                triangle.append(data[start_idx:end_idx])
                start_idx = start_idx + j+1

            tri_list.append(util.flip_triangle(triangle))

    return tri_list



# alt_triangle_map = dict()
# alt_triangle_map[1] = [[[k, ],  ] for k in range(0, 2)]
#
# def get_binary_triangle_with_alt_order(size):
#     if not size in alt_triangle_map:
#         pass




def get_binary_triangle_with_alt_order(size):
    num_elements = int((size+1) * size /2)
    elements = range(num_elements)

    binary_rows = get_row(num_elements)
    binary_rows.sort()

    tri_list = []

    for data in binary_rows:
        triangle = []
        start_idx = 0
        for j in range(size):
            end_idx = start_idx + j+1
            triangle.append(data[start_idx:end_idx])
            start_idx = start_idx + j+1

        #tri_list.append(util.flip_triangle(triangle))
        tri_list.append(triangle)


    return tri_list









# temp = get_binary_triangle_with_subset_order(3)
#
# for t in temp:
#     print(str(t) + ',' )
# #    print(', '.join(str(x for x in temp)) + ',')
#     #util.print_array(t)
#
# print(len(temp))

