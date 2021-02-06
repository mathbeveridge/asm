import itertools
import triangle.array_util as util

subsets_map = dict()
subsets_map[1] = [[],[1,] ]


def get_subsets(size):
    if not size in subsets_map:
        prev_list = get_subsets(size-1)

        new_list = [x for x in prev_list]

        for prev in prev_list:
            new_list.append( [size,] + prev)

        subsets_map[size] = new_list

    return subsets_map[size]




row_map = dict()
row_map[(1,1)] =[[1, ],[0, ] ]

# strictly decreasing rows
# weakly increasing columns
# num entries in column is strictly less than the max (final value) in the column

# strictly decreasing to 0
# def get_row_old(size):
#     if size == 0:
#         return []
#     elif not size in row_map:
#         my_set = range(1,size+1)
#         row_list = [ [0] * size ]
#         for i in range(1, size+1):
#             subset_list = itertools.combinations(my_set, i)
#             for subset in subset_list:
#                 print('subset', subset)
#                 row = [x for x in reversed(subset)] + [0] * (size -i)
#                 row_list.append(row)
#
#         row_map[size] = row_list
#
#     return row_map[size]

# strictly decreasing to 0
def get_row(max, row_len):
    if row_len == 0:
        return []
    elif not (max, row_len) in row_map:
        my_set = range(1,max+1)
        row_list = [ [0] * row_len ]
        for i in range(1, row_len+1):
            subset_list = itertools.combinations(my_set, i)
            for subset in subset_list:
                row = [x for x in reversed(subset)] + [0] * (row_len -i)
                row_list.append(row)

        row_map[(max, row_len)] = row_list

    return row_map[(max, row_len)]




pp_map = dict()
pp_map[(1,1)] =[[[0,] ] ]

partial_pp_map = dict()
partial_pp_map[(1,1)] =[[[0,] ] ]

def get_key(size, num_col):
    return size*100 + num_col

def get_partial_pp(size, num_col):
    key = get_key(size, num_col)
    if not key in pp_map:
        pp_list = []
        if num_col == 1:
            row_list = get_row(size, 1)
            for row in row_list:
                print(row)
                if not row[0] == 1:
                    pp_list.append([row])

        else:
            prev_pp_list = get_partial_pp(size, num_col-1)
            row_list = get_row(size, num_col)

            for row in row_list:

                if not row[-1] == 1:

                    #print('--------- handling row', row)
                    for pp in prev_pp_list:
                        print('\t\t', pp)

                        if all(row[i] <= pp[0][i] for i in range(num_col - 1)):
                            compatible = True
                            #print('prev', pp)
                            # for j in range(num_col - 1):
                            #     print('\t', j, 'row[j]', row[j], 'pp[j][-1]', pp[j][-1] )
                            #     if row[j] > 0 and pp[j][-1] <= num_col:
                            #         compatible = False
                            #         break
                            if compatible:
                                new_pp = [row] + [ x for x in pp]
                                pp_list.append(new_pp)





        pp_map[key] = pp_list


    return pp_map[key]

def get_pp_old(size):
    prev_list =  get_partial_pp(size, size-1)
    row_list = get_row(size, size)
    pp_list = []

    for row in row_list:
        for pp in prev_list:
            print('\t\t', pp)

            if all(row[i] <= pp[0][i] for i in range(size - 1)):
                compatible = True
                #print('prev', pp)
                for j in range(size - 1):
                    #print('\t', j, 'row[j]', row[j], 'pp[j][-1]', pp[j][-1])
                    if row[j] > 0 and pp[j][-1] <= size:
                        compatible = False
                        break
                if compatible:
                    new_pp = [row] + [x for x in pp]
                    pp_list.append(new_pp)

    return pp_list

def get_pp(size):
    prev_list = get_partial_pp(size, size)
    pp_list = []

   # print('partial size', len(prev_list))

    for pp in prev_list:
        nonzero_count = [0] * size
        for row in pp:
            for i in range(len(row)):
                if row[i]>0:
                    nonzero_count[i] += 1
        #print('nonzero', nonzero_count, pp)

        #util.print_array(pp)

        for i in range(1, size+1):
            print(size-i, i-1)

        max_diag = [pp[size-1-i][i] for i in range(0,size)]

        #print('!!!!!!!!!!!maxdiag', max_diag)


        #print('\tnonzero', nonzero_count, 'maxdiag', max_diag)

        #util.print_array(pp)

        compatible = True


        for i in range(size-1):
            if nonzero_count[i] >= max_diag[i]:
                print('failed current column', i)
            if nonzero_count[i] < max_diag[i+1]:
                print('failed next colunmn', i)



        if all((nonzero_count[i] == 0 or nonzero_count[i] < max_diag[i]) \
                       and nonzero_count[i] >= max_diag[i+1] for i in range(size-1)):
            pp_list.append(pp)

        # for i in range(size-1):
        #     print(nonzero_count[i], pp[size-1-i][i])
        #     print(nonzero_count[i], pp[size - 2 - i][i+1])
        #
        # if compatibile:
        #     pp_list.append(pp)


    return pp_list


    #        if all((nonzero_count[i] == 0 or nonzero_count[i] < max_diag[i]) \
    #                       and nonzero_count[i] >= max_diag[i+1] for i in range(size-1)):


pp_list = get_pp(3)

for pp in pp_list:
    util.print_array(pp)

print(len(pp_list))