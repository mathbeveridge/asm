
### These are Permutation Stack Triangles
### we found them by via Aztec Oceans by conjecturing that we should
### replace coin triangles with "coin triangles with overhang"
### Ian suggested cantilever structure. So cool!
### Percolated triangles? Swiss triangles?

# rows can (1) increase or (2) decrease by at most 1
def get_row(size):
    if size == 1:
        return [[k, ] for k in range(0, 2)]
    else:
        prev_list = get_row(size-1)
        new_list = []
        for idx in range(size+1):
            for prev in prev_list:
                if idx <= prev[0]+1:
                    new_list.append([idx,] + prev)
        return new_list


ocean_dict = dict()
ocean_dict[1] = [[[k, ],  ] for k in range(0, 2)]

# columns weakly decrease
def get_ocean_triangle(size):
    if not size in ocean_dict:
        prev_list = get_ocean_triangle(size-1)
        row_list = get_row(size)
        triangle_list = []

        #print(prev_list)

        for row in row_list:
            #print(row)
            for prev in prev_list:
                #print('\t', prev)
                is_compatible = True

                for idx in range(len(row)-1):
                    if row[idx] < prev[0][idx]:
                        is_compatible = False
                        break

                if is_compatible:
                    #print('COMPATIBLE:', row, prev)
                    triangle_list.append([row,] + prev)
                #else:
                    #print('NOT COMPATIBLE:', row, prev)

        ocean_dict[size] = triangle_list

    return ocean_dict[size]

def print_triangle(t):
    for row in t:
        print(row)
    print('--------')


def get_block_totals():
    for size in range(2,6):
        stacks = get_ocean_triangle(size)

        totals = [[0 for j in range(len(stacks[0][i]))] for i in range(len(stacks[0]))]
        #print('totals', totals)

        for s in stacks:
            #print(s)
            for i in range(len(s)):
                for j in range(len(s[i])):
                    totals[i][j]+= s[i][j]


        print('size=', size)
        print('num triangles=', len(stacks))

        #print(totals)
        tot = 0
        for row in totals:
            tot+=sum(row)
        print('total blocks=', tot)
        for x in totals:
            print(x)
        print("----------")




triangle_list = get_ocean_triangle(3)

#for t in triangle_list:
#    print_array(t)

#print(len(triangle_list))

#row_list = get_row(4)

#for r in row_list:
#    print(r)
get_block_totals()