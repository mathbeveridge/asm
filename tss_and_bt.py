import triangle.build_tss as build_tss
import triangle.build_ballot_triangle  as build_bt

import stackset.build_stack_sets as build_stack_sets


def print_triangle(triangle):
    for row in triangle:
        print(row)
    print('-----')


def print_triangle_list(triangle_list):
    for t in triangle_list:
        print_triangle(t)
    print(len(triangle_list))

# in this implementation, we find a row entry that decreases by more than one
# we then find a nonzero entry in its diagonal and do a +1/-1 swap
# we propagate this in the fixing row for each entry equal to the one we changed
#
#  it fails for n=3. We get 2 doubles in the transformed and 1 that was already a bt + tss.
def fix_row_towards_tss(triangle, idx):
    row_length = len(triangle[idx])
    for k in range(1,len(triangle[idx])):
        while triangle[idx][k-1] - triangle[idx][k] > 1:
            offset = -1
            for j in range(1,k+1):
                if triangle[idx+j][k-j] > 0:
                    # we found it!
                    offset = j
                    break

            if (offset < 0):
                raise Exception('fix row failed! idx=' + str(idx) + ' triangle=' + str(triangle))

            # fixing row entry k, but we may have to subtract from
            # entries to the right of the fixing value
            base_value = triangle[idx+offset][k-offset]

            for j in range(k, row_length):
                if triangle[idx+offset][j-offset] == base_value:
                    triangle[idx][j] = triangle[idx][j] + 1
                    triangle[idx + offset][j - offset] = triangle[idx + offset][j - offset] - 1
                else:
                    # let's quit this look early
                    break
            #print(idx,k,triangle)

    # no need to return anything



def get_increase_idx(row):
    for k in reversed(range(1,len(row))):
        if row[k-1] < row[k]:
            print('row', row, 'increases at', k)
            print(row[k-1], row[k])
            return k

    # no increases
    return -1


# this makes progress to turn a transposed bt into a tss
def fix_trans_row_towards_tss_v1(triangle, idx):
    row_length = len(triangle[idx])

    # where is the rightmost increase im this row?
    k = get_increase_idx(triangle[idx])

    while k > -1:
        shift_idx = 0

        # print_array(triangle)

        # j will increment downward from k to 0.
        # we move diagonally SW looking for the first row where we can shift the rest of the row
        for j in reversed(range(0, k)):

            # print(idx, j)

            # diff_one determines whether we could append the row here
            # diff_two figures out whether this is an improvement (must avoid infinite loop)
            if j == 0:
                diff_one = 0
                diff_two = -1
            else:
                diff_one = triangle[idx + k - j][j - 1] - triangle[idx][k]
                diff_two = triangle[idx + k - j][j] - triangle[idx][k]

            # print('diff_one', diff_one, 'diff_two', diff_two, 'j=', j, 'k=', k, 'idx', idx)
            # print('idx+k-j', idx+k-j)

            if diff_one == 0 or diff_one == 1:
                # print(idx, k, j, idx+k-j, j+1)
                if diff_two < 0:
                    # this is an improvement. we can move the rest of the row here
                    shift_idx = j
                    break

        # let's move things
        move_len = row_length - k
        # print('move len', move_len, 'going to row', idx+k-shift_idx)
        temp_row_at_idx = [triangle[idx][i] for i in range(k, k + move_len)]
        temp_row_at_shift = [triangle[idx + k - shift_idx][i] for i in range(shift_idx, shift_idx + move_len)]

        for i in range(len(temp_row_at_idx)):
            triangle[idx][k + i] = temp_row_at_shift[i]
            triangle[idx + k - shift_idx][shift_idx + i] = temp_row_at_idx[i]

        # print_array(triangle)

        # might need another adjustment so find the rightmost increase again
        k = get_increase_idx(triangle[idx])
        # print('k is', k, 'for row', triangle[idx])


