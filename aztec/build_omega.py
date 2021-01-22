

reversed_row_dict = dict()
reversed_row_dict[1] =[[k, ] for k in range(0, 2)]


row_dict = dict()
row_dict[1] =[[-k, ] for k in reversed(range(0, 2))]
row_dict[0] = [[0],]



def update_row(row):
    new_row = [x for x in row]

    #print('updating row', row)

    #if row[0] == len(row):
    #    new_row[0] = - new_row[0]

    for idx in range(1, len(row)):
        if abs(row[idx]) == abs(row[idx - 1]):
            new_row[idx] = - abs(new_row[idx])

    return new_row



def get_reverse_row(size):
    if not size in row_dict:
        row_list = []
        prev_list = get_reverse_row(size-1)

        for idx in range(size+1):
            for prev in prev_list:
                if idx == prev[-1]  or idx == prev[-1]+1:
                    row_list.append(prev + [idx])

        reversed_row_dict[size] = row_list

    return reversed_row_dict[size]

def get_row(size):
    if not size in row_dict:
        rev_row_list = get_reverse_row(size)
        row_list = [ [size -x for x in row] for row in rev_row_list]

        signed_row_list = [update_row(row) for row in row_list]

        row_dict[size] = signed_row_list

    return row_dict[size]





# initialize the eta dictionary
omega_dict = dict()
omega_dict[1] = [[[k, ],] for k in range(0,2)]

def get_omega(size):
    if size not in omega_dict:
        omega_list = []
        row_list = get_row(size)
        prev_list = get_omega(size-1)

        for row in row_list:
            for prev in prev_list:
                omega_list.append( [row] + prev)

        omega_dict[size] = omega_list

    return  omega_dict[size]



def increase_magnitude(num, delta):
    if  (num < 0):
        return num-delta
    else:
        return num+delta

def decrease_magnitude(num, delta):
    if  (num < 0):
        return num+delta
    else:
        return num-delta

def get_sign(num):
    if num < 0 :
        return -1
    else:
        return 1

def get_diff_lists(big_row, small_row):
    small_size =  len(small_row)
    #  a vector keeping track of small - big
    diff_row = [ abs(small_row[idx]) -  abs(big_row[idx]) for idx in range(small_size)]

    # a vector keeping track of first time we reach a bigger diff
    # (resets whenever small is below big)
    # the flat moves from small to big at these transitions.
    max_diff_row = []

    max_diff = -1

    for idx in range(small_size):
        if diff_row[idx] > max_diff:
            max_diff = diff_row[idx]

        max_diff_row.append(max_diff)

        if max_diff > -1  and diff_row[idx] < 0:
            # switched back
            max_diff = -1

    return diff_row, max_diff_row

def has_vertical_step_after(row, idx):
    #print('has_vertical_step_after', row, idx)
    if idx == len(row)-1:
        return True
    elif abs(row[idx]) - 1 > abs(row[idx+1]):
        return True
    elif abs(row[idx]) - 1 ==  abs(row[idx+1])  and row[idx+1] < 0:
        return True
    else:
        return False

def comb_rows(big_row_input, small_row_input):

    big_row = big_row_input.copy()
    small_row = small_row_input.copy()


    new_big_row = [b for b in big_row]
    new_small_row = [s for s in small_row]
    small_size = len(small_row)

    #  two vectors that keep track of small - big
    diff_row, max_diff_row = get_diff_lists(big_row, small_row)

    #print('diff_row', diff_row)
    #print('max_diff_row', max_diff_row)

    for idx in range(small_size):
        diff = diff_row[idx]
        max_diff = max_diff_row[idx]

        print('\tidx=', idx, max_diff)
        print('\t\t=', new_big_row)
        print('\t\t=', new_small_row)

        if (max_diff >= 0):
            #print('\taaaaaaa')
            b = big_row[idx]
            s = small_row[idx]

            if (diff >= 0):
                #print('\tAAAAA')
                # paths have intersected (just now or previously)
                b = increase_magnitude(big_row[idx], max_diff+1)
                s = decrease_magnitude(small_row[idx], max_diff+1)
            elif diff == -1 and small_row[idx] > 0:
                #print('\tBBBB')
                # paths are uncrossing
