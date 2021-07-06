import aztec.binary_comb as binary_comb
import aztec.build_ssyt as build_ssyt
import triangle.array_util as util



def get_sign(val):
    if val < 0:
        return -1
    else:
        return 1


def handle_rows(big_row_in, small_row_in, max_idx):
    big_row = [ x for x  in  big_row_in]
    small_row = [x for x  in small_row_in]

    hit_small_zero = False

    # this isn't the right place to assess since rows change a lot
    #possible_v_list = possible_v_idx_list(big_row_in,small_row_in)

    current_diff = 1
    delta = 0
    for idx in range(max_idx):
        big_abs_val = abs(big_row_in[idx])
        small_abs_val = abs(small_row_in[idx])
        big_sign  = get_sign(big_row_in[idx])
        small_sign = get_sign(small_row_in[idx])
        diff =  big_abs_val - small_abs_val
        if diff < current_diff:
            current_diff = diff
            # small took a down step while big took a flat step
            delta = delta + 1
            # can we absorb this new down in a previous vert?
            # only one new step to absorb.
            #
            vert_idx = get_vert_idx(big_row, idx)
            if vert_idx  > -1:
                if delta > 1:
                    print('WARNING: ASSUMES DELTA=1. SHOULD BE OKAY for delta', delta)
                for k in range(vert_idx, idx):
                    temp_val = abs(big_row[k])
                    temp_sign = get_sign(big_row[k])
                    big_row[k] = temp_sign * (temp_val + 1)
                big_row[idx] = big_abs_val + delta
                small_row[idx] = small_abs_val - delta  # diag step
            else:
                big_row[idx] = -(big_abs_val + delta) # flat step
                small_row[idx] = small_abs_val - delta # diag step
            if small_abs_val < delta:
                print('BIG PROBLEM: GOING NEGATIVE small', small_abs_val, 'delta', delta)
        else:
            if small_abs_val > 0 :
                big_row[idx] = big_sign * (big_abs_val + delta)
                small_row[idx] = small_sign * (small_abs_val - delta)
                if small_abs_val < delta:
                    print('BIG PROBLEM: GOING NEGATIVE small', small_abs_val, 'delta', delta)
            elif not hit_small_zero:
                # Need to create a V in the big row??????
                # no op for now. still thinking
                hit_small_zero = True

        # WILL THIS WORK FOR CREATING A V? 11:15


    # Need to create a V in the big row??????

    if not big_row_in == big_row and not created_new_v(big_row_in, big_row):
        print('must create a new v for big row', big_row, 'small row', small_row)
        possible_v_list = possible_v_idx_list_after(big_row,small_row)

        if len(possible_v_list) == 0:
            print('\tBIG PROBLEM: no way to create a v')
        else:
            print('possible v index list', possible_v_list)

    #    big_row[max_idx] = - big_row[max_idx]

    #THIS WORKED FOR n=4
    if big_row[max_idx] > 0 and delta > 0:
        if not big_row[max_idx-1] == big_row_in[max_idx-1]:
            print('PROBLEMATIC? MUST CREATE A V?')
            big_row[max_idx] = - big_row[max_idx]



    return big_row, small_row

def created_new_v(old_big_row, new_big_row):
    in_count = count_v(old_big_row)
    new_count = count_v(new_big_row)

    return new_count > in_count


def count_v(row):
    v_count = 0
    for k in range(len(row)-1):
        if row[k+1] < 0  and abs(row[k]) > abs(row[k+1]):
            v_count += 1

    return v_count


# look at original rows given and identify possible v locations
def possible_v_idx_list(big_row_in,small_row_in):
    v_list = []
    small_len = len(small_row_in)
    for i in range(small_len-1):
        if abs(big_row_in[i]) == abs(small_row_in[i]):
            if abs(big_row_in[i+1]) > abs(small_row_in[i+1]):
                v_list.append(i)

    if abs(big_row_in[small_len-1]) == abs(small_row_in[small_len-1]):
        v_list.append(small_len-1)

    return v_list

def possible_v_idx_list_after(new_big_row, new_small_row):
    idx_list = []
    for i in range(len(new_small_row)):
        if abs(new_big_row[i]) > abs(new_big_row[i+1]):
            if new_big_row[i+1] > 0 and not abs(new_small_row[i]) == abs(new_big_row[i+1]):
                idx_list.append(i)

    return idx_list



