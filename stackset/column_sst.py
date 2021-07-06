
import triangle.array_util as util



col_map = dict()

col_map[1] = [ [0,], [1,]]


def get_columns(size):
    if not size in col_map:
        prev_list = get_columns(size-1)
        new_list = []

        for prev in prev_list:
            count = [prev.count(x) for x in range(size)]

            new_list.append([0,] + prev)
            new_list.append([1, ] + prev)

            for x in range(2, size):
                if count[x-1] > count[x]:
                    new_list.append([x,] + prev)

            if count[size-1] > 0:
                new_list.append([size,] + prev)




        col_map[size] = new_list

    return col_map[size]



def to_sst(columns):
    size = len(columns)
    triangle = util.get_all_zero_triangle(size)

    for idx,x in enumerate(reversed(columns)):
        if x > 0:
            triangle[idx][x-1] = 1

    return triangle



for size in range(4,5):
    col_list = get_columns(size)
    for c in col_list:
        print('column is', c)
        util.print_array(to_sst(c))

    print('count', len(col_list))