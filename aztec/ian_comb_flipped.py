import triangle.build_ballot_triangle as bbt
import triangle.build_tss as btss
import triangle.array_util as util

import mysql.connector

import ast




def get_diag_sums(triangle):
    diags = []

    for i in range(len(triangle)):
        val = 0
        for j in range(i + 1):
            val += triangle[j][i - j]
        diags.append(val)

    return tuple(diags)

def get_list_from_db(query):
    conn = mysql.connector.connect(host='localhost', database='mysql', user='root', password='50Fl**rs')
    cur = conn.cursor(buffered=True)

    cur.execute(query)
    records = cur.fetchall()

    tri_list  = [ ast.literal_eval(r[0]) for r in records]

    cur.close()
    conn.close()

    return tri_list



def comb(tss, debug=False):
    size = len(tss)

    triangle = util.clone_array(tss)

    if debug:
        prev = util.clone_array(tss)
        print("COMBING")
        util.print_array(triangle)

    for i in reversed(range(1,size)):
        print('dealing with row ', i)
        for j in range(i,size):
            print('\thandling row ', j)
            triangle = handle_row_swap(triangle, j)

            if debug and not prev == triangle:
                print('>>>>> i,j', i, j)
                util.print_array(triangle)
                prev = util.clone_array(triangle)

    # for i in range(1,size):
    #         handle_row_swap(triangle, i)
    #
    #         if debug and not prev == triangle:
    #             print('>>>>> i', i)
    #             util.print_array(triangle)
    #             prev = util.clone_array(triangle)
    #


    return triangle






# comb from fbt to tss
def handle_row_with_col_max(triangle, row_idx, col_idx):
    row = triangle[row_idx]
    size = len(row)

    #print('handling row,col', row_idx, col_idx)

    if row[col_idx] < row[col_idx+1]:
        # excess amount
        diff = row[col_idx+1] - row[col_idx]
        temp_row = [x for x in row]
        next_row = triangle[row_idx+1]

        for k in range(col_idx+1, size):
            row[k] = next_row[k-1]
            next_row[k-1] = temp_row[k]

        # if row[col_idx] - row[col_idx+1] > 1:
        #     delta = row[col_idx] - row[col_idx+1] - 1
        #     cut_off = next_row[0] -  delta
        #     for k in range(size-1):
        #         if next_row[k] > cut_off:
        #             row[k+1] = row[k+1]  + next_row[k]  -  cut_off
        #             next_row[k] =  cut_off

        # if row[col_idx] - row[col_idx+1] > 1:
        #     for k in range(col_idx, size-1):
        #         change = max(0, next_row[k] - row[col_idx])
        #         row[k+1] = row[k+1]  + change
        #         next_row[k] =  next_row[k] - change

        if row[col_idx] - row[col_idx + 1] > 1:
            # if 1 above, then decrease by 1
            # if 2 above, then make equal
            if diff == 1:
                delta = row[col_idx] - 1
            else:
                delta = row[col_idx]

            floor = next_row[col_idx] - delta


            # delta = row[col_idx] - row[col_idx+1] - 1
            for k in range(col_idx, size - 1):
                change = max(0, next_row[k] - floor - row[k+1])
                row[k + 1] = row[k + 1] + change
                next_row[k] = next_row[k] - change


    return triangle



def comb_with_col_max(tss, debug=False):
    size = len(tss)

    triangle = util.clone_array(tss)

    if debug:
        prev = util.clone_array(tss)
        print("COMBING with col max")
        util.print_array(triangle)

    for col_idx in reversed(range(0,size-1)):
        if debug:
            print('dealing with col_max ', col_idx)
        for j in reversed(range(0,size - col_idx-1)):
            if debug:
                print('\thandling row ', j)
            triangle = handle_row_with_col_max(triangle, j, col_idx)

            if debug and not prev == triangle:
                print('>>>>> col_max,j', col_idx, j)
                util.print_array(triangle)
                prev = util.clone_array(triangle)

    # for i in range(1,size):
    #         handle_row_swap(triangle, i)
    #
    #         if debug and not prev == triangle:
    #             print('>>>>> i', i)
    #             util.print_array(triangle)
    #             prev = util.clone_array(triangle)
    #

    # # final time needed?
    # if debug:
    #     print('one more time')
    # for j in reversed(range(0,size-1)):
    #     if debug:
    #         print('\thandling row ', j)
    #     triangle = handle_row_with_col_max(triangle, j, col_max)
    #
    #     if debug and not prev == triangle:
    #         print('>>>>> col_max,j', col_max, j)
    #         util.print_array(triangle)
    #         prev = util.clone_array(triangle)

    return triangle






