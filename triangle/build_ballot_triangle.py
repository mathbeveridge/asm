import triangle.array_util as util
import aztec.binary_comb as comb
import logging


# BALLOT TRIANGLES
# these triangles have shape
# xxx
# xx
# x
#
# and rules:
# col decr by at most 1 (can increase too)
# row weak decr
# NE diag decr at most 1


def get_row_list(size):
    if size ==  1:
        return [ [0,], [1,]]
    else:
        previous_list = get_row_list(size-1)
        row_list = []
        for k in range(size+1):
            for prev_row in previous_list:
                if k >= prev_row[0]:
                    row_list.append( [k,]  + prev_row.copy())

        return row_list


##### be careful! you should really clone everything.

def build_bt(size):
    if size == 1:
        return [ [[0,],], [[1,],]]
    else:
        previous_list =  build_bt(size-1)
        row_list =  get_row_list(size)

        bt_list = []

        count = 0

        for prev in previous_list:
            prev_row = prev[0]

            for row in row_list:
                row_ok = True

                #  check col decrease by at most 1 (note: can increase)
                for i in range(len(prev_row)):
                    if row[i] - prev_row[i]  > 1:
                        row_ok =  False
                        break

                # do we need to check the diag, or is it forced?
                # if (row_ok):
                #     for i in range(len(prev_row)):
                #         if row[i+1] - prev_row[i]   > 1:
                #             row_ok =  False
                #             break


                if row_ok:
                    bt = [ p.copy() for p in prev]
                    bt.insert(0,row)
                    bt_list.append(bt)

                    count = count + 1

                    #if count % 1000 == 0:
                    #    print('bt count', count)
    return bt_list

def get_boosted_triangle(triangle):
    boosted = []
    for  idx,row in enumerate(triangle):
        boosted.append([ x + idx for x in row])

    return boosted


def to_tangle(triangle_in):

    triangle = get_boosted_triangle(triangle_in)
    size = len(triangle)
    path_list = []

    for row_idx in range(size):
        row = triangle[row_idx]
        row_size = len(row)

        start_x_val = size - row_idx

        my_path =  ['\draw[thick] (' + str(start_x_val)  + ',' + str(size) + ') -- ('
                    +  str(start_x_val)  + ',' + str(abs(row[0])) + ')']
        for col_idx in range(1, row_size):
            height = row[col_idx]
            prev_idx = col_idx - 1

            if row[prev_idx] - height > 1:
                # which version to we want? we have 2 choices.
                # v-less
                my_path.append(' -- (' + str(start_x_val - col_idx) + ',' + str(row[prev_idx]-1) + ')' )
                # truncated
                #my_path.append(' -- (' + str(start_x_val - prev_idx) + ',' + str(height+1) + ')' )

            my_path.append(' -- (' + str(start_x_val - col_idx) + ',' + str(height) + ')')


        my_path.append(' -- (0,' + str(size - row_size) + ')')

        my_path.append(';')

        path_list.append( ' '.join(my_path))

    return('\n'.join(path_list))


def to_tikz(triangle):
    size = len(triangle)
    tex_list = ['\\begin{tikzpicture}[scale=.5]']
    tex_list.append('\\begin{scope}[shift={(0,0)}]')
    #    tex_list.append('\\node at (' + str(-size) + ',' + str(size/2) +') {' + to_tex_ytableau(tri_before) + '};')
    tex_list.append('\\node at (' + str(-size) + ',' + str(1 / 2 * size) + ') {\scriptsize ' + util.to_tex_ytableau(
        triangle) + '};')

    tex_list.append(to_tangle(triangle))
    tex_list.append('\\end{scope}')

    tex_list.append('\\end{tikzpicture}')
    tex_list.append('\\qquad')
    #tex_list.append('\\bigskip')

    return '\n'.join(tex_list)


# def get_down_for_ballot(triangle):
#         size = len(B)
#         D = get_all_zero_triangle(size)
#         for k in range(size):
#             # print('B[k]', k, B[k])
#             D[k][k] = k + 1 - sum([B[k][j] for j in range(k + 1)])
#         return D


