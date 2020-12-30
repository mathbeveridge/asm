
def get_col_list(size):
    if size == 1:
        return [[k, ] for k in range(0,2)]
    else:
        prev_list =  get_col_list(size-1)
        new_list = [[0,] + p for p in prev_list]
        for p in prev_list:
            if p[0] == 1:
                new_list.append([1,] + p)

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
                    idx = col.index(1)
                    if idx == len(prev[0]):
                        new_list.append([col, ] + prev)
                    elif prev[0][idx] == 1:
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


def print_coin_pyramid(pyr):
    temp = [sum(p) for p in pyr]
    for i in range(len(temp)-1):
        if temp[i] - temp[i+1] > 1:
            print('**************FAILURE***********')
    for p in pyr:
        print(p)
    print([sum(p) for p in pyr])
    print('++++++++')

def print_coin_ocean(ocean):
    for pyr in ocean:
        print(pyr)
        print_coin_pyramid(pyr)
    print('----------')


for size in range(1,5):
    #temp = get_coin_oceans(size)
    temp = get_coin_pyramids(size)

    for t in temp:
        print_coin_pyramid(t)
#    print_coin_ocean(t)

    print(len(temp))