combed_map = dict()

##############
def compare(size):

    # rows decr by at most 1
    tss_list = btss.build_tss(size)

    # row weak decr
    # col weak incr or decr by 1
    bt_list = bbt.build_bt(size)

    fbt_list = [ util.flip_triangle2(b) for b in bt_list]

    combed_list = []
    combed_str_set = set()

    fail_list = []

    print('total', len(tss_list))

    #tss_list = tss_list[0:1000]

    print('========= FBT')
    for count,fbt in enumerate(fbt_list):

        if count % 1000 == 0:
            print(count)
        #print('handling TSS')
        #util.print_array(tss)
        #tri = comb(tss, True)
        tri = comb_with_col_max(fbt, False)

        if not get_diag_sums(fbt) == get_diag_sums(tri):
            print('*******ERRROR diag sum', fbt, tri)


        #tri = comb(tri)
        #tri = comb(tri)
        combed_list.append(tri)
        combed_str_set.add(str(tri))
        #util.print_array(tri)
        #print('=================')
        if not tri in tss_list:
            fail_list.append([fbt, tri])
            print('fail', count, fbt, '\t', tri)

        combed_key = str(tri)
        if not combed_key in combed_map:
            combed_map[combed_key] = [fbt,]
        else:
            combed_map[combed_key].append(fbt)


    missing_list = []
    # # print('========= BT')
    for tss in tss_list:
        if not tss in combed_list:
            missing_list.append(tss)
    # #     util.print_array(bt)


    fail_file = open('/Users/abeverid/PycharmProjects/asm/data/tss/flip_fail_bt.txt', 'w')


    for f in fail_list:
        util.print_array(f[0])
        util.print_array(f[1])
        fail_file.write(str(f[0]) + ' fails to' + str(f[1]))
        fail_file.write('\n')
        print('************')
    print('num failures', len(fail_list))

    fail_file.close()

    # t = [[2, 2, 1], [0, 0], [0]]
    #
    # util.print_array(t)
    # util.print_array(comb(t))
    #
    print('MISSING')

    missing_file = open('/Users/abeverid/PycharmProjects/asm/data/tss/flip_missing_tss.txt', 'w')
    for b in missing_list:
        missing_file.write(str(b))
        missing_file.write('\n')
    missing_file.close()
    #   util.print_array(b)
    print('num missing:', len(missing_list))


    print('combed tri size', len(combed_list))
    print('combed str size', len(combed_str_set))



    bad_list = [ x[0] for  x in fail_list]

    print(bad_list)

    print('repeats!!!!')
    rep_count = 0

    repeat_tss_file = open('/Users/abeverid/PycharmProjects/asm/data/tss/flip_repeat_tss.txt', 'w')
    repeat_bt_file = open('/Users/abeverid/PycharmProjects/asm/data/tss/flip_repeat_bt.txt', 'w')

    for key in combed_map:
        if len(combed_map[key]) > 1:
            print(key, len(combed_map[key]), combed_map[key])
            rep_count +=1

            key_tri = ast.literal_eval(key)
            key_diags = get_diag_sums(key_tri)

            repeat_tss_file.write(key)
            repeat_tss_file.write('\n')
            rep_list = combed_map[key]
            for rep in rep_list:
                repeat_bt_file.write(str(rep))
                repeat_bt_file.write('\n')

                rep_diags  = get_diag_sums(rep)

                if not key_diags == rep_diags:
                    print('MEGA ERROR!!!!!!!!', key_diags, rep_diags)



    repeat_tss_file.close()
    repeat_bt_file.close()

    print('repcount', rep_count)





