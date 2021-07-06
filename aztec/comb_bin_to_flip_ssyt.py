import aztec.binary_comb as binary_comb
import aztec.build_ssyt as ssyt_triangle
import triangle.array_util as util
import triangle.build_binary_triangle as binary_triangle


# add the end index later!
# this is my first attempt is does not swap rows, just pushes up and down.
# not sure how to handle going below: this won't preserve down steps
def comb_bin_row(triangle_in, row_idx, comb_end_idx):

    triangle = [[x for x in row] for row in triangle_in]

    big_row = [x for x in triangle[row_idx-1]]
    small_row = [x for x in triangle[row_idx]]
    small_size = len(small_row)


    #match_height = -1
    for i in range(small_size):
        if small_row[i] > big_row[i+1]:
            #print('\t\tfix problem')
            gap = small_row[i] - big_row[i+1]
            # diagonal is not weakly decreasing
            # where where these rows first equal (if ever?)
            start_idx = i
            while (start_idx > 0 and small_row[start_idx-1] == big_row[start_idx-1] ):
                start_idx+= -1

            end_idx = i+1
            # how long do the paths overlap (if at all)?
            while (end_idx < comb_end_idx) and (small_row[end_idx]  == big_row[end_idx]):
                end_idx+=1

            sm = [x for x in small_row]
            bg = [x for x  in big_row]

            for j in range(start_idx, i):
                big_row[j] = big_row[j] + 1

            for j in range(0, end_idx - i):
                big_row[i+j] = big_row[i+j] + 1 + j

            for j in range(start_idx, comb_end_idx):
                small_row[j] = small_row[j]-1



    triangle[row_idx] = small_row
    triangle[row_idx-1] = big_row

    return triangle


# let's try swapping where it gets bad
def comb_bin_row_swap(triangle_in, row_idx, comb_end_idx):

    triangle = [[x for x in row] for row in triangle_in]

    big_row = [x for x in triangle[row_idx-1]]
    small_row = [x for x in triangle[row_idx]]
    small_size = len(small_row)


    #match_height = -1
    for i in range(small_size):
        if small_row[i] > big_row[i+1]:
            #print('\t\tfix problem')
            gap = small_row[i] - big_row[i+1]
            # diagonal is not weakly decreasing
            # where where these rows first equal (if ever?)
            start_idx = i
            while (start_idx > 0 and small_row[start_idx-1] == big_row[start_idx-1] ):
                start_idx+= -1

            end_idx = i+1
            # how long do the paths overlap (if at all)?
            while (end_idx < comb_end_idx) and (small_row[end_idx] >= big_row[end_idx]):
                end_idx+=1

            sm = [x for x in small_row]
            bg = [x for x  in big_row]

            # BEGIN STRAIGHT UP/DOWN SWAP
            # for j in range(start_idx, end_idx):
            #     big_row[j] = sm[j] + 1
            #
            # for j in range(start_idx, comb_end_idx):
            #     small_row[j] = bg[j] - 1
            # END STRAIGHT UP/DOWN SWAP

            if i < small_size - 1:
                overlap = (small_row[i+1] == small_row[i] -1) and (small_row[i+1] == big_row[i+1])
            else:
                overlap = False

            if overlap:
                overlap_bump = 0
            else:
                overlap_bump = 0


            # BEGIN SHIFT SWAP
            for j in range(start_idx, i+1):
                big_row[j] = sm[j] + 1

            # when they overlap, increase height each time
            for j in range(i+1, end_idx):
                big_row[j] = sm[j]  + 1 + overlap_bump

            for j in range(end_idx, comb_end_idx+1): # or should we go to the end of the big row?
                big_row[j] = big_row[j] + overlap_bump

            for j in range(start_idx, i+1):
                small_row[j] = bg[j] - 1

                for j in range(i+1, end_idx):
                    small_row[j] = bg[j] - 1 + overlap_bump

            # MY HACK
            #if (big_row[end_idx-1] == big_row[end_idx])+1:
                # add a downstep
            #    big_row[end_idx-1] = big_row[end_idx-1] + 1

            # for j in range(i+1, end_idx):
            #         small_row[j] = bg[j]
            # END STRAIGHT UP/DONW SWAP



    triangle[row_idx] = small_row
    triangle[row_idx-1] = big_row

    return triangle



