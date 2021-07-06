
import triangle.gog_magog as gog_magog
import triangle.array_util as util
import stackset.build_stack_set as bss



def get_lagog_seq(n):
    lagog_list = gog_magog.build_lagog(n)

    if n == 2:
        return [ [t,] for t in lagog_list]
    else:
        new_list = []
        prev_seq_list = get_lagog_seq(n-1)

        for t in lagog_list:
            for seq in prev_seq_list:
                prev_t = seq[0]

                if is_compatible(t, prev_t):
                    new_list.append( [t,] + seq)

    return new_list


def is_compatible(tri, prev_tri):
    for i in range(len(prev_tri)):
        for j in range(len(prev_tri[i])):
            if tri[i][j] > prev_tri[i][j]:
                return False

    return True



def do_compare(set1, set2, rosetta):
    size = len(rosetta) + 2

    if set2[0]  > set1[0]:
        s1 = set2
        s2 = set1
        mult = -1
    else:
        s1 = set1
        s2 = set2
        mult = 1

    if s1[0] == s2[0]:
        diff = s1[1] - s2[1]
        if diff == 0 :
            return 0
        else:
            return  mult * diff/ abs(diff)
    elif s1[1] == s2[1]:
        diff = s1[0] - s2[0]
        if diff == 0 :
            return 0
        else:
            return  mult * diff/ abs(diff)
    elif s1[1] > s2[1]:
        return mult
    else:
        # need to look it up
        triangle = rosetta[s1[1]]

        start_row = -1
        start_col =  size - s1[0]

        col_diff = s1[0] - s2[0]
        row_diff = s2[1] - s1[1]

        tri_len = len(triangle)

        row_idx = start_row+row_diff
        col_idx = start_col+col_diff - 1

        lagog_row_idx = row_idx
        lagog_row = triangle[lagog_row_idx]
        m = len(lagog_row)
        mm = m-1-row_idx
        val = lagog_row[mm]

        test_val =  col_idx >= len(lagog_row) -  mm - val

        if test_val:
            return 1
        else:
            return -1



def get_sst_seq(n):
    sst_list = bss.build_stacks(n)

    if n == 1:
        return [ [t,] for t in sst_list]
    else:
        new_list = []
        prev_seq_list = get_sst_seq(n-1)

        for sst in sst_list:
            for seq in prev_seq_list:
                prev_sst = seq[0]

                if is_sst_compatible(sst, prev_sst):
                    new_list.append( [sst,] + seq)

    return new_list

def is_sst_compatible(sst, prev_sst):
    for i in range(len(prev_sst)):
        prev_row = prev_sst[i]
        new_row = sst[i+1]
        prev_len = len(prev_row)
        prev_sum = 1
        #print('new and prev', new_row, prev_row)
        new_sum = new_row[prev_len]

        for j in reversed(range(prev_len)):
            prev_sum += prev_row[j]
            new_sum += new_row[j]

            if new_sum > prev_sum:
                return False

    return True



#lagog_list = gog_magog.build_lagog(3)

size = 4

seq_list = get_lagog_seq(size)

print('all sequences')

bad_count = 0

for seq in seq_list:
    #print(seq)
    #util.print_array(seq)
    #print(seq[0])
    #print(seq[0][0])
    #print(seq[0][0][size-2])
    if seq[0][0][size-2] < size-1 and seq[0][0][size-3] > 0 and seq[1][1][0] == 0:
        bad_count += 1
        print('bad a', seq)
    elif seq[0][0][size-2] == size-1 and seq[0][0][size-3] == 0 and seq[1][1][0] > 0:
        bad_count += 1
        print('bad b', seq)

print('num lagog sequence', len(seq_list))
print('bad count', bad_count)
print(len(seq_list) - bad_count)



set1 = [5,0]
set2 = [4,2]
rosetta = [ [[1,2,3], [1,2], [0]], [[1, 2], [1]], [[1]]]

#print(set1, set2)
#print(do_compare(set1, set2, rosetta))



#seq_list = get_sst_seq(3)
#
# print('all sequences')
#
# for t in seq_list:
#     util.print_array(t)
#print('num sst sequence', len(seq_list))