# version 2
# this makes progress to turn a transposed bt into a tss
# try to move as much of the row as possible. (NO SWAP)
# this misses 4 triangles for n=3
def fix_trans_row_towards_tss_v2(triangle, idx):
    row_length = len(triangle[idx])

    # where is the rightmost increase im this row?
    k = get_increase_idx(triangle[idx])

    while k > -1:
        shift_idx = 0

        print_triangle(triangle)
        move_len = row_length - k

        # how much can we move from each entry?
        left_bound = triangle[idx][k-1]
        temp_row_to_keep = [0] * move_len
        for i in range(0,left_bound):
            temp_row_to_keep[i] = left_bound -i
        temp_row_to_move = [triangle[idx][k+i] - temp_row_to_keep[i] for i in range(move_len)]

        print('want to move:', temp_row_to_move)


        # j will increment downward from k to 0.
        # we move diagonally SW looking for the first row where we can shift the rest of the row
        for j in reversed(range(0,k)):

            print('idx', idx, 'k', k, 'j', j)

            # diff_one determines whether we could append the row here
            # diff_two figures out whether this is an improvement (must avoid infinite loop)
            if j == 0:
                diff_one = 0
                diff_two = -1
            else:
                diff_one = triangle[idx+k-j][j-1] - triangle[idx][k]
                diff_two = triangle[idx+k-j][j] - triangle[idx][k]
                diff_one = triangle[idx + k - j][j - 1] - triangle[idx + k - j][j] - temp_row_to_move[0]
                diff_two = -1




            print('diff_one', diff_one, 'diff_two', diff_two, 'j=', j, 'k=', k, 'idx', idx)
            print('idx+k-j', idx+k-j)

            if diff_one == 0 or diff_one == 1:
                print(idx, k, j, idx+k-j, j+1)
                if diff_two < 0:
                    # this is an improvement. we can move the rest of the row here
                    shift_idx = j
                    break



        #let's move things
        print('move len', move_len, 'going to row', idx+k-shift_idx)
        temp_row_at_idx = [ triangle[idx][i] for i in range(k, k+move_len)]
        temp_row_at_shift = [triangle[idx + k - shift_idx][i] for i in range(shift_idx, shift_idx  + move_len)]

        for i in range(len(temp_row_to_keep)):
            triangle[idx][k+i] = temp_row_to_keep[i]
            triangle[idx+k-shift_idx][shift_idx+i] = triangle[idx+k-shift_idx][shift_idx+i] + temp_row_to_move[i]


        print_triangle(triangle)

        # might need another adjustment so find the rightmost increase again
        k = get_increase_idx(triangle[idx])
        #print('k is', k, 'for row', triangle[idx])


def get_cliff_drop_idx(row):
    for idx in range(1,len(row)):
        if row[idx-1] - row[idx] > 1:
            return idx
    return -1