def sort_missing_repeats():
    missing_bt_file = open('/Users/abeverid/PycharmProjects/asm/data/tss/flip_missing_tss.txt', 'r')
    missing_bt_list = []
    for line in missing_bt_file.readlines():
        line = line.strip()
        missing_bt_list.append(ast.literal_eval(line))

    repeat_tss_file = open('/Users/abeverid/PycharmProjects/asm/data/tss/flip_repeat_tss.txt', 'r')
    repeat_tss_list = []
    for line in repeat_tss_file.readlines():
        line = line.strip()
        repeat_tss_list.append(ast.literal_eval(line))


    repeat_bt_file = open('/Users/abeverid/PycharmProjects/asm/data/tss/flip_repeat_bt.txt', 'r')
    repeat_bt_list = []
    for line in repeat_bt_file.readlines():
        line = line.strip()
        repeat_bt_list.append(ast.literal_eval(line))

    for repeat in repeat_bt_list:
        util.print_array(repeat)


    missing_bt_map = dict()
    for missing in missing_bt_list:
        key = get_diag_sums(missing)

        if not key in missing_bt_map:
            missing_bt_map[key] = [ missing,]
        else:
            missing_bt_map[key].append(missing)

    repeat_bt_map = dict()
    for rep in repeat_bt_list:
        key = get_diag_sums(rep)

        if not key in repeat_bt_map:
            repeat_bt_map[key] = [rep, ]
        else:
            repeat_bt_map[key].append(rep)

    repeat_tss_map = dict()
    for rep in repeat_tss_list:
        key = get_diag_sums(rep)

        if not key in repeat_tss_map:
            repeat_tss_map[key] = [rep, ]
        else:
            repeat_tss_map[key].append(rep)

    print('************************************')
    for key in missing_bt_map:
        print(key)

        print('\tmissing tss')
        miss_list = missing_bt_map[key]
        for m in miss_list:
            print('\t\t',  m)

        print('\trepeated tss')
        rep_list = repeat_tss_map[key]
        for m in rep_list:
            print('\t\t',  m)

        print('\tballots that clash')
        rep_list = repeat_bt_map[key]
        for m in rep_list:
            print('\t\t',  m)



def check_diagonal_sum(diag_sum):
    q_tss = 'SELECT name FROM FIVE_TSS WHERE diag1=%s and diag2=%s and diag3=%s and diag4=%s and diag5=%s' % diag_sum
    q_bt = 'SELECT name FROM FIVE_BT WHERE diag1=%s and diag2=%s and diag3=%s and diag4=%s and diag5=%s' % diag_sum

    tss_list = get_list_from_db(q_tss)
    bt_list = get_list_from_db(q_bt)
    fbt_list = [ util.flip_triangle2(b) for b in bt_list]
    combed_list = []

    print('combing FBT')
    for t in fbt_list:
        combed = comb_with_col_max(t, False)
        if not combed in tss_list:
            print('>>>>>>>>>FAIL!')
            util.print_array(t)
            util.print_array(combed)
            print('fail:', t, combed)
        elif combed in combed_list:
            print('>>>>>>>>> REPEAT!')
            util.print_array(t)
            util.print_array(combed)
        else:
            combed_list.append(combed)
            print('>>>passed!')
            util.print_array(t)
            util.print_array(combed)

    print('*********************  missing TSS')
    for t in tss_list:
        if not t in combed_list:
            util.print_array(t)


# x = bad5_list[0]
# util.print_array(x)
# util.print_array(comb(x, True))


# tss_list = btss.build_tss(5)
# bt_list = bbt.build_bt(5)
#
# tss_list = [ tss for tss in tss_list if get_diag_sums(tss) == [2, 4, 3, 2, 1]]
# bt_list = [ bt for bt in bt_list if get_diag_sums(bt) == [2, 4, 3, 2, 1]]
#
# comb_list = [comb(tss) for tss in tss_list]
#
# for bt in bt_list:
#     if not bt in comb_list:
#         util.print_array(bt)


def count_layer():
    size = 5
    tss_list = btss.build_tss(size)

    top_counts = [0] * (size+1)

    block_counts = [0] * (size+1)

    for tss in tss_list:
        count = get_diag_sums(tss)
        top_counts[count[0]] += 1
        block_counts[count[-1]] += 1

    print('top', top_counts)
    print('bot', block_counts)



def get_layer_triangle(triangle):
    size = len(triangle)

    layer_tri = [ [0] * (k+1) for k in range(size)]


# x
# xx
# xxx

    for i in range(size):
        #print('handling i', i)
        for j in range(i+1):
            layer_tri[i][j] = sum ([ 1  for k  in range(j+1) if triangle[k][j-k] >=  size-i])


    tri = [[x for x in reversed(row)] for row in reversed(layer_tri)]

    return tri