def to_BD(triangle):
    size = len(triangle)
    B = util.get_all_zero_triangle(size)
    D = util.get_all_zero_triangle(size)

    tiered = [[x+ idx for x in row] for idx, row in enumerate(triangle)]

    path_triangle = [[size - x for x  in reversed(row)]  for row in reversed(tiered)]

    #util.print_array(path_triangle)

    #tiered = [ [size -  x - idx for  x in row] for idx,row in enumerate(triangle)]

    #path_triangle = [[x for x in reversed(row)] for row in reversed(tiered)]

    #path_triangle = [ [size - x - idx  for x in reversed(row)] for idx,row in enumerate(triangle)]

    #path_triangle = [x for x in reversed(path_triangle)]

    #print('ballot')
    #util.print_array(triangle)
    #print('path triangle')
    #util.print_array(path_triangle)

    for row_idx,row in enumerate(path_triangle):
        if row[0] == row_idx:
            B[row_idx][0] = 1

        for col_idx in range(1, len(row)):
            if row[col_idx] < row[col_idx-1]:
                B[row_idx][col_idx] = 1


        D[row_idx][-1] = row[-1]

        for col_idx in range(0, len(row)-1):
            if row[col_idx] > row[col_idx+1] + 1:
                D[row_idx][col_idx] = row[col_idx] - row[col_idx+1] - 1

    #print('binary')
    #util.print_array(B)
    #print('down')
    #util.print_array(D)

    return B,D


def is_row_gog(bt):
    is_good = True
    for row in bt:
        for idx in range(len(row)-1):
            if row[idx+1] - row[idx] > 1:
                is_good = False
                break
        if not is_good:
            break
    return is_good


def get_block_totals():
    for size in range(2,4):
        stacks = build_bt(size)

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


####### ADAPTING COMB

def comb_BD(binary_triangle, down_triangle):
    size = len(binary_triangle)
    B = [[x for x in row] for row in binary_triangle]
    D = [[x for x in row] for row in down_triangle]

    print('comb_DB start')
    print(B)
    print(D)
    print('omega')
    print(comb.get_omega(B,D))

    for k in reversed(range(size)):
        print('\tcomb row', k)
        #### we already have a starting value for D[k][k]
        #D[k][k] =  sum([B[k][j] for j in range(k+1)])
        print('\t\t@ adjusting D[k][k] for k=', k )
        print('\t\t\tk+1=', k+1 )
        print('\t\t\tB[k][0..k]=', [B[k][j] for j in range(k+1)] )
        print('\t\t\tD[k][0..k]=', [D[k][j] for j in range(k+1)] )

        old_dkk = D[k][k]
        print('\t\t\tD[k][k] old=', D[k][k])
        #D[k][k] = k+1 - sum([B[k][j] + D[k][j] for j in range(k+1)])
        #D[k][k] = k + 1 - sum([B[k][j] for j in range(k + 1)]) - sum([D[k][j] for j in range(k + 1)])
        print('\t\t\tD[k][k] new=', D[k][k])
        if not old_dkk == D[k][k]:
            TypeError('FAILURE')
        for i in range(k,size-1):
            print('\tuntangle', i, k)
            B,D = untangle(B,D,i,k)
            print('\t\t', B)
            print('\t\t', D)

    print('comb_DB returning')
    print(B)
    print(D)
    print('omega')
    print(comb.get_omega(B, D))
    print('++++++++++++++++++++++++')

    return B,D


