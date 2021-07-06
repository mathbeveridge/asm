import aztec.binary_comb as binary_comb
import triangle.array_util as util

# we comb the binary triangle
# and then decompose into a series of binary triangles, one for each path (with the trivial smaller paths)
# these triangles have a special structure:
#   at most one 1 in each column,
#   the row position weakly decreasing from left to right


def get_down_path(size):
    return [ x for x in reversed(range(size))]



atom_map = dict()

def get_atoms(size):
    if not size in atom_map:

        bin_list = binary_comb.get_binary_triangle(size)

        combed_list = [binary_comb.comb(t) for t in bin_list]

        omega_list = [binary_comb.get_omega(combed[0], combed[1]) for combed in combed_list]

        atoms = dict()

        down_path = get_down_path(size - 1)

        for bin_tri, omega in zip(bin_list, omega_list):
            if size == 1 or omega[1] == down_path:
                atoms[str(omega[0])] = bin_tri

        atom_map[size] = atoms

    return atom_map[size]


def factor(omega):
    factor_list = [get_atoms(len(row))[str(row)] for row in omega]

    return factor_list


def invert(bin_tri):
    new_tri = util.flip_triangle(bin_tri)

    new_tri = [[1-x for x in row] for row in reversed(new_tri)]

    return new_tri


def convert(bin_tri):

    new_tri = invert(bin_tri)

    my_list = []

    for row in new_tri:
        if 1 in row:
            my_list.append(row.index(1) + 1)
        else:
            my_list.append(0)
    return my_list


# changing to counting from the bottom
def convert_v2(bin_tri):

    size = len(bin_tri)

    new_tri = invert(bin_tri)

    my_list = []

    for row in new_tri:
        if 1 in row:
            my_list.append(len(row) - row.index(1) )
        else:
            my_list.append(0)
    return my_list

######
#Alternate Factorization

# returns a binary triangle with monotone decreasing rows
def convert_to_triangle(bin_tri):

    new_tri = util.flip_triangle(bin_tri)

    new_tri = [[1-x for x in row] for row in reversed(new_tri)]

    for row in new_tri:
        for idx in reversed(range(len(row)-1)):
            if row[idx+1] == 1:
                row[idx] = 1

    return new_tri

def sum_triangles(tri_list):
    new_tri = [[x for x in row ] for row in tri_list[0]]

    for idx in range(1, len(tri_list)):
        tri = tri_list[idx]
        for i in range(len(tri)):
            for j in range(len(tri[i])):
                new_tri[i][j] = new_tri[i][j] + tri[i][j]
    return new_tri

######

def check_diag(decomp):
    t = [convert_v2(d) for d in decomp]
    size = len(t)


    print(t)
    for i in range(1, size):
        cur = 0
        for j in range(i+1):
            print('i,j', i, j)
            if (not t[i-j][j] == 0)  and t[i-j][j] < cur:
                print('failing: t[i-j][j] < cur', t[i-j][j], cur )
                return False
            else:
                cur = max(cur, t[i-j][j])
    return True


size = 4

bin_list = binary_comb.get_binary_triangle(size)

combed_list = [binary_comb.comb(t) for t in bin_list]

omega_list = [binary_comb.get_omega(combed[0], combed[1]) for combed in combed_list]

# for omega in omega_list:
#     print('OMEGA DECOMP')
#     util.print_array(omega)
#     decomp = factor(omega)
#     for d in decomp:
#         #util.print_array(convert(d))
#         print('\t column is', convert(d))
#         #B, D = binary_comb.comb(d)
#         #print('\t\t', binary_comb.get_omega(B, D))


#omega_list = [[ [4, -4, 2, 1], [3, 2, 1], [2, 1], [1]],]

count = 0
good_count = 0
fail_diag_count = 0
for omega in omega_list:
    if True: #not binary_comb.is_supported_gog(omega):
        print('#######', count)
        good_count += 1
        decomp = factor(omega)
        if not check_diag(decomp):
            fail_diag_count +=1
            print('DIAGONAL FAIL!')
        for orow, d in zip(omega,decomp):
            #util.print_array(convert(d))
            print("{:<15}".format(str(orow)), "{:<15}".format(str(convert(d))))
            #B, D = binary_comb.comb(d)
            #print('\t\t', binary_comb.get_omega(B, D))
        print('')
    count += 1

print(good_count)
print('fail diag', fail_diag_count)

# for idx,omega in enumerate(omega_list):
#     decomp = factor(omega)
#     print('@@@@@@@@@@@@@', idx)
#     util.print_array(bin_list[idx])
#     util.print_array(omega)
#     for d in decomp:
#         #util.print_array(convert_to_triangle(d))
#         print('\td is', d)
#     print('')
#     util.print_array(bin_list[idx])
#     util.print_array(omega)
#     for d in decomp:
#         util.print_array(convert_to_triangle(d))
#     print('')
#     decomp2 = [convert_to_triangle(d) for d in decomp]
#     print('sum triangles gives:')
#     util.print_array(sum_triangles(decomp2))




#util.print_array(bin_list[62])
#B, D = binary_comb.comb(bin_list[62])
#print('combed to', B, D)
#util.print_array(binary_comb.get_omega(B,D))


# print('!!!!!!!!!!!!!!!!')
# atoms  = get_atoms(3)
#
# for key in [ "[3, 1, 0]", ]:
#     print('key', key)
#     atom = atoms[key]
#     print('\tatom', atom)
#     util.print_array(atom)
#     util.print_array(invert(atom))
#     print('atom is', convert(atom))


#util.print_array(bin_list[548])