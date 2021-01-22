
import aztec.build_half_coin as bhc

col_dict = dict()
col_dict[1] =[[k, ] for k in range(0, 2)]


# columns must weakly increase
def get_column(size):
    if not size in col_dict:
        prev_list = get_column(size-1)
        new_list = []
        for idx in range(size+1):
            for prev in prev_list:
                if idx <= prev[0] or (idx == size and prev[0] == size-1):
                    new_list.append([idx,] + prev)
        col_dict[size] = new_list

    return  col_dict[size]


# initialize the ocean dictionary
pst2_dict = dict()
pst2_dict[1] = [[[k, ],] for k in range(0,2)]

# no constraints for columns?
def get_pst2(size):
    if not size in pst2_dict:
        prev_list = get_pst2(size-1)
        col_list = get_column(size)
        new_list = []

        for c in col_list:
            for p in prev_list:
                new_list.append([c,] + p)

        pst2_dict[size] = new_list

    return pst2_dict[size]


temp = get_pst2(2)

#for t in temp:
#    print(t)


def flip(triangle):
    first_col = triangle[0]
    new_triangle = [[x,] for x in first_col]
    for row in triangle[1 : len(triangle)]:
        for idx in range(len(row)):
            new_triangle[idx].append(row[idx])

    return new_triangle


for size in  range(5,6):
    pst2_list = get_pst2(size)
    pst2_list = [flip(t) for t in pst2_list]

    ocean_list = bhc.get_coin_oceans(size)
    stack_list = [ bhc.ocean_to_stack2(t) for t in ocean_list]

    stack_name_list = [str(s) for s in stack_list]


    print('missing in pst:')
    for p in pst2_list:
        if not str(p) in stack_name_list:
            for row in p:
                print(row)
            print('---------')

    print(len(pst2_list))
    print(len(stack_list))

    # for p in stack_list:
    #      for row in p:
    #          print(row)
    #      print('---------')