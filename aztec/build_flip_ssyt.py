import aztec.build_eta as build_eta
import triangle.array_util as util

# row i can start with multiple i's but then is strictly decreasing
# T(i,j) \geq n+1-i-j
# T(i,j) \leq n+i - i
# Columns weakly decreasing


row_dict = dict()
row_dict[1] =[[k, ] for k in range(0, 2)]
row_dict[0] = [[0],]



flip_ssyt_dict = dict()
flip_ssyt_dict[1] =[[[k, ]] for k in range(0, 2)]



# def get_row(size):
#     if not size in row_dict:
#         prev_list = get_row(size-1)
#         new_list = []
#
#
#         for prev in prev_list:
#             new_list.append([size-1,] + prev )
#
#         for prev in prev_list:
#             if prev[0] == size -1:
#                 new_list.append([size,] + prev)
#                 new_list.append([size,] + [1+x for x in prev])
#
#         row_dict[size] = new_list
#
#     return row_dict[size]

def get_row(size):
    return build_eta.get_row(size)


def get_flip_ssyt(size):
    if not size in flip_ssyt_dict:
        prev_list = get_flip_ssyt(size-1)
        new_list = []

        row_list = get_row(size)

        for row in row_list:
            if row == [2,1,0]:
                print("matched", row)


            for prev in prev_list:
                compatible = True
                for idx in range(size-1):
                    if row[idx] < prev[0][idx]:
                        compatible = False
                        break
                    #elif row[idx] == prev[0][idx] and row[idx+1] < row[idx]:
                    elif row[idx+1] < prev[0][idx]:
                        compatible = False
                        break
                if compatible:
                    new_list.append([row,] + prev)

        flip_ssyt_dict[size] = new_list


    return flip_ssyt_dict[size]



tri_list = get_flip_ssyt(2)

for t in tri_list:
    util.print_array(t)

print(len(tri_list))




my_tri_lists = [ get_flip_ssyt(2), get_flip_ssyt(3), get_flip_ssyt(4)]
my_totals = [ util.print_block_totals(x) for x in my_tri_lists]
print('block totals=',my_totals)




