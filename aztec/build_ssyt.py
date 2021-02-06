import aztec.binary_comb as binary_comb
import triangle.array_util as util
import triangle.build_binary_triangle as binary_triangle


# we are going to build a rectangular array that corresponds to SSYT


matrix_map = dict()

# returns a size x size matrix such that
# - each row is a 0-1 vector
# - the sum of column i is i+1
# - each partial sum of the rows is a weakly increasing vector
# (note we are leaving off the "final" row since it is all-ones
# see https://someproofsandstuff.files.wordpress.com/2015/03/hookcon.pdf
# we use row vectors
def get_ssyt_matrix(size):
    if not size in matrix_map:
        max_sums = [k for k in range(1,size)]

        first_row_list = util.get_increasing_binary_arrays(size-1)
        other_row_list = util.get_binary_arrays(size-1)

        matrix_list = [ [ row, ] for row in first_row_list]

        for idx in range(size-1):
            new_matrix_list = []
            for new_row in other_row_list:
                for matrix in matrix_list:
                    sums = util.get_column_sums(matrix)
                    sums = [x + y for x,y in zip(new_row, sums)]

                    # check still weakly decreasing and beneath max_sums
                    if all(sums[i] <= sums[i+1] for i in range(size-2)) \
                        and all(sums[i] <= max_sums[i] for i in range(size-1)):
                        new_matrix_list.append( matrix + [new_row])
            matrix_list = new_matrix_list

        ssyt_list = []
        for m in matrix_list:
            sums = util.get_column_sums(m)
            if all(sums[i] == max_sums[i] for i in range(size-1)):
                # it's easier to understand if we reverse index the rows
                ssyt_list.append([ [x for x in reversed(row)] for row in m])

        ssyt_list = get_sorted(ssyt_list)

        matrix_map[size] = ssyt_list




    return matrix_map[size]


def matrix_to_first_half(matrix):
    size = len(matrix[0])
    matrix = util.transpose_rect(matrix)
    triangle = [ [x for j,x in enumerate(row) if j < size - i] for i,row in enumerate(matrix)]

    return triangle


ssyt_map = dict()


def flip_matrix(matrix_in):
    num_rows = len(matrix_in)
    num_cols = num_rows -1
    path_matrix_list = get_path_matrix_list(matrix_in)


    for m in path_matrix_list:
        util.print_array(m)
        util.print_array(util.anti_transpose_rect(m))
        print('************')


    trans_list = [util.anti_transpose_rect(m) for m in path_matrix_list]

    # remove the unnecessary vertical 1's
    for path_idx, matrix in enumerate(trans_list):

        print('path', path_idx, matrix)

        for j in range(num_rows - path_idx):
            idx = find_first_one_in_col(matrix, j)
            for k in range(idx+1, num_rows):
                matrix[k][j]=0

        # remove first column
        for row in matrix:
            row.pop(0)

    sum_mat = [[0 for x in range(num_cols)] for y in range(num_rows)]

    for matrix in trans_list:
        sum_mat = util.add_arrays(sum_mat, matrix)

    omega = []
    for idx,matrix in enumerate(trans_list):
        omega.append(path_matrix_to_omega_row(matrix, idx))

    return omega


def path_matrix_to_omega_row(matrix, path_idx):
    num_row = len(matrix)
    num_col = num_row - 1
    row = []
    path_length = num_col - path_idx

    prev_idx = path_idx

    for j in range(path_length):
        idx = find_first_one_in_col(matrix, j)
        if (idx == prev_idx):
            row.append(-num_col+idx)
        else:
            row.append(num_col-idx)
        prev_idx = idx

    return row





def get_path_matrix_list(matrix_in):
    num_rows = len(matrix_in)
    num_cols = num_rows - 1
    matrix = [[x for x in row] for row in matrix_in]

    path_matrix_list = []

    # split matrix into its paths
    for i in range(num_cols):
        path_matrix =  [[0 for x in range(num_cols)] for y in range(num_rows)]


        for j in range(num_cols - i):
            idx = find_first_one_in_col(matrix, j)
            path_matrix[idx][j] = 1
            matrix[idx][j] = 0

        # for fix the endpoints
        path_matrix[-1][num_cols-1-i] = 1

        for j in range(num_rows):
            if i == j:
                path_matrix[j] = [1,] + path_matrix[j]
            else:
                path_matrix[j] = [0, ] + path_matrix[j]


        util.print_array(path_matrix)

        # now fill in the 1's in the appropriate columns
        for j in range(num_cols+1  - i):
            idx = find_first_one_in_col(path_matrix, j)
            if j < num_cols - i:
                next_idx = find_first_one_in_col(path_matrix, j+1)
            else:
                next_idx = num_rows

            for k  in range(idx+1, next_idx):
                path_matrix[k][j] = 1


        path_matrix_list.append(path_matrix)



    return path_matrix_list