#util.print_array(bad5_list[0])

#util.print_array(comb(bad5_list[0], True))


bt_list = bbt.build_bt(5)
fbt_list = [ util.flip_triangle2(b) for b in bt_list]


t1 = [[2, 3, 3, 2, 1], [1, 3, 2, 1], [0, 2, 1], [0, 1], [0]]
t2 = [[2, 4, 3, 2, 1], [0, 3, 2, 1], [0, 2, 1], [0, 1], [0]]
t3 = [[1, 2, 3, 2, 1], [0, 0, 0, 0], [0, 0, 0], [0, 0], [0]]


t5_29162 = fbt_list[29162]
t5_19075 = fbt_list[19075]
t5_19076 = fbt_list[19076]

t5a = [[[2, 1, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [0, 0], [0]], [[2, 3, 3, 2, 1], [0, 0, 0, 0], [0, 0, 0], [0, 0], [0]]]

t5b = [[2, 1, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [0, 0], [0]]
t5c = [[2, 3, 3, 2, 1], [0, 0, 0, 0], [0, 0, 0], [0, 0], [0]]

t5d1 = [[2, 1, 1, 0, 0], [2, 2, 2, 1], [1, 0, 0], [0, 0], [0]]
t5d2 = [[2, 1, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [0, 0], [0]]
t5d3 = [[2, 1, 3, 2, 1], [2, 1, 0, 0], [0, 0, 0], [0, 0], [0]]

triangle = t5d3

#triangle = [[3, 3, 2, 1], [2, 1, 0], [0, 0], [0]]


util.print_array(triangle)
#
#
triangle = comb_with_col_max(triangle, True)
#
#
util.print_array(triangle)

# this "diagonal sum" seemed like a good idea.
# but it only gets a subset of the ballot triangles
# is there a way to match them up afterwards?
def test_layer_triangle(size):
    tss_list = btss.build_tss(size)

    bt_list  = bbt.build_bt(size)

    after_map = dict()

    error_count = 0
    for t in tss_list:
        tlayer = get_layer_triangle(t)
        s = util.flip_triangle2(tlayer)
        #print(t, s)
        print('before')
        util.print_array(t)
        print('after')
        util.print_array(s)
        key =  str(s)
        if not key in after_map:
            after_map[key] = [ t,]
        else:
            after_map[key].append(t)

        # if not s in bt_list:
        #     error_count+=1
        #     print('start tss')
        #     print(t)
        #     print('after')
        #     util.print_array(s)

    #print('errors', error_count)

    print('tss size', len(tss_list))
    print('after size', len(after_map))

    rep_count = 0
    for key in after_map:
        key_list = after_map[key]
        if len(key_list) > 1:
            rep_count += 1
            print('repeated', key)
            print('AFTER')
            util.print_array(ast.literal_eval(key))
            print('BEFORE')
            for x in key_list:
                util.print_array(x)


    print('>>>>>>>>>>>>>>>>missing')
    missing_count = 0
    for b in  bt_list:
        if not str(b) in after_map:
            print('missing', b)
            util.print_array(b)
            missing_count += 1


    print('before', len(tss_list))
    print('after', len(after_map))
    print('repeated', rep_count)
    print('missing', missing_count)


#test_layer_triangle(2)

#compare(5)

#sort_missing_repeats()

check_diagonal_sum((2,3,3,2,1))

#count_layer()


### A NEW IDEA: use rows of TSS as columns of BT since they already
### decrease by at most 1.
### now we need columns weakly decreasing.


#   t = [[2, 3, 2, 1], [0, 1, 0], [0, 0], [0]]

#comb_with_col_max(t,True)

# t = [[4,4,3,2,2,2,1], [2,2,2,2,2]]
#
# tflip = util.flip_triangle2(t)
#
# util.print_array(t)
# util.print_array(tflip)



# bt_counts = [0] * 6
#
# bt_list = bbt.build_bt(5)
#
#
# for b in bt_list:
#     b = util.flip_triangle2(b)
#     bt_counts[b[0][0]] += 1
#
#
# tss_counts = [0] * 6
#
# tss_list = btss.build_tss(5)
#
#
# for t in tss_list:
#     tss_counts[t[0][0]] += 1
#
#
# print('bt ', bt_counts)
# print('tss', tss_counts)



### IDEA: MAYBE PROCESS DIAGONALLY