# untangle rows i and i+1 up to column k
def untangle(B, D, i, k):
    #print('untangle', i, k, B, D)
    cur = 0
    d = 0
    s = 0

    print('\t\t\ti=', i, 'k=', k)
    print('\t\t\tbefore')
    print('\t\t\t\t', B)
    print('\t\t\t\t', D)
    print('\t\t\t\tomega')
    print('\t\t\t\t', comb.get_omega(B,D))

    # CUR should be the gap. STILL NEED TO FIX THIS ARGH!!!!

    for j in range(k+1):
        # ORIGINAL
        cur = cur + B[i+1][j] - B[i][j]
        if (j>0):
            cur = cur + D[i+1][j] - D[i][j-1]
        # BALLOT?
        #cur = cur + B[i + 1][j] - D[i+1][j] - B[i][j] + D[i+1][j]
        print('row i', i ,'col j', j, 'cur', cur, 'd', d)
        if cur > d:
            print('\tYES swap')
            d = cur
            s = s + d - cur
            #print('$$$$$$$$$$$ hit it')
            # interchange direction of steps
            B[i][j] = 1
            B[i+1][j] = 0
        else:
            print('\tno swap')
        # distribute the push downwards if we can
        h = D[i][j]
        if h <= s:
            D[i][j] = 0
            s = s - h
        else:
            D[i][j] = h - s
            s=0

    # transfer d vertical steps to P_{i+1}
    print('\tmoving d', d, 'steps from i,k', i, k)
    ######## HERE IS WHERE THE CHANGE NEEDS TO BE!
    D[i][k] = D[i][k] - d
    # ORIGINAL
    #D[i+1][k] = d
    # BALLOT?
    D[i+1][k] = D[i+1][k] + d
    #print('untangle returning', i, k, B, D)

    print('\t\t\tafter')
    print('\t\t\t\t', B)
    print('\t\t\t\t', D)
    print('\t\t\t\tomega')
    print('\t\t\t\t', comb.get_omega(B, D))

    print(min(D[i]))

    if min(D[i]) < 0:
       raise ValueError(' '.join(['Untangle removed too many blocks (B,D,i,k)', str(B), str(D), str(i), str(k)]))


    return B,D

def increase_magnitude(num, delta):
    if  (num < 0):
        return num-delta
    else:
        return num+delta

def decrease_magnitude(num, delta):
    #print('decreasing', num, delta)
    if  (num < 0):
        return num+delta
    else:
        return num-delta

def get_sign(num):
    if num < 0 :
        return -1
    else:
        return 1


def separate_working(omega, i, k):

    logging.debug('separate %s %s %s', omega, i, k)

    big_row = omega[i]
    small_row = omega[i+1]

    gap = 0
    d = 0



    logging.debug('\tbig %s',big_row)
    logging.debug('\tsmall %s', small_row)

    for j in range(k):
        logging.debug('\t\t', j)
        logging.debug('\t\tcomparing %s %s', abs(small_row[j]), abs(big_row[j]))
        gap =  abs(small_row[j]) - abs(big_row[j])

        logging.debug('\t\tgap %s', gap)

        if gap >= d:
            logging.debug('****** new d', gap+1, 'at idx', j)
            d = gap+1
            small_row[j] = abs(small_row[j])
            big_row[j] = -(abs(big_row[j]))

        logging.debug('\t\tchange d= %s', d)
        small_row[j] = decrease_magnitude(small_row[j],d)
        big_row[j] = increase_magnitude(big_row[j], d)

    omega[i] = big_row
    omega[i+1] = small_row

    return omega


# deal with big drop and small drop on the fly
# we use down steps as we encounter them
# only flatten big step when it's not a drop
def separate_v1(omega, i, k):
    logging.debug('begin separate %s %s %s', omega, i, k)

    big_row = omega[i]
    small_row = omega[i + 1]

    gap = 0
    d = 0
    s = 0

    # need to keep track of the vertical steps to absorb changes
    small_drop = [len(small_row) - abs(small_row[0]), ]

    for small_idx in range(1, len(small_row)):
        small_drop.append(abs(small_row[small_idx - 1]) - abs(small_row[small_idx]))

    logging.debug('small drop %s', small_drop)

    logging.debug('\tbig %s', big_row)
    logging.debug('\tsmall %s', small_row)

    for j in range(k):
        logging.debug('\t\t j=%s', j)
        logging.debug('\t\tcomparing %s %s', abs(small_row[j]), abs(big_row[j]))
        gap = abs(small_row[j]) - abs(big_row[j])

        logging.debug('\t\tgap %s', gap)

        if gap >= d:
            s = s + gap - d + 1
            d = gap + 1
            logging.debug('****** new s=%s d=%s at idx %s', s, d, j)
            # exchange flat and down: heights changed below
            small_row[j] = abs(small_row[j])
            big_row[j] = -(abs(big_row[j]))

        if j > 0:
            drop = small_drop[j]

            logging.debug('******* drop  %s', drop)
            if drop > 1:
                s = max([0, s - drop + 1])

        logging.debug('\t\tchange big by d=%s', d)
        big_row[j] = increase_magnitude(big_row[j], d)
        logging.debug('\t\tchange small by s=%s', s)
        small_row[j] = decrease_magnitude(small_row[j], s)

    omega[i] = big_row
    omega[i + 1] = small_row

    logging.debug('end separate %s %s %s', omega, i, k)

    return omega