# like v1 but we fix the original row if it decreases too much.
# this makes progress to turn a transposed bt into a tss
def fix_trans_row_towards_tss_v3(triangle, idx):
    row_length = len(triangle[idx])

    # where is the rightmost increase im this row?
    k = get_increase_idx(triangle[idx])

    while k > -1:
        shift_idx = 0

        # print_array(triangle)

        # j will increment downward from k to 0.
        # we move diagonally SW looking for the first row where we can shift the rest of the row
        for j in reversed(range(0, k)):

            # print(idx, j)

            # diff_one determines whether we could append the row here
            # diff_two figures out whether this is an improvement (must avoid infinite loop)
            if j == 0:
                diff_one = 0
                diff_two = -1
            else:
                diff_one = triangle[idx + k - j][j - 1] - triangle[idx][k]
                diff_two = triangle[idx + k - j][j] - triangle[idx][k]

            # print('diff_one', diff_one, 'diff_two', diff_two, 'j=', j, 'k=', k, 'idx', idx)
            # print('idx+k-j', idx+k-j)

            if diff_one == 0 or diff_one == 1:
                # print(idx, k, j, idx+k-j, j+1)
                if diff_two < 0:
                    # this is an improvement. we can move the rest of the row here
                    shift_idx = j
                    break

        # let's move things
        move_len = row_length - k
        # print('move len', move_len, 'going to row', idx+k-shift_idx)
        temp_row_at_idx = [triangle[idx][i] for i in range(k, k + move_len)]
        temp_row_at_shift = [triangle[idx + k - shift_idx][i] for i in range(shift_idx, shift_idx + move_len)]

        for i in range(len(temp_row_at_idx)):
            triangle[idx][k + i] = temp_row_at_shift[i]
            triangle[idx + k - shift_idx][shift_idx + i] = temp_row_at_idx[i]

        # print_array(triangle)


        # does the originial row decrease too quickly? if so, fix it.
        # this is probably a hack as written, and will fail for larger triangles.

        cliff_idx = get_cliff_drop_idx(triangle[idx])

        #print('cliff idx', cliff_idx, triangle[idx])

        debug_counter = 0

        while (cliff_idx > -1 and debug_counter < 30):
            debug_counter = debug_counter + 1
            #print_array(triangle)

            #print('cliff idx', cliff_idx, triangle[idx])

            relative_start_idx = cliff_idx - k
            shift_start_idx = shift_idx + relative_start_idx
            height = triangle[idx + k - shift_idx][shift_start_idx]
            shift_end_idx = shift_start_idx

            # print('cliff idx', cliff_idx, 'relative idx', relative_start_idx)
            #print('\t', idx, k, shift_idx, 'leads to row', idx+k-shift_idx)
            #print('start', shift_start_idx, 'height', height, 'shift_idx', shift_idx)



            #print('recorded height', triangle[idx + k - shift_idx][shift_end_idx], triangle[idx + k - shift_idx])

            while (triangle[idx + k - shift_idx][shift_end_idx]) == height:
                shift_end_idx = shift_end_idx + 1


            #print('start', shift_start_idx, 'end', shift_end_idx)

            for counter,shift_counter in enumerate(range(shift_start_idx, shift_end_idx)):
                #print('made it into the loop!!!!!!!!!!!!', counter, shift_counter)
                #print(idx, idx + k - shift_idx )
                #print(k + 1 + counter, shift_counter)

                #print('before', triangle)

                triangle[idx][cliff_idx +  counter] = triangle[idx][cliff_idx +  counter] +1
                triangle[idx + k - shift_idx][shift_counter] = triangle[idx + k - shift_idx][shift_counter] - 1

                #print('after', triangle)

            # update again if necessary
            cliff_idx = get_cliff_drop_idx(triangle[idx])

        # might need another adjustment so find the rightmost increase again
        k = get_increase_idx(triangle[idx])
        # print('k is', k, 'for row', triangle[idx])





# A new approach.
# Start at the largest row. Look for an ascent. Subtract the largest interval of 1's that you can. Repeat.
# this makes progress to turn a transposed bt into a tss
# This fails because entries get too large.
def fix_trans_row_towards_tss_v4(triangle, idx):
    row = triangle[idx]
    next_row = triangle[idx+1]
    ascent_idx = get_increase_idx(row)

    while (ascent_idx > -1):

        end_idx = ascent_idx

        while end_idx < len(row) and row[end_idx] > 0:
            end_idx = end_idx + 1

        for i in range(ascent_idx, end_idx):
            row[i] = row[i] - 1
            next_row[i-1] = next_row[i-1] + 1

        ascent_idx = get_increase_idx(row)


# Another approach.
# Start at the largest row. Look for an ascent. Move a 1 diagonally SW. Repeat.
# This fails because (a) it repeats some at the intersection of BT and TSS, and
# (b) it creates some cliffs.
def fix_trans_row_towards_tss_v5(triangle, idx):
    print(triangle, idx)
    row = triangle[idx]
    next_row = triangle[idx+1]
    ascent_idx = get_increase_idx(row)

    while (ascent_idx > -1):
        row[ascent_idx] = row[ascent_idx] - 1
        next_row[ascent_idx-1] = next_row[ascent_idx-1] + 1

        ascent_idx = get_increase_idx(row)





