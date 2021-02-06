import copy


# a utility class for creating and processing 2D arrays
# most often these arrays are triangular (but not always)
# functions that return triangles should have 'triangle' in the name
# parameters should be named array_2d to avoid clash with Python's array

# xxxab
# be careful when using functions that return sets of columns and rows from a cached map
# return a copy.deepcopy() of the set of objects.
# Otherwise a change to the arrays in these lists will also affect the cached map



#####################
#### making 2D arrays
####
####
####
####

# returns [[0],[0,0],[0,0,0],...]
def get_all_zero_triangle(size):
    return [[0] * k for k in range(1,size+1)]


bin_array_map = dict();
bin_array_map[1] = [[k, ] for k in range(0, 2)]

# returns all binary arrays for given size
def get_binary_arrays(size):
    if not size in bin_array_map:
        prev_list = get_binary_arrays(size-1)
        new_list1 = [ [0, ] + p for p in prev_list]
        new_list2 = [ [1, ] + p for p in prev_list]
        new_list = new_list1 + new_list2

        bin_array_map[size] = new_list

    return copy.deepcopy(bin_array_map[size])


incr_bin_array_map = dict();
incr_bin_array_map[1] = [[k, ] for k in range(0, 2)]

def get_increasing_binary_arrays(size):
    return [ [0]*k + [1]*(size-k) for k in reversed(range(size+1))]


#####################################
####### manipulating 2d arrays
####
####
####
####

def get_column_sums(array_2d):
    row_size = max([len(row) for row in array_2d])
    sums = [0] * row_size
    for row in array_2d:
        for j in range(len(row)):
            sums[j] += row[j]

    return sums

def transpose_rect(rect_array):
    num_row = len(rect_array)
    num_col = len(rect_array[0])
    new_array = [ [0] * num_row  for _ in range(num_col)]

    for i in range(num_col):
        for j in range(num_row):
            new_array[i][j] = rect_array[j][i]

    return new_array


def anti_transpose_rect(rect_array):
    num_row = len(rect_array)
    num_col = len(rect_array[0])
    new_array = [ [0] * num_row  for _ in range(num_col)]

    for i in range(num_col):
        for j in range(num_row):
            new_array[i][j] = rect_array[num_col-1-j][num_row-1-i]

    return new_array

def flip_triangle(triangle):
    #print(triangle)
    size = len(triangle)
    flip = get_all_zero_triangle(size)
    #print(flip)
    for i in range(size):
        for j in range(i+1):
            #print(i,j,size)
            #print('\t', size-1-i, size-1-j)
            flip[i][j] = triangle[size-1-j][size-1-i]
    return flip

def flip_triangle2(triangle):
    tri  = [row for row in reversed(triangle)]
    flip = flip_triangle(tri)
    return [row for row in reversed(flip)]


def add_arrays(array1, array2):
    new_array = []
    for row1,row2 in zip(array1, array2):
        new_array.append([x+y for x,y in zip(row1,row2)])

    return new_array

############################
####### displaying 2D arrays
####
####
####
####

def print_array(array_2d):
    for row in array_2d:
        print(row)
    print('-----------')


# to draw the array as ytableau in LaTeX
def to_tex_ytableau(array_2d):
    tex_list = ['{\scriptsize $\\begin{ytableau}']
    for row in array_2d:
        tex_list.append(' & '.join(str(r) for r in row) + ' \\\\')
    tex_list.append('\\end{ytableau}$ }')

    return ' '.join(tex_list)


# create tikz for an omega triangle
def omega_to_tangle(triangle):
    size = len(triangle)
    path_list = []

    for row_idx in range(size):
        row = triangle[row_idx]
        row_size = len(row)
        my_path =  ['\draw[thick] (-1, ' + str(row_size) + ') -- (0, ' \
                  + str(abs(row[0])) + ')']
        for col_idx in range(1, row_size):
            height = row[col_idx]
            prev_idx = col_idx - 1
            if height < 0:
                my_path.append(' -- (' + str(prev_idx) + ',' + str(abs(height)) + ')' )
            elif abs(row[col_idx-1]) > abs(height):
                my_path.append(' -- (' + str(prev_idx) + ',' + str(abs(height)+1) + ')' )


            my_path.append(' -- (' + str(col_idx) + ',' + str(abs(height)) + ')')

        if not row[row_size-1] == 0:
            my_path.append(' -- (' + str(row_size-1) + ',0)')

        my_path.append(';')

        path_list.append( ' '.join(my_path))

    return('\n'.join(path_list))


def omega_list_to_tex_file(omega_list, file_name):

    out_file = open(file_name, 'w')

    size = len(omega_list[0])

    lines = ['\\documentclass[12pt]{article}', '\\usepackage{amsmath}', '\\usepackage{ytableau}',
             '\\usepackage{tikz}', '\\begin{document}']


    for idx, triangle in enumerate(omega_list):
        lines.append('\\begin{tikzpicture}[scale=.5]')


        lines.append('\\node at (-' + str(size)  + ',' + str(size/2) + ') {')
        lines.append(idx)
        lines.append('};')


        lines.append('\\node at (0,' + str(size/2) + ') {')
        lines.append(to_tex_ytableau(triangle))
        lines.append('};')

        lines.append('\\begin{scope}[shift={(' + str(size) + ',0)}]')
        lines.append(omega_to_tangle(triangle))
        lines.append('\\end{scope}')

        lines.append('\\end{tikzpicture}')
        lines.append('')
        lines.append('\smallskip')

    lines.append('\\end{document}')

    out_file.writelines(["%s\n" % item for item in lines])