def comb_bin(triangle):
    size = len(triangle)
    for i in range(1, size):
        print('dealing with row,', i)
        for j in reversed(range(1,i+1)):
            print('\tcomb row', j, triangle)
            triangle = comb_bin_row_swap(triangle, j, size-i)
            print('\t\toutput: ', triangle)

    return triangle




def test_bin_and_flipped_reordered():
    ssyt_list = ssyt_triangle.get_ssyt_matrix(4)
    bin_tri_reordered = ssyt_triangle.get_bin3_tri_reordered()

    ssyt_omega_list = [ util.get_absolute_array(ssyt_triangle.flip_matrix_to_omega(m)) for m in ssyt_list ]

    bin_omega_list = [ util.get_absolute_array(binary_comb.get_omega_for_cliff(b)) for b in bin_tri_reordered ]



    count = 0
    diff_count = 0
    for s,b in zip(ssyt_omega_list, bin_omega_list):
        if not s == b:
            if not (s == comb_bin(b)):
                print("FAILED!!!!!!!!!!")
                print('>>>>>>>>>>> count=', count)
                print('binary')
                util.print_array(b)
                print('flipped ssyt x')
                util.print_array(s)
                diff_count += 1
                print('*******combed binary')
                util.print_array(comb_bin(b))
        count+=1

    print('diff count ', diff_count)


def test_bin_and_flipped(size):
    ssyt_list = ssyt_triangle.get_ssyt_matrix(size+1)
    bin_tri_list = binary_triangle.get_binary_triangle(size)

    bin_tri_list = [[row for row in reversed(tri)] for tri in bin_tri_list]

    ssyt_omega_list = [ util.get_absolute_array(ssyt_triangle.flip_matrix_to_omega(m)) for m in ssyt_list ]

    bin_omega_list = [ util.get_absolute_array(binary_comb.get_omega_for_cliff(b)) for b in bin_tri_list ]


    ssyt_map = dict()


    count = 0

    for b in  bin_omega_list:
        #print('processing', b)
        out = comb_bin(b)
        key = str(out)

        if not out in ssyt_omega_list:
            print('FAILED: no match for binary', b, 'with image', out)
        elif key in ssyt_map:
            ssyt_map[key] = ssyt_map[key]  + [ b,]
            print('DUPLICATE', out, 'mapped to by', ssyt_map[key])
        else:
            ssyt_map[key]  = [b,]

    for s in ssyt_omega_list:
        if str(s) not in ssyt_map:
            print('MISSING SSYT', s)

    print(len(ssyt_map))

    for key in ssyt_map:
        if len(ssyt_map[key]) > 1 or not key == str(ssyt_map[key][0]):
            print('ssyt', key, 'binary', ssyt_map[key])


test_bin_and_flipped(3)


b = [[2, 1, 1], [2, 1], [0]]
s = [[3, 3, 1], [1, 0], [0]]

# b = [[2, 1, 1], [1, 0], [1]]
# s = [[3, 1, 1], [1, 0], [0]]



# b = [[2, 1, 1], [1, 0], [1]]
# s = [[3, 1, 1], [1, 0], [0]]

b = [[3, 2, 2, 2], [3, 3, 2], [2, 2], [1]]





b = [[3, 2, 1], [2, 2], [0]]

b = [[2, 1, 0], [2, 1], [0]]

b = [[2, 2, 1], [2, 2], [1]]


b = [[3, 2, 1], [2, 2], [1]]

b = [[2, 1, 1], [2, 1], [0]]

b = [[2, 1, 1], [2, 1], [0]]

print('binary')
util.print_array(b)
#print('flipped ssyt')
#util.print_array(s)
print('*******combed binary')
util.print_array(comb_bin(b))