# deal with small drop at the end
def separate_v2(omega, i, k):

    logging.debug('begin separate %s %s %s', omega, i, k)

    big_row = omega[i]
    small_row = omega[i+1]

    gap = 0
    d = 0
    s = 0

    diff_list = []

    # need to keep track of the vertical steps to absorb changes
    small_drop = [len(small_row) - abs(small_row[0]),]


    for small_idx in range(1, len(small_row)):
        small_drop.append(abs(small_row[small_idx-1]) - abs(small_row[small_idx]))

    small_slack_list = [0]

    for small_idx in range(1, len(small_row)):
        if small_drop[small_idx] > 1:
            new_slack = small_drop[small_idx] - 1
        else:
            new_slack = 0
        small_slack_list.append(small_slack_list[-1] + new_slack)


    logging.debug('small drop %s', small_drop)


    logging.debug('\tbig %s',big_row)
    logging.debug('\tsmall %s', small_row)

    for j in range(k):
        logging.debug('\t\t j=%s', j)
        logging.debug('\t\tcomparing %s %s', abs(small_row[j]), abs(big_row[j]))
        gap =  abs(small_row[j]) - abs(big_row[j])

        logging.debug('\t\tgap %s', gap)

        if gap >= d:
            d = gap+1
            logging.debug('****** new s=%s d=%s at idx %s', s, d, j)
            # exchange flat and down: heights changed below
            small_row[j] = abs(small_row[j])
            big_row[j] = -(abs(big_row[j]))

        diff_list.append(d)

        logging.debug('\t\tchange big by d=%s', d)
        big_row[j] = increase_magnitude(big_row[j], d)

        # how much to lower the small path
        s = max(0, d - small_slack_list[j])

        logging.debug('\t\tchange small by s=%s', s)
        small_row[j] = decrease_magnitude(small_row[j],s)


    omega[i] = big_row
    omega[i+1] = small_row

    logging.debug('end separate %s %s %s', omega, i, k)

    return omega




# deal with small drop at the end
# bijective for n <= 3
def separate_v3(omega, i, k):

    logging.debug('begin separate %s %s %s', omega, i, k)

    big_row = omega[i]
    small_row = omega[i+1]

    gap = 0
    d = 0
    s = 0
    changed_prev = False

    # need to keep track of the vertical steps to absorb changes
    small_drop = [len(small_row) - abs(small_row[0]),]


    for small_idx in range(1, len(small_row)):
        small_drop.append(abs(small_row[small_idx-1]) - abs(small_row[small_idx]))

    small_slack_list = [0]

    for small_idx in range(1, len(small_row)):
        if small_drop[small_idx] > 1:
            new_slack = small_drop[small_idx] - 1
        else:
            new_slack = 0
        small_slack_list.append(small_slack_list[-1] + new_slack)


    logging.debug('small drop %s', small_drop)


    logging.debug('\tbig %s',big_row)
    logging.debug('\tsmall %s', small_row)

    change_list = []

    for j in range(k):
        logging.debug('\t\t j=%s', j)
        logging.debug('\t\tcomparing %s %s', abs(small_row[j]), abs(big_row[j]))
        gap =  abs(small_row[j]) - abs(big_row[j])

        logging.debug('\t\tgap %s', gap)

        if gap >= d:
            d = gap+1
            logging.debug('****** new s=%s d=%s at idx %s', s, d, j)
            # exchange flat and down: heights changed below
            small_row[j] = abs(small_row[j])
            if j == 0 or abs(big_row[j]) == abs(big_row[j-1]) - 1:
                # only flatten when there  was no drop
                big_row[j] = -(abs(big_row[j]))


        # how much to raise/lower the paths
        # absorb down steps as we encounter them
        s = max(0, d - small_slack_list[j])

        change_list.append(s)

        logging.debug('\t\tchange big by s=%s', s)
        big_row[j] = increase_magnitude(big_row[j], s)
        logging.debug('\t\tchange small by s=%s', s)
        small_row[j] = decrease_magnitude(small_row[j], s)

    for j in range(k-1):
        if change_list[j] > 0 and change_list[j+1] == 0:
            # mark with flat step
            logging.debug('\t\tflattening big entry to mark end of change j=%s', j)
            big_row[j+1] = -abs(big_row[j+1])

    if change_list[k-1] > 0:
        logging.debug('\t\tflattening last big entry to mark end of change j=%s', j)
        big_row[k] = -abs(big_row[k])

    omega[i] = update_row(big_row)
    omega[i+1] = update_row(small_row)

    logging.debug('end separate %s %s %s', omega, i, k)

    return omega





