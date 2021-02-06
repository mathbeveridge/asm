### this is work that I did with Ian


# deal with ocean by adding the largest diagonal
def diag_layer_list(size):
    if size == 1:
        return [[k, ] for k in range(0,2)]
    else:
        layer_list = []
        prev_list = diag_layer_list(size - 1)
        for x in range(size+1):
            for prev_layer in prev_list:
                if  x == 0 and prev_layer[0] == 0:
                    layer_list.append([x, ] + prev_layer)
                elif x > 0 and x > prev_layer[0]:
                    layer_list.append([x, ] + prev_layer)
        #print('diag layer list', size, layer_list)
        return layer_list


# this checks that columns strictly decrease to 0
# since we have shifted to the left
# nonzeros are strictly increasing
def check_southwest(prev_diag, new_diag):
     for idx in range(len(prev_diag)):
         if prev_diag[idx] > 0 and new_diag[idx] <= prev_diag[idx]:
             return False

     return True


ocean_dict = dict()
ocean_dict[1] = [[[0],],[[1],]]

def build_ocean(n):
    if not n in ocean_dict:
        current_oceans = []
        prev_oceans = build_ocean(n - 1)
        diag_list = diag_layer_list(n)
        for triangle in prev_oceans:
            # print('gog=', gog)
            prev_diag = [triangle[i][i] for i in range(n - 1)]
            # print('prev_diag', prev_diag)
            for diag in diag_list:
                if check_southwest(prev_diag, diag):
                    new_triangle = [[diag[0]], ]
                    for idx in range(n - 1):
                        new_triangle.append(triangle[idx] + [diag[idx + 1]])
                    current_oceans.append(new_triangle)
                    #print('old', triangle, 'new', new_triangle)
        ocean_dict[n] = current_oceans
    return ocean_dict[n]


# this works (returning unique values) as long as we input the arctic oceans
def to_binary_ocean(triangle):
    size = len(triangle)

    #print_array(triangle)

    binary_triangle = [[0 for x in range(idx+1)] for idx in range(size)]

    for col_idx in range(size):
        for row_idx in range(col_idx, size):
            val = triangle[row_idx][col_idx]
            if val > 0:
                binary_triangle[size-val][col_idx] = 1

    #print_array(binary_triangle)

    return binary_triangle

def build_binary_ocean(size):
    return [to_binary_ocean(triangle) for triangle in build_ocean(size)]

def check_stackable(small_triangle, big_triangle):
    small_size = len(small_triangle)

    for row_idx in range(small_size):
        for col_idx in range(row_idx+1):
            if big_triangle[row_idx][col_idx] > small_triangle[row_idx][col_idx]:
                return False
            elif big_triangle[row_idx][col_idx] == 1:
                for idx in range(col_idx,row_idx):
                    print(idx, col_idx)
                    if not small_triangle[idx][col_idx] == big_triangle[idx][col_idx]:
                        return False

    return True


def print_triangle(triangle):
    for t in triangle:
        print(t)
    print('----------')



# for num in range(3,4):
#     ocean_list = build_ocean(num)
#     print(len(ocean_list))
#
#     for ocean in ocean_list:
#         to_binary_ocean(ocean)
#         #print_array(ocean)


#print_array(to_binary_ocean([[3],[2,2],[1,1,1]]))


small_triangle_list = build_binary_ocean(1)
big_triangle_list = build_binary_ocean(2)
bigger_triangle_list = build_binary_ocean(3)
biggest_triangle_list = build_binary_ocean(4)


#for t in bigger_triangle_list:
#    print_array(t)


print(len(small_triangle_list))
print(len(big_triangle_list))
print(len(bigger_triangle_list))
print(len(biggest_triangle_list))


print('------------')


for size in range(1,5):
    bo_list = build_binary_ocean(size)
    str_set = set()
    print(len(bo_list))
    for bo in bo_list:
        str_set.add(str(bo))
    print(len(str_set))




# count = 0
#
# for small in small_triangle_list:
#     for big in big_triangle_list:
#         if check_stackable(small, big):
#             count+=1
#             #print(small, big, bigger)
#
#
# print(count)

big_count = 0
bigger_count = 0
biggest_count = 0

for small in small_triangle_list:
    for big in big_triangle_list:
        if check_stackable(small, big):
            big_count+=1
            for bigger in bigger_triangle_list:
                 if check_stackable(big, bigger):
                    bigger_count+=1
                    for biggest in biggest_triangle_list:
                        if check_stackable(bigger, biggest):
                            biggest_count+=1
                    #print(small, big, bigger)

print('big count', big_count)
print('bigger count', bigger_count)
print('biggest count', biggest_count)