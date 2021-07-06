import aztec.binary_comb as binary_comb
import triangle.array_util as util
import triangle.build_binary_triangle as bbt
import stackset.build_stack_set as bss


# there are many
def get_layers_as_permutations(size):
    bin_list = binary_comb.get_binary_triangle(size)
    layer_list = []

    #bin_list = [ bin_list[-1]]

    for b in bin_list:
       layer_list.append(get_permutation_layers_left(b))

    return layer_list


# get first 1 from the left
# the triangle rotation below turns these into "top"
def get_permutation_layers_left(bin_tri):

    triangle = [[x for x in row] for row in reversed(bin_tri)]
    size = len(triangle)

    print('input')
    util.print_array(triangle)

    layers = []

    for i in range(size):
        layer = []
        for j in range(len(triangle) - i):
            row = triangle[j]
            if 1 in row:
                idx = row.index(1)
                layer.append(idx+1)
                row[idx]=0
            else:
                layer.append(0)

        layers.append(layer)

    print('output')
    util.print_array(layers)

    return layers



# get first 1 from the left
# the triangle rotation below turns these into "bottom"
def get_permutation_layers_right(bin_tri):

    triangle = [[x for x in row] for row in reversed(bin_tri)]
    size = len(triangle)

    print('input')
    util.print_array(triangle)

    layers = []

    for i in range(size):
        layer = []
        for j in range(len(triangle)-i):
            row = triangle[j]
            if 1 in row:
                rev_row = row[::-1]
                idx = len(rev_row) - 1 - rev_row.index(1)
                layer.append(idx+1)
                row[idx]=0
            else:
                layer.append(0)

        layers.append(layer)

    print('output')
    util.print_array(layers)

    return layers


# Peel a binary triangle into layers.
# Schroder Family Options:
# (1) peel the top 1 in each column. This makes an awesome family that is still combable.
# (2) peel the bottom 1 in each column
# Either one factors the binary triangle into Schroder paths.


# gets binary layers from top (schroder family) the 1's are "weakly increasing in location"
def get_binary_layers(size):

    bin_list = binary_comb.get_binary_triangle(size)
    layer_list = []

    for b in bin_list:
       layer_list.append(get_layers(b))

    return layer_list

def get_layers(bin_tri):
    #print('input')
    #util.print_array(bin_tri)
    triangle = [[x for x in row] for row in reversed(bin_tri)]
    #triangle = util.flip_triangle2(triangle)
    size = len(triangle)

    layers = []

    #print('input')
    #util.print_array(triangle)


    for i in range(size):
        max_idx = size
        layer = []
        for j in range(size-i):
            row = triangle[j]
            if 1 in row and row.index(1) <= max_idx:
                idx = row.index(1)
                layer.append(idx+1)
                row[idx]=0
                max_idx = idx
            else:
                layer.append(0)

        layers.append(layer)

    #print('output')
    #util.print_array(layers)

    return layers


# gets layers from the bottom (schroder family)
def get_binary_layers_from_bottom(size):

    bin_list = binary_comb.get_binary_triangle(size)
    layer_list = []

    for b in bin_list:
       layer_list.append(get_layers_from_bottom(b))

    return layer_list


def get_layers_from_bottom(bin_tri):
    #print('input')
    #util.print_array(bin_tri)
    triangle = [[x for x in row] for row in reversed(bin_tri)]
    #triangle = util.flip_triangle2(triangle)
    size = len(triangle)

    layers = []

    #print('input')
    #util.print_array(triangle)

    for i in range(size):
        max_idx = size
        layer = []
        for j in range(size-i):
            row = triangle[j][0:max_idx]
            if 1 in row: #and util.find_last(row,1) <= max_idx:
                idx = util.find_last(row,1)
                layer.append(idx+1)
                triangle[j][idx]=0
                max_idx = idx+1
            else:
                layer.append(0)

        layers.append(layer)



    #print('output')
    #util.print_array(layers)

    return layers


def binary_for_layer(layer, tri_size):
    binlayer_tri = util.get_all_zero_triangle(tri_size)
    binlayer_tri = [ row for row in reversed(binlayer_tri)]
    for idx,x in enumerate(layer):

        if x > 0:
            binlayer_tri[x-1][idx]=1

    rev_tri = [ x for x in reversed(binlayer_tri)]

    layer_size = len(layer)

    # return the subtriangle for top layering
    rev_tri = rev_tri[0: layer_size]

    return rev_tri


def invert_bin_to_omega(bin_tri):
    new_bin = [[1-x for x in row] for row in bin_tri]
    omega = binary_comb.get_omega_for_cliff(new_bin)

    return omega

def invert_bin_to_combed_omega(bin_tri):
    new_bin = [[1-x for x in row] for row in bin_tri]
    B, D = binary_comb.comb(new_bin)
    omega = binary_comb.get_omega(B, D)

    return omega