# commented out "deal with small drop at the end"
def separate(omega, i, k):

    logging.debug('begin separate %s %s %s', omega, i, k)

    big_row = omega[i]
    small_row = omega[i+1]

    gap = 0
    d = 0
    s = 0
    changed_prev = False

    # need to keep track of the vertical steps to absorb changes
    small_drop = [len(small_row) - abs(small_row[0]),]


    for small_idx in range(1, len(small_row)):
        small_drop.append(abs(small_row[small_idx-1]) - abs(small_row[small_idx]))

    small_slack_list = [0]

    for small_idx in range(1, len(small_row)):
        if small_drop[small_idx] > 1:
            new_slack = small_drop[small_idx] - 1
        else:
            new_slack = 0
        small_slack_list.append(small_slack_list[-1] + new_slack)


    logging.debug('small drop %s', small_drop)


    logging.debug('\tbig %s',big_row)
    logging.debug('\tsmall %s', small_row)

    change_list = []

    for j in range(k):
        logging.debug('\t\t j=%s', j)
        logging.debug('\t\tcomparing %s %s', abs(small_row[j]), abs(big_row[j]))
        gap =  abs(small_row[j]) - abs(big_row[j])

        logging.debug('\t\tgap %s', gap)

        if gap >= d:
            d = gap+1
            logging.debug('****** new s=%s d=%s at idx %s', s, d, j)
            # exchange flat and down: heights changed below
            small_row[j] = abs(small_row[j])
            if j == 0 or abs(big_row[j]) == abs(big_row[j-1]) - 1:
                # only flatten when there  was no drop
                big_row[j] = -(abs(big_row[j]))

        # if small drops and intersects the next (flat) big step, then push up
        # that next big step
        if abs(small_row[j]) == - big_row[j+1]:
            big_row[j+1] = abs(big_row[j+1])



        # how much to raise/lower the paths
        # absorb down steps as we encounter them
        s = max(0, d - small_slack_list[j])

        change_list.append(s)

        logging.debug('\t\tchange big by s=%s', s)
        big_row[j] = increase_magnitude(big_row[j], s)
        logging.debug('\t\tchange small by s=%s', s)
        small_row[j] = decrease_magnitude(small_row[j], s)

    # for j in range(k-1):
    #     if change_list[j] > 0 and change_list[j+1] == 0:
    #         # mark with flat step
    #         logging.debug('\t\tflattening big entry to mark end of change j=%s', j)
    #         big_row[j+1] = -abs(big_row[j+1])
    #
    # if change_list[k-1] > 0:
    #     logging.debug('\t\tflattening last big entry to mark end of change j=%s', j)
    #     big_row[k] = -abs(big_row[k])

    omega[i] = update_row(big_row)
    omega[i+1] = update_row(small_row)

    logging.debug('end separate %s %s %s', omega, i, k)

    return omega







def update_row(row):
    new_row = [x for x in row]

    #print('updating row', row)

    #if row[0] == len(row):
    #    new_row[0] = - new_row[0]

    for idx in range(1, len(row)):
        if abs(row[idx]) == abs(row[idx - 1]):
            new_row[idx] = - abs(new_row[idx])

    return new_row

def update_omega(omega):
    return [update_row(row) for row in omega]


def comb_new(omega_in):
    size = len(omega_in)
    omega = [[x for x in row] for row in omega_in]

    logging.debug('comb start')
    logging.debug(str(omega))


    for k in range(size-1):
        logging.debug('\tcomb row %s', k)
#        print('\t\t\tT[k][0..k]=', [omega[k][j] for j in range(k+1)] )

        for i in reversed(range(k+1)):
            logging.debug('\tseparate %s %s', i, k)
            omega = separate(omega,i,size-k-1)
            logging.debug('\t\t %s', omega)

    logging.debug('comb returning')
    logging.debug(str(omega))
    logging.debug('++++++++++++++++++++++++')

    return update_omega(omega)



