# this creates permutation stack triangles as layers of permutations.

def get_col_list(size):
    if size == 1:
        return [[k, ] for k in range(0,2)]
    else:
        prev_list =  get_col_list(size-1)
        new_list1 = [[0,] + p for p in prev_list]
        new_list2 = [[1,] + p for p in prev_list]
        new_list = new_list1 + new_list2

        return new_list


def get_coin_pyramids(size):
    if size == 1:
        return [[[k, ],] for k in range(0,2)]
    else:
        prev_list = get_coin_pyramids(size-1)
        col_list = get_col_list(size)
        new_list = []
        for prev in prev_list:
            for col in col_list:
                if not 1 in col:
                    new_list.append([col,] + prev)
                else:
                    is_compatible = True
                    for idx in range(len(col)-1):
                        if col[idx] ==1 and  prev[0][idx] == 0:
                            is_compatible = False
                            break

                    if is_compatible:
                        new_list.append([col, ] + prev)
        return new_list


# initialize the ocean dictionary
ocean_dict = dict()
ocean_dict[1] = [[[[k, ],],] for k in range(0,2)]

def get_coin_oceans(size):
    if not size in ocean_dict:
        prev_list = get_coin_oceans(size-1)
        layer_list = get_coin_pyramids(size)
        new_list = []

        #print("previous oceans:", prev_list)

        for layer in layer_list:
            for prev in prev_list:
                is_compatible = True
                for idx1 in range(size-1):
                    for idx2 in range(size - idx1 - 1):
                        #print('layer',layer, 'prev', prev, idx1, idx2)
                        if layer[idx1][idx2] < prev[0][idx1][idx2]:
                            #print('\tNOT compatible')
                            is_compatible = False
                            break
                if is_compatible:
                    new_list.append([layer,]+prev)

        ocean_dict[size] = new_list


    return ocean_dict[size]


# these coin pyramids are staircase shape
# rows weakly increasing 0/1
# this should be a variation on our permutation map
# n+1-j possibilities for column j
def print_coin_pyramid(pyr):
    temp = [sum(p) for p in pyr]
    for i in range(len(temp)-1):
        if temp[i] - temp[i+1] > 1:
            print('**************FAILURE***********')
    for row in pyr:
        print(row)
    #print([sum(p) for p in pyr])
    #print(pyr[0][0] + pyr[1][0]+pyr[2][0], pyr[0][1]+pyr[1][1], pyr[0][2])
    print('+++++++')


def print_triangle(t):
    for row in t:
        print(row)
    print('---------')

def print_coin_pyramid2(pyr):
    print(triangle_to_column(pyr))

# turns a binary triangle into a stacked column
# we sum along columns in level i to get row i
def triangle_to_column(pyr):
    size = len(pyr)
    out = []
    for idx1 in range(size):
        temp = 0
        for idx2 in range(size-idx1):
            temp+= pyr[idx2][idx1]
        out.append(temp)
    return(out)

# columns strictly decrease to 0 and that's it.
def print_coin_ocean(ocean):

    print('*************')
    stack = ocean_to_stack(ocean)
    print_triangle(stack)
    print('><><><><><><><')
    for t in ocean:
        print_triangle(t)
    print('**************')


def ocean_to_stack(ocean):
    stack = [triangle_to_column(row) for row in ocean]
    return stack

# columns are weakly decreasing
# we add layers at the NW corner
def ocean_to_stack2(ocean):
    size = len(ocean)
    triangle = [[ 0  for j in range(size - i)] for i in range(size) ]
    for layer in ocean:
        for i in range(len(layer)):
            for j in range(len(layer[i])):
                triangle[i][j]+=layer[i][j]

    return triangle



# columns are weakly increasing
# we add layers at the SW corner
#  so max triangle is
# 1 1 1
# 2 2
# 3
def ocean_to_stack3(ocean):
    size = len(ocean)
    triangle = [[ 0  for j in range(size - i)] for i in range(size) ]
    for height,layer in enumerate(ocean):
        for i in range(len(layer)):
            for j in range(len(layer[i])):
                triangle[height+i][j]+=layer[i][j]

    return triangle








def get_block_totals():
    for size in range(2,6):
        temp = get_coin_oceans(size)
        stacks = [ocean_to_stack(t) for t in temp]

        totals = stacks[0]

        for s in stacks:
            for i in range(len(s)):
                for j in range(len(s[i])):
                    totals[i][j]+= s[i][j]


        print('size=', size)
        print('num triangles=', len(stacks))
        tot = 0
        for row in totals:
            tot+=sum(row)
        print('total blocks=', tot)
        for x in totals:
            print(x)
        print("----------")




def get_complement(ocean):
    stack = ocean_to_stack(ocean)
    size = len(stack)


    max_tri = [[size -i -j for j in range(size-i) ] for i in range(size) ]



    triangle = [[max_tri[i][j] - stack[i][j] for j in range(size-i) ] for i in range(size) ]

    return triangle


def get_colsum(triangle):
    size = len(triangle)

    sums = []

    for i in range(size):
        sum = 0
        for j in range(size-i):
            sum+= triangle[i][j]
        sums.append(sum)
    return sums

# this takes us back to the original permutation form
# rows can decrease by at most 1
# columns weakly decreasing
def ocean_to_colsum_triangle(ocean):
    triangle = []
    for t in ocean:
        triangle.append(get_colsum(t))

    return triangle


#
def push_triangle_south(triangle):
    size = len(triangle)
    out = []
    for i in range(size):
        row = []
        for j in range(i+1):
            row.append(triangle[i-j][j])
        #out.append(row)
        out.insert(0,row)

    return out


def push_ocean_south(ocean):
    new_ocean = [push_triangle_south(t) for t in ocean]

    return new_ocean


# for i in range(3,4):
#     temp = get_coin_oceans(i)
#     for t in temp:
#         print_coin_ocean(t)
#     print(len(temp))

for i in range(2, 2):
    temp = get_coin_oceans(i)
    #for t in temp:
    #    comp = get_complement(t)
    #    print_triangle(comp)

    stack_set1 = set()
    stack_set2 = set()
    ss1_rows = set()
    ss2_rows = set()

    for t in temp:
        print('START<<<<<<<<<')
        #print_coin_ocean(t)
        s = ocean_to_stack(t)
        stack_set1.add(str(s))
        ss1_rows.add(str(s[0]))
        #s = ocean_to_stack3(t)
        #stack_set2.add(str(s))
        #ss2_rows.add(str(s[0]))

        for row in t:
            print_triangle(row)

        print_triangle(s)

        #t2 = ocean_to_colsum_triangle(t)

        #print_triangle(t2)
        #print('push south')
        #s = push_ocean_south(t)
        #print_triangle(ocean_to_stack2(s))
        #print_coin_ocean(s)
        #print('??????????????????')


    print(len(temp))
    print(len(stack_set1))
    print(len(stack_set2))

    # print('ss2 but not ss1')
    # for x in ss2_rows:
    #     if x not in ss1_rows:
    #         print(x)
    #
    for x in stack_set1:
        if  x  in stack_set2:
            print(x)

    #print(len(ss1_rows))
    #print(len(ss2_rows))


    #get_block_totals()

    ### MY STACK METHOD IS BAD! NEED TO ADD ALONG COLUMNS NOT ROWS