#                b = increase_magnitude(big_row[idx], 1)
#                s = decrease_magnitude(small_row[idx], 1)
                b = increase_magnitude(big_row[idx], 1)
                s = decrease_magnitude(small_row[idx], 1)
                print('zzzzzzzzzzzz')

            if (idx == 0) or max_diff_row[idx] > max_diff_row[idx-1]:
                # switch from D above F to  F above D
                #print('\tCCCC')
                b = - abs(b)
                s = abs(s)

            new_big_row[idx] = b
            new_small_row[idx] = s

        elif abs(small_row[idx]) == abs(big_row[idx+1]) and big_row[idx+1] < 0:
            # the the next step in big_row is a flat step that touches current
            # small_row step
            #print('\tDDDDDD')
            b = big_row[idx]
            s = small_row[idx]

            # s should be a down step (no matter what)
            new_small_row[idx] = abs(s)-1

            if idx == len(small_row)-1:
                # this was the last step of small_row
                # push up the next big step now
                # we are done with this corner intersection
                big_row[idx+1] = increase_magnitude(big_row[idx+1],1)

            elif diff_row[idx+1] < 0:
                # this is a corner intersection: must deal with it

                print('corner intersection', idx)
                # push up the next big step now
                big_row[idx + 1] = increase_magnitude(big_row[idx + 1], 1)

                # lower the small steps until reaching a vertical step
                for j in range(idx,small_size):
                    new_small_row[j] = decrease_magnitude(small_row[j], 1)


                #### previous implementation: I thought we should stop at first down step
                #small_idx = idx

                #while not has_vertical_step_after(small_row, small_idx):
                #    #print('\tlowering next', small_row, small_idx)
                #    small_idx +=1
                #    new_small_row[small_idx] = decrease_magnitude(small_row[small_idx], 1)

                # now must reset the vectors we are using
                # later intersections are affected!
                big_row = new_big_row
                small_row = new_small_row
                diff_row, max_diff_row = get_diff_lists(big_row, small_row)
            else:
                # idx+1 is an intersection on its own
                # so the code will do the right thing
                #print('\tEEEEE')
                pass
        else:
            # this step is perfectly fine
            pass

        print('\t\t=', new_big_row)
        print('\t\t=', new_small_row)

    return [update_row(new_big_row), update_row(new_small_row)]