n=2

tss_list = build_tss.build_tss(n)
bt_list = build_bt.build_bt(n)
bt_list = build_tss.transpose_list(bt_list)

tss_only_list  = []
bt_only_list  = []

print('tss only:')
count = 0
for tss in tss_list:
    count = count + 1
    if count % 1000 == 0:
        print('tss count', count)
    if  not tss in bt_list:
        tss_only_list.append(tss)

print('total=', len(tss_only_list))
print('=============================')

print('bt only:')
count = 0
for bt in bt_list:
    count = count + 1
    if count % 1000 == 0:
        print('tss count', count)
    if  not bt in tss_list:
        bt_only_list.append(bt)
        #print_array(bt)

print('total=', len(bt_only_list))
print('=============================')



#temp_list = [ [ [2, 1, 0], [1, 1], [0] ], ]
#temp_list = [ [ [1, 0, 1], [0, 0], [0] ], ]
#temp_list = [ [ [0, 2, 1], [0, 1], [0] ], ]
#temp_list = [ [ [1, 0, 1], [1, 0], [1] ], ]
#temp_list = [ [ [0, 0, 1], [0, 0], [0] ], ]

temp_list = [[ [2, 3, 2, 1], [0, 0, 0], [0, 0], [0]],]

temp_list = [[ [3, 4, 3, 2, 1], [1, 0, 0, 0], [0, 0, 0], [0, 0], [0]],]

transformed_set = set()

for bt in bt_only_list:
    print('---- MAPPING BT to TSS ------')
    triangle = [ row.copy() for row  in bt]


    # v1, v2, v3 go from smallest to largest
    # v1 is a bijection for n=3 and smaller
    # v3 is a bijection for n=4 and smaller
    for i in reversed(range(len(triangle))):
        #print('fixing row', i, 'for', triangle)
        fix_trans_row_towards_tss_v3(triangle, i)

    # v4 goes from largest to smallet, but doesn't work
    #for i in range(len(triangle)-1):
        #print('fixing row', i, 'for', triangle)
        #fix_trans_row_towards_tss_v5(triangle, i)

    # v5 needs more passes, and doesn't work
    #for i in reversed(range(len(triangle)-1)):
        #print('fixing row', i, 'for', triangle)
        #for j in range(i, len(triangle)-1):
        #    fix_trans_row_towards_tss_v5(triangle, j)



    #print_array(triangle)
    if not triangle in tss_only_list:
        print('transform failed!')
        if triangle in tss_list:
            print('\ttriangle is both tss and bt')
        print_triangle(bt)
        print_triangle(triangle)
        print('#########')
    else:
        if not str(triangle) in transformed_set:
            transformed_set.add(str(triangle))
            print('success!')
            print_triangle(bt)
            print_triangle(triangle)
        else:
            print('transform double:')

            print_triangle(bt)
            print_triangle(triangle)
            print('*************************')


print(len(tss_only_list), 'tss only')
print(len(transformed_set),'transformed')

print('did not create these tss:')

miss_count = 0
for tss in tss_only_list:
   if str(tss) not in transformed_set:
       print_triangle(tss)
       miss_count = miss_count +1

print('missed tss', miss_count )


print('######## tss:', len(tss_list) )


pst_list = build_stack_sets.build_pst(n)

for pst in pst_list:
    pst.reverse()

count = 0

for t in tss_list:
    if build_tss.transpose(t) in pst_list:
        count = count + 1
        print_triangle(t)
        #print_array(build_tss.transpose(t))
        print('##############')

print('count', count)


print('!!!!!!!!!!!')
count=0
for bt in bt_list:
    if build_bt.is_row_gog(bt):
        count = count+1
        print_triangle(bt)
print(count)


#for pst in pst_list:
#    print(pst)