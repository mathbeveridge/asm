import triangle.triangle_util as util
import aztec.binary_comb as comb


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
    #    tex_list.append('\\node at (' + str(-size) + ',' + str(size/2) +') {' + to_ytableau(tri_before) + '};')
    tex_list.append('\\node at (' + str(-size) + ',' + str(1 / 2 * size) + ') {\scriptsize ' + util.to_ytableau(
        triangle) + '};')

    tex_list.append(to_tangle(triangle))
    tex_list.append('\\end{scope}')

    tex_list.append('\\end{tikzpicture}')
    tex_list.append('\\qquad')
    #tex_list.append('\\bigskip')

    return '\n'.join(tex_list)


def get_down_for_ballot(triangle):
        size = len(B)
        D = get_all_zero(size)
        for k in range(size):
            # print('B[k]', k, B[k])
            D[k][k] = k + 1 - sum([B[k][j] for j in range(k + 1)])
        return D


def to_BD(triangle):
    size = len(triangle)
    B = util.get_all_zero(size)
    D = util.get_all_zero(size)



    tiered = [[x+ idx for x in row] for idx, row in enumerate(triangle)]

    path_triangle = [[size - x for x  in reversed(row)]  for row in reversed(tiered)]

    util.print_triangle(path_triangle)

    #tiered = [ [size -  x - idx for  x in row] for idx,row in enumerate(triangle)]

    #path_triangle = [[x for x in reversed(row)] for row in reversed(tiered)]

    #path_triangle = [ [size - x - idx  for x in reversed(row)] for idx,row in enumerate(triangle)]

    #path_triangle = [x for x in reversed(path_triangle)]

    print('ballot')
    util.print_triangle(triangle)
    print('path triangle')
    util.print_triangle(path_triangle)

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

    print('binary')
    util.print_triangle(B)
    print('down')
    util.print_triangle(D)

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



if __name__ == '__main__':


    combed_map = dict()

    bt_list = build_bt(2)
    #for bt in bt_list:
    #    print(to_tikz(bt))
    #print(len(bt_list))


    #get_block_totals()


    #t = [[3,0,0,0],[2,1,0],[1,0],[0]]

    #print(to_tangle(t))

    #t = bt_list[100]
    #t = [[2,1,1,1],[1,0,0],[0,0],[0]]
    for t in bt_list:
        print('==========================')
        util.print_triangle(t)
        outB, outD = to_BD(t)

        #util.print_triangle(outB)
        #util.print_triangle(outD)


        omega = comb.get_omega(outB, outD)

        print('check omega')
        util.print_triangle(omega)

        comb_B, comb_D = comb.comb_BD(outB, outD)
        comb_omega = comb.get_omega(comb_B, comb_D)

        print('combed to')
        util.print_triangle(comb_omega)

        key = str(comb_omega)

        if key in combed_map:
            print('ERROR!', str(t), combed_map[key])
        else:
            combed_map[key] = t

    #util.print_triangle()

    print('errors:', str(len(bt_list) - len(combed_map)))


    print('###########################')

    tri = [[0,0],[0]]
    tri = [[2, 0], [1]]
    #tri = [[1, 0], [1]]
    util.print_triangle(tri)

    size = len(tri)

    tiered = [[x+ idx for x in row] for idx, row in enumerate(tri)]
    util.print_triangle(tiered)

    pt2 = [[size - x for x  in reversed(row)]  for row in tiered]

    util.print_triangle(pt2)

    path_triangle = [[size - x - idx for x in reversed(row)] for idx, row in enumerate(tri)]

    path_triangle = [x for x in reversed(path_triangle)]

    pt = []

    # for idx in range(len(tri)):
    #     row = []
    #     for x in reversed(tri[idx]):
    #         row.append(size - x )
    #
    #     pt.append(row)

    util.print_triangle(path_triangle)
    util.print_triangle(pt)