###########
###########
###########

def get_column_sums(triangle):
    sums = [abs(x) for x in triangle[0]]

    for i in range(1, len(triangle)):
        for j in range(len(triangle[i])):
            sums[j] = sums[j] + abs(triangle[i][j])

    return sums


# 3 2 1
# 2 1
# 1
def tip_west(triangle):
    size =  len(triangle)
    tip_triangle = util.get_all_zero_triangle(size)
    tip_triangle = []

    for row_idx in range(size):
        tip_row = []
        for col_idx in range(size - row_idx):
            count = 0
            for i in range(size - row_idx - col_idx):
                if triangle[row_idx][i] > col_idx:
                    count += 1
            tip_row.append(count)
        tip_triangle.append(tip_row)

    return tip_triangle




def test(size):
    combed_map = dict()
    count_error_map = dict()
    comb_error_list = []
    intersect_list = []

    bt_list = build_bt(size)
    uncombed_omega_list = comb.get_uncombed_triangles(size)
    combed_omega_list = comb.get_combed_triangles(size)

    combed_omega_list = [update_omega(omega) for omega in combed_omega_list]

    #for z in combed_omega_list:
    #    if z[0] == [-4,-4,-4,-3]:
    #        util.print_array(z)

    for t in bt_list:
        logging.debug('==========================')
        logging.debug('BALLOT TRIANGLE')
        logging.debug(str(t))
        outB, outD = to_BD(t)

        #util.print_array(outB)
        #util.print_array(outD)


        omega = comb.get_omega(outB, outD)

        logging.debug('check omega %s', omega)


        #comb_B, comb_D = comb_BD(outB, outD)
        #comb_omega = comb.get_omega(comb_B, comb_D)
        comb_omega = comb_new(omega)

        logging.debug('combed to %s', comb_omega)

        before_col_sums = get_column_sums(omega)
        after_col_sums = get_column_sums(comb_omega)

        logging.debug('\tbefore sums %s', before_col_sums)
        logging.debug('\tafter sums %s', after_col_sums)

        if not before_col_sums == after_col_sums:
            count_error_map[str(omega)] = str(comb_omega)

        key = str(comb_omega)

        if key in combed_map:
            print('ERROR!', str(omega), combed_map[key], 'both map to', key)
        else:
            print('start', omega, 'end', comb_omega)
            combed_map[key] = omega

        if omega in uncombed_omega_list:
            intersect_list.append(omega)
            idx = uncombed_omega_list.index(omega)
            if not comb_omega == combed_omega_list[idx]:
                comb_error_list.append([str(omega), str(combed_omega_list[idx]), str(comb_omega)])

    #util.print_array()

    print('errors:', str(len(bt_list) - len(combed_map)))

    print('>>>>>>> missing combed triangles:')
    for combed in combed_omega_list:
        if str(combed) not in combed_map:
            print(combed)

    print('>>>>>>> failed BT combing:')

    combed_omega_str_list = [str(x) for x in combed_omega_list]

    for bt_combed in combed_map:
        if str(bt_combed) not in combed_omega_str_list:
            print(bt_combed)


    print('>>>>>> failed column sums')

    for x in count_error_map:
        print(x)
        print(count_error_map[x])
        print('-------')
    print('num col sum errors', len(count_error_map))


    print('>>>> combing errors compared to standard combing')
    print('total intersection', len(intersect_list), 'error count', len(comb_error_list))

    for x in comb_error_list:
        print(x)
    # print('###########################')

    # print('intersection')
    # for t in intersect_list:
    #     util.print_array(t)
    #
    # print('intersection  combed')
    # for t in intersect_list:
    #     util.print_array(comb_new(t))