def find_first_one_in_col(matrix, idx):
    print(matrix, idx)
    num_rows = len(matrix)
    for k in range(num_rows):
        if matrix[k][idx] == 1:
            return k

    raise ValueError("No 1 in column %s of matrix %s", str(idx), str(matrix))




def matrix_to_ssyt(matrix):
    num_row = len(matrix)
    num_col = len(matrix[0])

    scaled_mat = [ [(idx+1)* x for x in row] for idx,row in enumerate(matrix)]
    scaled_mat = util.transpose_rect(scaled_mat)

    #util.print_array(scaled_mat)

    ssyt = [[ x for x in row if x > 0] for row in scaled_mat]


    return ssyt


def ssyt_to_first_half(ssyt):
    size = len(ssyt)+1
    first_half = [[ x for x in row if x < size - idx] for idx,row in enumerate(ssyt)]
    #first_half = [[idx, row] for idx, row in enumerate(ssyt)]

    return first_half


#def ssyt_matrix_to_tikz(matrix):


def index_of_top_one(matrix, col_idx):
    ret_val = -1
    for idx in range(len(matrix)):
        if matrix[idx][col_idx] == 1:
            ret_val = idx
            break

    if ret_val == -1:
        raise ValueError("Did not find a 1 in column %s of %s", col_idx, matrix)

    return ret_val


# the Schroder family only interects on horizontals
def matrix_to_BD(matrix_in):
    matrix = [[x for x in row] for row in matrix_in]
    size = len(matrix) - 1

    B = []
    D = []

    for end_idx in reversed(range(size)):
        b_row = []
        d_row = []

        #prev_idx = size
        top_one_list = [ index_of_top_one(matrix, col_idx) for col_idx in range(end_idx+1)]

        # update B matrix
        prev_idx = size - end_idx - 1

        for col_idx, cur_idx in enumerate(top_one_list):

            if prev_idx == cur_idx:
                b_row.append(0)
            else:
                b_row.append(1)

            prev_idx = cur_idx

            matrix[cur_idx][col_idx] = 0

        B.insert(0,b_row)

        # update D matrix
        #  handle entries in reverse order
        prev_idx = size+1

        for cur_idx in reversed(top_one_list):
            if cur_idx == prev_idx:
                d_row.insert(0, 0)
            else:
                # diagonal step accounts for one height
                d_row.insert(0, prev_idx - cur_idx -1)
            prev_idx = cur_idx

        D.insert(0,d_row)

            # # 0 is flat step, 1 is down step
            # for col_idx in range(end_idx+1):
            #     cur_idx = index_of_top_one(matrix, col_idx)
            #     if prev_idx == cur_idx:
            #         b_row.insert(0, 0)
            #         cur_down = 0
            #         d_row.insert(0, cur_down)
            #     else:
            #         b_row.insert(0, 1)
            #         cur_down =   prev_idx - cur_idx
            #         d_row.insert(0, cur_down)
            #     prev_idx = cur_idx
            #
            #     matrix[cur_idx][col_idx] = 0
            #
            # B.insert(0,b_row)
            # D.insert(0,d_row)

    return B,D


# show the matrix, the ssyt and the paths
def matrix_to_tex(matrix):

    tex_list = ['matrix:', '$\\begin{bmatrix}']

    for row in matrix:
        tex_list.append(' & '.join([str(x) for x in row]) + ' \\\\')

    tex_list.append('\\end{bmatrix}$ \\quad \n')

    # create the ssyt
    ssyt = matrix_to_ssyt(matrix)

    ssyt_tex = 'SSYT: ' + util.to_tex_ytableau(ssyt) + ' \\quad \n tangle:'


    ### create the tangle
    B,D = matrix_to_BD(matrix)
    omega = binary_comb.get_omega(B,D)
    omega_tex = binary_comb.to_tikz_after(omega, False)

    return '\n'.join(tex_list) + ssyt_tex + omega_tex



