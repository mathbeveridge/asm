import triangle.array_util as util

# rsst has the reverse rule for the 1's: partial column sums must be weakly increasing


# these are equinumerous with 312 avoiding gog words.
# so we can wr

rsst_map = dict()

rsst_map[1] = [[[k, ],] for k in range(0,2)]

def build_rsst(size):
    if not size in rsst_map:

        max_sums = [k for k in range(1,size+1)]

        first_row_list = util.get_increasing_binary_arrays(size)

        matrix_list = [[row, ] for row in first_row_list]

        for idx in range(1, size):
            row_list = [ [0] *  idx + row  for row in util.get_binary_arrays(size-idx)]

            new_matrix_list = []
            for new_row in row_list:
                for matrix in matrix_list:
                    print('-------')
                    sums = util.get_column_sums(matrix)
                    print('sums before:', sums)
                    sums = [x + y for x,y in zip(new_row, sums)]
                    print('sums after: ', sums)
                    # check still weakly decreasing and beneath max_sums
                    if all(sums[i] <= sums[i+1] for i in range(size-1)) \
                        and all(sums[i] <= max_sums[i] for i in range(size)):
                        new_matrix_list.append( matrix + [new_row])
                        print('\t', (matrix + [new_row]))
            matrix_list = new_matrix_list

        rsst_map[size] = matrix_list

    return rsst_map[size]



rsst_list = build_rsst(2)

for r in rsst_list:
    util.print_array(r)

print('len', len(rsst_list))