# when path intersects, raise big and lower small
# when small increases to a new height above big, transfer the flat as well
def twist_rows(big_row_input, small_row_input):

    big_row = big_row_input.copy()
    small_row = small_row_input.copy()

    new_big_row = []
    new_small_row = []

    # track  the difference small[.] -  big[.]
    max_diff = -1

    print(big_row, small_row)

    for idx in range(len(small_row)):
        diff = abs(small_row[idx]) - abs(big_row[idx])
        new_max = False

        # the default values
        b = big_row[idx]
        s = small_row[idx]

        if diff > max_diff:
            max_diff = diff
            new_max = True

        if max_diff >= 0:
            # overlap by an edge or more
            #print('at or above for idx', idx, diff, max_diff)
            #print('\told b and s', big_row[idx], small_row[idx])

            b = increase_magnitude(big_row[idx], max_diff+1)
            s = decrease_magnitude(small_row[idx], max_diff+1)
            #print('\tnew b and s', b, s)

        # elif (idx > 0 and big_row[idx] < 0):
        #     prev_small = abs(small_row[idx-1])
        #     if prev_small == abs(big_row[idx]):
        #         # touch at a point
        #         b = increase_magnitude(big_row[idx], 1)
        #         s = decrease_magnitude(small_row[idx], 1)
        elif (big_row[idx+1] < 0) and abs(small_row[idx]) == abs(big_row[idx+1]):
            # touching a corner. is there more?
            if idx == len(small_row)-1 or abs(small_row[idx+1]) < abs(big_row[idx+1]):
                #print('-------')
                #print('idx', idx)
                #print('big_row[idx+1]<0:', big_row[idx+1])
                #print('abs(small_row[idx]) == abs(big_row[idx+1]):', abs(small_row[idx]), abs(big_row[idx+1]) )
                #print(idx, big_row, small_row)
                # just a corner touch. Let's take care of it
                # xxxab REALLY NEED TO check that this is correct
                big_row[idx + 1] =  increase_magnitude(big_row[idx+1],1)
                if  idx == len(small_row)-1:
                    small_row[idx] = decrease_magnitude(small_row[idx], 1)
                else:
                    small_row[idx + 1] = decrease_magnitude(small_row[idx + 1], 1)


        if diff < 0 and max_diff > -1:
            # we moved below again, so reset max_diff
            max_diff = -1
        elif new_max:
            # a new maximum difference
            # transfer the signs
            max_diff = diff
            b_sign = get_sign(big_row[idx])
            s_sign = get_sign(small_row[idx])
            b =  s_sign * abs(b)
            s =  b_sign * abs(s)

        new_big_row.append(b)
        new_small_row.append(s)

    new_big_row.append(big_row[-1])

    # updating rows to add any new horizontal steps

    #print('\t', update_row(new_big_row), update_row(new_small_row))

    return update_row(new_big_row), update_row(new_small_row)

# this one swapped rows. bad idea!
def old_twist_rows(big_row, small_row):
    new_big_row = []
    new_small_row = []

    for idx in range(len(small_row)):
        if abs(small_row[idx]) >= abs(big_row[idx]):
            b = increase_magnitude(small_row[idx])
            s = decrease_magnitude(big_row[idx])
        else:
            b = big_row[idx]
            s = small_row[idx]

        new_big_row.append(b)
        new_small_row.append(s)

    new_big_row.append(big_row[-1])

    return [new_big_row, new_small_row]


def comb(omega):


    #print('>>>>> combing', omega)
    # make a copy for safety
    triangle = [ [ r for r in row ]  for row in omega]

    size = len(omega)
    for i in range(1, size):
        #print('first dealing with row i=', i)
        for j in reversed(range(1, i+1)):
            #print('\ttwisting rows', j-1,j)
            big_row = triangle[j-1]
            small_row =  triangle[j]

            new_big_row, new_small_row = comb_rows(big_row, small_row)
            triangle[j-1] = new_big_row
            triangle[j]  = new_small_row

            #print('comb', i, j, triangle)

    return triangle


def to_tangle(triangle):
    size = len(triangle)
    path_list = []

    for row_idx in range(size):
        row = triangle[row_idx]
        row_size = len(row)
        my_path =  ['\draw[thick] (-1, ' + str(row_size) + ') -- (0, ' \
                  + str(row[0]) + ')']
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

def to_ytableau(triangle):
    tex_list = [ '$\\begin{ytableau}']
    for row in triangle:
        tex_list.append(' & '.join(str(r) for r in row) + ' \\\\')
    tex_list.append('\\end{ytableau}$')

    return ' '.join(tex_list)


def to_tikz(tri_before, tri_after):
    size = len(tri_before)
    tex_list = ['\\begin{tikzpicture}']
    tex_list.append('\\begin{scope}[shift={(0,0)}]')
