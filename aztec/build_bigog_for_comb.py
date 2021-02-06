import aztec.build_bigog as build_bigog
import triangle.array_util  as util
import aztec.binary_comb  as binary_comb
import aztec.general_comb as gen_comb

cb_dict = dict()
cb_dict[1] = [[[k, ],] for k in range(0,2)]


def get_bigog_triangles(size):
    bigog_list = get_bigog_for_comb(size)
    return [bigog_to_omega(b) for b in bigog_list ]

def get_bigog_for_comb(size):
    if not size in cb_dict:
        bigog_list = build_bigog.get_bigog(size)

        cb_list = [to_bigog_for_comb(t) for t in bigog_list]
        cb_dict[size] = cb_list

    return cb_dict[size]

def to_bigog_for_comb(bigog):

   # print(bigog)

    triangle = [[x for x in reversed(row)] for row in bigog]
    #triangle = util.flip_triangle2(triangle)

    #util.print_array(triangle)

    return(bigog)


def bigog_to_omega(bigog):
    B, D = to_BD(bigog)
    return binary_comb.get_omega(B,D)

def to_BD(cb):
    #print('to_BD', cb)
    size = len(cb)
    B = []
    D = []

    for k,row in enumerate(cb):
        drop = 0
        brow = [0] * (size - k)
        drow = [0] * (size - k)

        if len(row) == 1 and row[0] == 0:
            brow[0] = 0
            drow[0] = 1

        else:
            prev_idx = 0

            for idx in range(0,size+1):
                if idx in row:
                    # update drop matrix
                    count = row.count(idx)

                    if idx == 0:
                        drow[idx] = count
                    elif count > 1:
                        drow[idx] = count - 1
                    # update binary matrix
                    if idx > 0:
                        brow[idx-1] = 1

                    if idx == size:
                        count = row.count(size)

                        if count > 1:
                            drow[prev_idx+1] = count -1

                    prev_idx = idx

            # drop = drop+count
        #drow[-1] = len(drow) - drop
        B.insert(0,[b for b in reversed(brow)])
        D.insert(0, [d for d in reversed(drow)])
        #B.append([b for b in reversed(brow)])
        #D.append([d for d in reversed(drow)])
    return B,D



def test_comb():

    size = 3

    combed_list = binary_comb.get_combed_triangles(size)

    bc_list = get_bigog_for_comb(size)

    #bc_list = [ bc_list[18], bc_list[52], bc_list[21], bc_list[53], bc_list[41], bc_list[60] ]

    #bc_list = [  bc_list[41], ]

    print('starting')

    fail_count = 0

    #bc_list = [ [[0, 2, 3], [0, 2], [0]]]

    bc_mapping = dict()
    double_count  = 0

    bigog_omega_list = []
    bigog_omega_after_list = []

    for count, bc in enumerate(bc_list):
        B, D = to_BD(bc)

        #B, D = binary_comb.comb_BD(B,D)

        print('>>>>>>>>>>>>>>><<<<<<<<<<<<<<<')
        util.print_array(bc)
        util.print_array(B)
        util.print_array(D)
        util.print_array(binary_comb.get_omega(B,D))


        # print('>>>>>>>>>>>>>>><<<<<<<<<<<<<<<')
        # print('>>>>>>>>>>>>>>><<<<<<<<<<<<<<<')
        # print('>>>>>>>>>>>>>>><<<<<<<<<<<<<<<')

        print('>>>>>>> combing',count, bc, B, D)
        print('\t', binary_comb.get_omega(B,D))

        bigog_omega_list.append(binary_comb.get_omega(B, D))

        BB, DD = gen_comb.comb_BD(B,D)
        combed = binary_comb.get_omega(BB,DD)

        bigog_omega_after_list.append(combed)



        print('\t\t\t', combed)

        combed_str = str(combed)

        before = binary_comb.get_omega(B, D)

        #print(combed)
        if not combed in combed_list:
            util.print_array(bc)
            util.print_array(B)
            util.print_array(D)
            print('before')
            util.print_array(before)
            print('fail')
            util.print_array(combed)
            fail_count +=1
        elif not combed_str in bc_mapping:
            bc_mapping[combed_str] = [ before, ]
        else:
            bc_mapping[combed_str].append(before)
            print('error double map:', combed_str, 'is mapped to by', bc_mapping[combed_str])
            print('\tcount=', count)
            double_count += 1
        #
        #print('-------')
        # else:
        #     print('pass')
        #     util.print_array(combed)


    # print('BINARY COMBED LIST')
    # for x in combed_list:
    #     print(x)


    before_file_name = '/Users/abeverid/PycharmProjects/asm/data/bigog/bigog' + str(size) + '.tex'
    after_file_name = '/Users/abeverid/PycharmProjects/asm/data/bigog/bigog' + str(size) + '-after.tex'
    util.omega_list_to_tex_file(bigog_omega_list, before_file_name)
    util.omega_list_to_tex_file(bigog_omega_after_list, after_file_name)

    print(len(combed_list))
    print('fail count', fail_count)

    print('doubles', double_count)

def test_swap(size):
    binary_list = binary_comb.get_uncombed_triangles(size)
    bigog_list = get_bigog_triangles(size)

    binary_only_list = [ b for b in binary_list if b not in bigog_list]
    bigog_only_list = [ b for b in bigog_list if b not in binary_list]

    print('>>>>>>>>>>>binary only', len(binary_only_list))
    for b in binary_only_list:
        print(b)
    print('>>>>>>>>>>>bigog only', len(bigog_only_list))
    for b in bigog_only_list:
        print(b)


test_swap(2)