bin_tri_list = [
    [[0], [0, 0], [0, 0, 0]],
    [[0], [0, 0], [0, 0, 1]],
    [[0], [0, 0], [0, 1, 0]],

    [[0], [0, 0], [0, 1, 1]],
    [[0], [0, 1], [0, 0, 0]],
    [[0], [0, 1], [0, 0, 1]],
    [[0], [0, 1], [0, 1, 0]],
    [[0], [0, 1], [0, 1, 1]],


    [[0], [0, 0], [1, 0, 0]],
    [[0], [1, 0], [0, 0, 0]],
    [[1], [0, 0], [0, 0, 0]],

    [[0], [0, 0], [1, 0, 1]],
    [[0], [1, 0], [0, 0, 1]],
    [[1], [0, 0], [0, 0, 1]],

    [[0], [0, 0], [1, 1, 0]],
    [[0], [1, 0], [0, 1, 0]],
    [[1], [0, 0], [0, 1, 0]],

    [[0], [0, 1], [1, 0, 0]],
    [[0], [1, 1], [0, 0, 0]],
    [[1], [0, 1], [0, 0, 0]],

    [[0], [0, 0], [1, 1, 1]],
    [[0], [1, 0], [0, 1, 1]],
    [[1], [0, 0], [0, 1, 1]],

    [[0], [0, 1], [1, 1, 0]],
    [[0], [1, 1], [0, 1, 0]],
    [[1], [0, 1], [0, 1, 0]],

    [[0], [0, 1], [1, 0, 1]],
    [[0], [1, 1], [0, 0, 1]],
    [[1], [0, 1], [0, 0, 1]],

    [[0], [0, 1], [1, 1, 1]],
    [[0], [1, 1], [0, 1, 1]],
    [[1], [0, 1], [0, 1, 1]],

    [[0], [1, 0], [1, 0, 0]],
    [[1], [0, 0], [1, 0, 0]],
    [[1], [1, 0], [0, 0, 0]],

    [[0], [1, 0], [1, 0, 1]],
    [[1], [0, 0], [1, 0, 1]],
    [[1], [1, 0], [0, 0, 1]],

    [[0], [1, 0], [1, 1, 0]],
    [[1], [0, 0], [1, 1, 0]],
    [[1], [1, 0], [0, 1, 0]],

    [[0], [1, 1], [1, 0, 0]],
    [[1], [0, 1], [1, 0, 0]],
    [[1], [1, 1], [0, 0, 0]],

    [[0], [1, 0], [1, 1, 1]],
    [[1], [0, 0], [1, 1, 1]],
    [[1], [1, 0], [0, 1, 1]],

    [[0], [1, 1], [1, 0, 1]],
    [[1], [0, 1], [1, 0, 1]],
    [[1], [1, 1], [0, 0, 1]],

    [[0], [1, 1], [1, 1, 0]],
    [[1], [0, 1], [1, 1, 0]],
    [[1], [1, 1], [0, 1, 0]],

    [[0], [1, 1], [1, 1, 1]],
    [[1], [0, 1], [1, 1, 1]],
    [[1], [1, 1], [0, 1, 1]],

    [[1], [1, 0], [1, 0, 0]],
    [[1], [1, 0], [1, 0, 1]],
    [[1], [1, 0], [1, 1, 0]],
    [[1], [1, 1], [1, 0, 0]],
    [[1], [1, 0], [1, 1, 1]],
    [[1], [1, 1], [1, 0, 1]],
    [[1], [1, 1], [1, 1, 0]],
    [[1], [1, 1], [1, 1, 1]]
    ]


order_list = [ 0, 1, 2, 8, 4, 5, 6, 17, 9, 12, 15,
               32, 3, 7, 26, 11, 21, 35, 23, 38, 10,
               13, 16, 33, 19, 28, 25, 42, 34, 37, 40,
               56, 22, 31, 48, 36, 46, 57, 51, 58, 18,
               27, 24, 41, 43, 49, 52, 59, 14, 30, 47,
               39, 55, 61, 50, 62, 20, 29, 44, 45, 54,
               60, 53, 63 ]

print(len(set(order_list)))


bin_tri_reordered = [bin_tri_list[k] for k in order_list]


def write_ssyt_matrix(size):
    file_name = '/Users/abeverid/PycharmProjects/asm/data/ssyt' + str(size) + '.txt'

    out_file = open(file_name, 'w')

    matrix_list = get_ssyt_matrix(size)

    for m in matrix_list:
        out_file.writelines(str(m) + '\n')