def write_bin_layers(bin_list, layer_list, suffix):

    sst_list = bss.build_stacks(len(bin_list[0]))


    lines = util.get_tex_header()

    num = -1
    for bin_tri, layer_tri in zip(bin_list, layer_list):

        num += 1

        if True:

            # need to invert this mapping!
            xinv = [[1 - a for a in row] for row in bin_tri]

            omega_before = binary_comb.get_omega_for_cliff(xinv)
            B, D = binary_comb.comb(xinv)
            omega = binary_comb.get_omega(B, D)

            print(layer_tri)
            size = len(layer_tri)



            binlayer_list = [ binary_for_layer(row, size) for row in layer_tri ]

            #binlayer_list = [ [row for row in reversed(tri)]  for tri in binlayer_list]



            #### this implementation rotates the triangle!!!!

            print('binary:', bin_tri)
            for x in binlayer_list:
                print('\t', x)

            rot_bin_tri = util.rotate_triangle(bin_tri)



            rot_bin_tri = [row for row in reversed(rot_bin_tri)]

#            if rot_bin_tri in sst_list:
            if True:


                lines.append('\\subsubsection*{Triangle Number ' + str(num) + '}')
                lines.append('')



                lines.append('\\begin{tikzpicture}[scale=.5]')

                lines.append('\\node at (0,' + str(3  * size + 1) + ') {')
                lines.append(util.to_tex_ytableau([ row for row in reversed(rot_bin_tri)]))
                lines.append('};')


                lines.append('\\begin{scope}[shift={(0,' + str(3  * size/ 2) + ')}]')
                lines.append(util.omega_to_tangle(invert_bin_to_omega(rot_bin_tri)))
                lines.append('\\end{scope}')

                lines.append('\\begin{scope}[shift={(0,0)}]')
                lines.append(util.omega_to_tangle(invert_bin_to_combed_omega(rot_bin_tri)))
                lines.append('\\end{scope}')



                for count,bl in enumerate(binlayer_list):




                    lines.append('\\node at (' + str( (count +1) * 3/2 * size ) + ',' + str(3  * size +1) + ') {')
                    lines.append(util.to_tex_ytableau([row for row in reversed(bl)]))
                    lines.append('};')

                    lines.append('\\begin{scope}[shift={(' + str((count + 1) * 3/2 * size) + ',' + str(3  * size/ 2) + ')}]')
                    lines.append(util.omega_to_tangle(invert_bin_to_omega(bl)))
                    lines.append('\\end{scope}')


                    lines.append('\\begin{scope}[shift={(' + str((count + 1) * 3/2 * size) + ',0)}]')
                    lines.append(util.omega_to_tangle(invert_bin_to_combed_omega(bl)))
                    lines.append('\\end{scope}')

                lines.append('\\end{tikzpicture}')
                lines.append('')
                lines.append('\medskip')


    lines = lines + util.get_tex_footer()





    file_name = '/Users/abeverid/PycharmProjects/asm/data/sst_layer_' + suffix + str(size) + '.tex'


    print('writing to', file_name)

    out_file = open(file_name, 'w')

    out_file.writelines(["%s\n" % item for item in lines])

    #for x in lines:
    #    print(x)





#print(get_layers_from_bottom([[0],[0,1],[0,0,1]]))


size = 4
bin_list = binary_comb.get_binary_triangle(size)
sst_list = bbt.get_stack_set(size)
sst_list = [util.flip_triangle2(s) for s in sst_list]
sst_list = [[row for row in reversed(s)] for s in sst_list]

#bin_list = [ [row for row in reversed(t)] for t in bin_list]

#suffix = 'top'
#layer_list = get_binary_layers(size)
#layer_list = get_binary_layers_from_bottom(size)



suffix = 'perm_top'
layer_list = get_layers_as_permutations(size)


count = 0
for x, y in zip(bin_list, layer_list):
    #print('hi', x, y)

    # for xrow, yrow in zip(reversed(x),y):
    #
    #     print("{:<15}".format(str(xrow)), "{:<15}".format(str(yrow)))
    # print('')

    #print(x)

    xinv = [[1-a for a in row] for row in x]


    omega_before = binary_comb.get_omega_for_cliff(xinv)
    B,D = binary_comb.comb(xinv)
    omega = binary_comb.get_omega(B,D)
    #if  not binary_comb.is_magog(omega_before):

    xx = util.flip_triangle(x)

    if  xx in sst_list: #not binary_comb.is_vless_gog(omega):
        count +=1
        #print(x, omega, y)



        #print(x)

        for xrow, orow, yrow in zip(reversed(xx), omega, y):

            print("{:<15}".format(str(xrow)), "{:<15}".format(str(orow)), "{:<15}".format(str(yrow)))
        print('')


print(count)

print(len(bin_list))


write_bin_layers(bin_list, layer_list, suffix)



#print(get_layers_from_bottom([[1], [1, 1], [1, 0, 0]]))