# returns the index with a  vertical step that we can steal from
# 31 March: only take  it if it is RIGHT THERE
# returns -1 if no such index
def get_vert_idx(big_row, current_idx):
    if current_idx > 0 and abs(big_row[current_idx-1]) - 1 > abs(big_row[current_idx]):
        return current_idx
    else:
        return -1

    # THIS SEARCHES FOR PREVIOUS VERTICAL STEPS
    # for idx in reversed(range(0,current_idx)):
    #     if abs(big_row[idx]) - 1 > abs(big_row[idx+1]):
    #         # we can use this vertical step
    #         return idx+1
    # else:
    #     return -1


def comb(triangle_in, debug=False):
    triangle = util.clone_array(triangle_in)

    size = len(triangle)
    for i in range(size-1):
        max_idx = len(triangle[i+1])
        for j in reversed(range(i+1)):
            if debug:
                print('handle', i,j)
            new_big, new_small = handle_rows(triangle[j], triangle[j+1], max_idx)
            triangle[j] = new_big
            triangle[j+1] = new_small
            if debug:
                util.print_array(triangle)

    return triangle



def test_omega(omega, debug=False):
    print('before')
    util.print_array(omega)
    new_omega = comb(omega, debug)
    print('after')
    util.print_array(new_omega)
    return new_omega


combed_map = dict()

def test_size(size):
    bin_comb_omega_list = binary_comb.get_combed_triangles(size-1)

    matrix_list = build_ssyt.get_ssyt_matrix(size)

    vless_comb_list =  []

    vless_comb_str_list = []

    for k, m in enumerate(matrix_list):

        omega = build_ssyt.flip_matrix_to_omega(m)

        print('========= matrix', k)
        util.print_array(m)
        new_omega = test_omega(omega)


        for i in range(size-1):
            new_omega[i][0] = abs(new_omega[i][0])



        if new_omega[0] == [3,-2,-1]:
            print('matched first row')
            print(new_omega)
            print(vless_comb_list)

        if str(new_omega) in vless_comb_str_list:
            '>>>>>>> REPEAT!!!!'
        vless_comb_str_list.append(str(new_omega))

        vless_comb_list.append(new_omega)

        combed_key = str(new_omega)
        if not combed_key in combed_map:
            combed_map[combed_key] = [omega,]
        else:
            combed_map[combed_key].append(omega)


    bad_vless_count = 0


    for new_omega in vless_comb_list:
        for row in new_omega:
            row[0] = abs(row[0])

    for k, new_omega in enumerate(vless_comb_list):
        if not new_omega in bin_comb_omega_list:
            print('bad vless comb', k)
            util.print_array(new_omega)
            bad_vless_count +=1


    bin_count = 0
    for k,omega in enumerate(bin_comb_omega_list):
        if not omega in vless_comb_list:
            print('missing', k)
            util.print_array(omega)
            bin_count += 1

    print('bad count', bad_vless_count)
    print('missing count', bin_count)


    print(len(vless_comb_list))

    temp_set = set()
    for x in vless_comb_list:
        temp_set.add(str(x))

    print(len(vless_comb_list))



    print('repeats!!!!')
    rep_count = 0
    for key in combed_map:
        if len(combed_map[key]) > 1:
            print(key, len(combed_map[key]), combed_map[key])
            rep_count +=1
    print('repcount', rep_count)

    # omega19before = build_ssyt.flip_matrix_to_omega(matrix_list[19])
    # omega19after = comb(omega19before)
    #
    # omega38before = build_ssyt.flip_matrix_to_omega(matrix_list[38])
    # omega38after = comb(omega38before)
    #
    # print('19 is', omega19after)
    # print('38 is', omega38after)
    # print(str(omega19after) == str(omega38after))

test_size(5)


# omega = [[2, -2, -2], [-2, -2], [-1]]
#omega = [[2, -2, 0], [-2, 0], [0]]


# 14 should map to [[-3, -3, -1], [2, 0], [0]]
# 34 should map to [[-3, -3, -1], [1, 0], [0]]

# 18 should map to [[-3, 2, -1], [2, 0], [0]]
# 38 should map to [[-3, 2, -1], [1, 0], [0]]



# we are using the downstep available!!!
#omega = [[-3, 1, -1],[1, -1],[0]]


omega14 = [[2, -2,  1], [-2, 1], [1] ]
omega18 = [[-3,1,-1], [1, -1], [1] ]
omega38 = [[-3,1,-1], [1, -1], [0] ]


omega1 = [[3, -3, 2, 0], [-3, 2, 0], [1, 0], [0]]
omega2 = [[-4, -4, 2, 0], [2, 1, 0], [1, 0], [0]]

omega8 = [[-4, 3, -3, -3], [-3, -3, 2], [-2, -2], [-1]]


#test_omega(omega8, True)

#handle_rows([-3, 2, 1],[-2, -2],2)

#print(handle_rows(omega18[0], omega18[1], 2))