def compare_to_binary(size):

    file_name = '/Users/abeverid/PycharmProjects/asm/data/ssyt/bin-ssyt' + str(size) + '.tex'

    out_file = open(file_name, 'w')


    lines = ['\\documentclass[12pt]{article}', '\\usepackage{amsmath}', '\\usepackage{ytableau}',
             '\\usepackage{tikz}', '\\begin{document}']

    matrix_list = get_ssyt_matrix(size)
    #triangle_list = binary_triangle.get_binary_triangle_with_subset_order(size-1)
    triangle_list = bin_tri_reordered


    # bin_tri_list

    # matrix_list = [
    #     [[1, 1], [1, 0], [0, 0]],
    #     [[1, 0], [1, 1], [0, 0]],
    #     [[1, 0], [1, 0], [0, 1]],
    #     [[1, 1], [0, 0], [1, 0]],
    #     [[1, 0], [0, 1], [1, 0]],
    #     [[1, 0], [0, 0], [1, 1]],
    #     [[0, 0], [1, 1], [1, 0]],
    #     [[0, 0], [1, 0], [1, 1]]
    # ]
    #
    # triangle_list = [
    #     [[0], [0, 0]],
    #     [[0], [0, 1]],
    #     [[0], [1, 0]],
    #     [[1], [0, 0]],
    #     [[0], [1, 1]],
    #     [[1], [0, 1]],
    #     [[1], [1, 0]],
    #     [[1], [1, 1]]
    # ]


    count = -1
    for t,m in zip(triangle_list, matrix_list):
        count = count+1
        size = len(triangle_list[0])
        t_B, t_D = binary_comb.comb(t)
        t_cliff_omega = binary_comb.get_omega_for_cliff(t)
        t_combed_omega = binary_comb.get_omega(t_B, t_D)

        m_B, m_D = matrix_to_BD(m)
        m_omega = binary_comb.get_omega(m_B,m_D)

        t_invert = [ [ 1 -x for x in row ] for row in reversed(t)]

        print(t, t_invert)


        lines.append('\\begin{tikzpicture}[scale=.5]')

        lines.append('\\node at (0,' + str(size/2) + ') {')
        lines.append(util.to_tex_ytableau(t_invert))
        lines.append('};')

        lines.append('\\begin{scope}[shift={(' + str(1 * size -1) + ',1)}]')
        lines.append(binary_comb.to_tangle2(t_cliff_omega))
        lines.append('\\end{scope}')

        lines.append('\\begin{scope}[shift={(' + str(2.5*size -1) + ',1)}]')
        lines.append(binary_comb.to_tangle2(t_combed_omega))
        lines.append('\\end{scope}')

        lines.append('\\node at (' +  str(4 * size) + ',' + str(size/2) + ') {')
        lines.append(util.to_tex_ytableau(util.flip_triangle2(matrix_to_ssyt(m))))
        lines.append('};')


        lines.append('\\node at (' +  str(5.5 * size) + ',' + str(size/2) + ') {')
        lines.append(util.to_tex_ytableau(m))
        lines.append('};')




        lines.append('\\begin{scope}[shift={( ' + str(6.5 * size) + ',0)}]')
        lines.append(binary_comb.to_tangle(m_omega))
        lines.append('\\end{scope}')

        lines.append('\\node at (' + str(7.5 * size) + ',0) {' + str(count) + '};')

        lines.append('\\end{tikzpicture}')
        lines.append('')

    lines.append('\\end{document}')

    out_file.writelines(["%s\n" % item for item in lines])

    # print("----------------")
    #
    # for m in get_sorted(matrix_list):
    #     util.print_array(m)
    #
    # for t in triangle_list:
    #     util.print_array(t)

def get_sorted(matrix_list):
    my_list = [ util.transpose_rect(m) for m in matrix_list]

    my_list.sort()

    my_list = [ util.transpose_rect(m) for m in reversed(my_list)]

    return my_list


def test():

    for size in range(5,6):
        matrix_list = get_ssyt_matrix(size)

        first_half_list = []

        for m in matrix_list:
            #util.print_array(m)
            # print(' ', m[1][2])
            # print(m[2][1], m[2][2])
            # print('--------')
            #ssyt = matrix_to_ssyt(m)

    #        util.print_array(m)

    #        B, D = matrix_to_BD(m)

    #        print('B')

    #        util.print_array(B)

    #        print('D')
    #        util.print_array(D)

    #        print('omega')
    #        util.print_array(binary_comb.get_omega(B,D))

    #        print('tex')
            print('\n\n')
            print(matrix_to_tex(m))


            #first_half = matrix_to_first_half(m)
            #first_half = ssyt_to_first_half(ssyt)


            #if not first_half in first_half_list:
            #    first_half_list.append(first_half)

                # triangle_list = [ssyt_to_first_half(s) for s in ssyt_list]


                #for t in triangle_list:
            #    util.print_array(t)

        #for f in first_half_list:
        #    util.print_array(f)

        #print(len(matrix_list))
        #print(len(first_half_list))


def test_flip_matrix():

    mat_list = get_ssyt_matrix(3)

    out_list = [flip_matrix(matrix) for matrix in  mat_list]



    for idx in range(len(mat_list)):


        print('the input is')
        util.print_array(mat_list[idx])


        print('the output is')

        util.print_array(out_list[idx])





test_flip_matrix()

#compare_to_binary(4)


#write_ssyt_matrix(5)