if __name__ == '__main__':




    #for bt in bt_list:
    #    print(to_tikz(bt))
    #print(len(bt_list))


    #get_block_totals()


    #t = [[3,0,0,0],[2,1,0],[1,0],[0]]

    #print(to_tangle(t))

    #t = bt_list[100]
    #t = [[2,1,1,1],[1,0,0],[0,0],[0]]

    #bt_list = [[[2, 0], [1]]] #, [[1, 0], [1]]]












    #
    # tri = [[0,0],[0]]
    # tri = [[2, 0], [1]]
    # #tri = [[1, 0], [1]]
    # util.print_array(tri)
    #
    # size = len(tri)
    #
    # tiered = [[x+ idx for x in row] for idx, row in enumerate(tri)]
    # util.print_array(tiered)
    #
    # pt2 = [[size - x for x  in reversed(row)]  for row in tiered]
    #
    # util.print_array(pt2)
    #
    # path_triangle = [[size - x - idx for x in reversed(row)] for idx, row in enumerate(tri)]
    #
    # path_triangle = [x for x in reversed(path_triangle)]
    #
    # pt = []
    #
    # # for idx in range(len(tri)):
    # #     row = []
    # #     for x in reversed(tri[idx]):
    # #         row.append(size - x )
    # #
    # #     pt.append(row)
    #
    # util.print_array(path_triangle)
    # util.print_array(pt)

    print('!!!!!!!!!!!!!!!!!!!!!!!!!!')
    # print('>>>> BEFORE')
    # # myB = [[1], [0, 1]]
    # # myD = [[0], [1, 0]]
    #
    # # starting from the top
    # myB = [[1], [0, 1], [1, 0, 0]]
    # myD = [[0], [1, 0], [0, 0, 2]]
    #
    # # midway
    # myB = [[1], [0, 1], [1, 0, 0]]
    # myD = [[0], [1, 0], [0, 0, 2]]
    # print(myB)
    # print(myD)
    # print(comb.get_omega(myB,myD))
    #
    # myB, myD = untangle(myB, myD, 1, 1)
    # #myB, myD = comb_BD(myB,myD)
    #
    # print('>>>> AFTER')
    # print(myB)
    # print(myD)
    # print(comb.get_omega(myB,myD))


    # big_row = [3,2,1,0]
    # small_row = [3,3,3]
    # print(big_row,small_row)
    # print(separate(big_row,small_row,2))

    #omega = [[1,0],[1]]

    ########

    # size = 5
    # bt_list = build_bt(size)
    # uncombed_omega_list = comb.get_uncombed_triangles(size)
    # combed_omega_list = comb.get_combed_triangles(size)
    #
    # success_count = 0
    #
    # for idx in range(len(uncombed_omega_list)):
    #     omega = uncombed_omega_list[idx]
    #     combed_omega = comb_new(omega)
    #
    #     #print('---------')
    #     #print(omega)
    #     #print(combed_omega)
    #
    #     if not str(combed_omega) == str(combed_omega_list[idx]):
    #         print('FAILURE!', combed_omega, combed_omega_list[idx])
    #     else:
    #         success_count = success_count + 1
    #
    # print(success_count)



    ######


    #logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


    test(2)

    # t = [[-3, 2, -2], [-2, -2], [-1]]
    # t = [[2, 1, 0], [-2, -2], [-1]]
    # t = [[2, -2, -2], [-2, 0], [0]]
    #t = [[-3, -3, -3], [-2, 0], [0]]
    # t = [[2, -2, 1], [-2, 1], [-1]]
    #t = [[3, -3, 2, 0], [-3, 2, 0], [1, 0], [0]]
    t = [[4,2,-2,-2],[2,-2,1],[2,-2],[1]]
    t = [[-4, -4, -3, -3], [-3, -3, 1], [-2, 0], [0]]
    out = comb_new(t)

    logging.info('before')
    logging.info(t)
    logging.info(get_column_sums(t))
    logging.info('after')
    logging.info(out)
    logging.info(get_column_sums(out))



    size = 3

    bt_list = build_bt(size)

    col_set = set()

    for bt in bt_list:
        util.print_array(bt)
        tip_bt = tip_west(bt)
        print('tipped')
        util.print_array(tip_bt)
        #col_set.add(str([tip_bt[i][0] for i in range(size)]))
        print('=============')

    for c in col_set:
        print(c)

    print(len(col_set))

    util.print_block_totals(bt_list)


    my_tri_lists = [ build_bt(2), build_bt(3), build_bt(4)]
    my_totals = [ util.print_block_totals(x) for x in my_tri_lists]
    print('block totals=',my_totals)