#    tex_list.append('\\node at (' + str(-size) + ',' + str(size/2) +') {' + to_ytableau(tri_before) + '};')
    tex_list.append('\\node at (' + str(size/2) + ',' + str(3/2*size) +') {' + to_ytableau(tri_before) + '};')

    tex_list.append(to_tangle(tri_before))
    tex_list.append('\\end{scope}')

    tex_list.append('\\begin{scope}[shift={(' + str(2*size) + ',0)}]')
    tex_list.append('\\node at (' + str(size/2) + ',' + str(3/2*size) +') {' + to_ytableau(tri_after) + '};')
    tex_list.append(to_tangle(tri_after))
    tex_list.append('\\end{scope}')
    tex_list.append('\\end{tikzpicture}')
    tex_list.append('\\bigskip')
    tex_list.append('\\bigskip')

    return '\n'.join(tex_list)


def are_equal(triangle1, triangle2):
    for row1, row2 in zip(triangle1,triangle2):
        for x,y in zip(row1,row2):
            if not x == y:
                return False
    return True

def is_magog(triangle):
    for idx in range(0,len(triangle)-1):
        # biggest NW diag must increase
        if abs(triangle[idx][-1]) < abs(triangle[idx+1][-1]):
            return False


        row = [abs(x) for x in triangle[idx]]
        next_row = [abs(x) for x in triangle[idx+1]]
        # no shared diagonals
        # no crossing
        for j in range(1, len(row)-1):
            if row[j] < row[j-1] and row[j] == next_row[j] and row[j-1] ==  next_row[j-1]:
                #print("failing", triangle)
                return False

            #if row[j] < next_row[j]:
            #    return False

    return True


def test_comb(triangle, expected_triangle):
    combed_triangle = comb(triangle)
    print('----------')
    print('input:', triangle)
    print('expected:', expected_triangle)
    print('output:', combed_triangle)

    if not are_equal(expected_triangle, combed_triangle):
        print('>>>>>>>>>> FAIL!!!!!  <<<<<<<<<<<<<<<')


if __name__ == '__main__':

    print('========================')

    omega_list = [] #get_omega(4)

    omega_str_map = dict()

    equal_count = 0
    magog_count = 0
    duplicate_count = 0

    for t in omega_list:
        print('BEFORE')
        for row in t:
            print(row)
        print('----')

        if are_equal(t,[[4, 3, -3, -3], [3, -3, 2], [2, -2], [0]]):
            print('EQUAL', t)

        print('AFTER')
        triangle = comb(t)
        if str(triangle) in omega_str_map:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>already created', triangle)
            print('\t', t, 'and', omega_str_map[str(triangle)] )
            duplicate_count=duplicate_count+1
        else:
            omega_str_map[str(triangle)] =  t
        for x in triangle:
            print(x)
        print('###########')

        if are_equal(t, triangle):
            equal_count+=1

        if is_magog(t):
            magog_count+=1
        #print(to_tangle(triangle))
        #print(to_ytableau(triangle))
            #print(to_tikz(t, triangle))
            #print('')

    print('equal_count', equal_count)
    print('total', len(omega_str_map))
    print('duplicate', duplicate_count)

#
# omega_list = get_omega(3)
#
# for t in omega_list:
#     for r in t:
#         print(r)
#     print('-----')
# print(len(omega_list))

#rows = get_row(3)

#for r in rows:
#    print(r)

#print(len(omega_list))
#print(len(omega_str_set))

    #print([[4,3,-3,2,-2],[3,-3,-3,-3]])
    #print(twist_rows([4,3,-3,2,-2],[3,-3,-3,-3]))
    #print(twist_rows([4, 3, 2, 1, 0], [3, -3, -3, -3]))

    #print(to_tangle([[3,-2,-2,],[1,1],[0]]))

    #out = comb([[2,-2,-2],[2,-2],[0]])
    #print(out)

    #out = comb([[2,-2,-2],[2,1],[1]])
    #print(out)

    # in_big  = [6,5,4,-4,-4,3]
    # in_small = [5,4,-4,-4,2]
    # out =  twist_rows(in_big,in_small)
    # expected = [[6,5,-5,-5,-4,3],[5,4,3,-3,2]]
    #

    #out = twist_rows([5, -5, -5, -3, -3], [4, -4, 3, -2])
    #print(out)
    # print(expected)

    #start = [[5, -5, -5, -5, -5], [4, 3, -3, -3], [3, -3, 2], [2, -2], [0]]
    # start = [[4, 3, -3, -3], [3, -3, 2], [2, -2], [0]]
    #
    # start = [[2,-2,-2],[2,1],[0]]
    #
    # print(start)
    #
    # end = comb(start)
    # print(end)
    #
    # big_row = [5,-4,3,2,1,0]
    # small_row = [4,3,-2,-2,-2]

    # big_row = [2,-2,-2]
    # small_row = [2,1]
    #

    big_row = [2,1,-1]
    small_row = [2,1]
    my_triangle = [big_row,small_row]
    #my_triangle = [[2,-2,-2],[2,1],[1]]

    #[[2, -2, -2], [1, -1], [1]] and [[2, -2, -2], [2, 1], [0]]

    print('BEFORE', big_row, small_row)
    print('triangle', my_triangle)

    new_big_row, new_small_row = comb_rows(big_row, small_row)

    new_triangle = comb(my_triangle)

    #print('BEFORE', big_row, small_row)

    print('AFTER', new_big_row, new_small_row)

    print('new triangle', new_triangle)


    #test_comb([[2,-2,-2],[2,1],[1]],
    #          [[-3,-3,-2],[-2,0],[0]])



    # test_comb([[2,-2,-2],[2,-1],[0]],
    #           [[-3,-3,-2],[1,-1],[0]])
    #
    # #test_comb([[2,-2,-2],[2,1],[0]],
    # #          [[-3,-3,-2],[1,0],[0]])
    #
    #
    # test_comb([[2,-2,-2],[2,-2],[0]],
    #           [[-3,-3,-2],[1,-1],[0]])
    #
    # test_comb([[2,-2,-2],[1,-1],[1]],
    #           [[-3,-2,-2],[1,-1],[0]])
    print('*********')
    print('*********')
    print('*********')
    print('*********')

    # test_comb([[3, -3, -3, -3], [3, 2, -2], [2, 1], [0]],
    #           [[-4, -4, -4, -3], [-3, 2, -1], [1, 0], [0]])
    #
    # test_comb([[3, -3, -3, -3], [3, 2, -2], [2, -2], [0]],
    #           [[-4, -4, -4, -3], [-3, -3, -1], [0, 0], [0]])
    #
    #
    #
    # test_comb([[3, 2, -2, 1], [2, -2, -2], [2, 1], [1]],
    #           [[-4, -4, -3, 1], [-3, 1, -1], [1, 0], [0]])
    #
    # test_comb([[3, 2, -2, 1], [3, -3, 2], [1, 0], [1]],
    #           [[-4, -4, -4, 1], [-3, 1, 0], [1, 0], [0]])


    #test_comb([[3, -3, 2, 1], [2, 1, -1], [2, 1], [1]],
    #           [[-4, -4, 2, 1], [-3, 1, -1], [1, 0], [0]])

    #test_comb([[3, -3, 2, 1], [3, 2, 1], [1, 0], [1]],
    #           [[-4, -4, 2, 1], [-3, 1, 0], [1, 0], [0]])


def get_index_of_downstep(row, start_idx):
    start_height = row[start_idx]
    row_size = len(row)
    lower_row = [start_height] * (start_idx) + [start_height - j for j in range(row_size - start_idx)]

    diff  = [x - y for x,y in zip (row, lower_row)]

    print(diff)

    # find all the indices where this difference is non-positive
    # we want the SECOND one.
    down_idx_list =  [x for x, val in enumerate(diff)
                                  if val <= 0 ]
    #list(filter(lambda i: i <=0, diff))

    print(down_idx_list)

    if len(down_idx_list) > 1:
        return down_idx_list[1]
    else:
        return row_size



print(get_index_of_downstep([6,6,5,4,3], 0))

