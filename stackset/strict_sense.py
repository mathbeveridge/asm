

import itertools

import triangle.array_util as util

import triangle.kagog_lagog as kagog_lagog



def get_ssb2(n):
    if n == 1:
        return [[1, ], ]
    elif n == 2:
        return [[[1], [2, 3]], ]
    else:
        prev_list = [[[1], [2, 3]], [[1,], [2,], [3,]] ]

        new_list = []

        for i in range(4, get_sbb_size(n)+1):
            new_list = []
            for prev in prev_list:
                for row_idx in range(len(prev)):
                    prev_len = len(prev[row_idx])
                    if prev_len < row_idx+1:
                        if prev_len == row_idx or len(prev[row_idx-1]) > prev_len:
                            new_array = util.clone_array(prev)
                            new_array[row_idx].append(i)
                            new_list.append(new_array)

                if len(prev) < n:
                    new_array = util.clone_array(prev)
                    new_array.append([i,])
                    new_list.append(new_array)

            prev_list = new_list

        return new_list







def get_sbb_size(n):
    return int(n*(n+1)/2)


def get_allowed_first_row_list(n):
    ssb_size = get_sbb_size(n)
    m = ssb_size - n + 2
    subsets = get_subsets(range(3,m),n-2)

    for s in subsets:
        print(s)

    new_subsets = [ [1, 2] + list(s) for s in subsets]

    return new_subsets

def get_subsets(my_set,k):
    return list(itertools.combinations(my_set, k))



# for each entry, we could the number of smaller entries above and to the right.
def ssb_to_lagog_list(ssb):
    lagog_list = []
    for i in range(2, len(ssb)):
        row = ssb[i]
        row_len = len(row)
        triangle = []
        for j in range(0, row_len - 2):
            val = row[j]

            lagog_row = []
            for k in range(1+j, i):

                temp_row = ssb[k]
                count = 0
                for idx in range(j+1, len(temp_row)):
                    if temp_row[idx] < val:
                        count +=1
                lagog_row.insert(0, count)
            triangle.append(lagog_row)

        lagog_list.append(triangle)

    return lagog_list


######



ssb_list2 = [
[[1],
[2, 3],
[4, 5, 6],
[7, 8, 9, 10],
[11, 12, 13, 14, 15]],]

ssb_list3 = [
[[1],
[2, 6],
[3, 7, 10],
[4, 8, 11, 13],
[5, 9, 12, 14, 15]],]


size = 4

ssb_list = get_ssb2(size)

ssb_lagog_list = []

for ssb in ssb_list:
    #util.print_array(ssb)
    #util.print_array(ssb_to_lagog_list(ssb))
    lagog_list = ssb_to_lagog_list(ssb)
    #rev_lagog_list = [[[z for z in reversed(y)] for y in x] for x in reversed(lagog_list)]
    rev_lagog_list = [x for x in reversed(lagog_list)]
    ssb_lagog_list.append(rev_lagog_list)
print(len(ssb_list))


lagog_seq_list = kagog_lagog.get_lagog_seq(size-1)

for x in ssb_lagog_list:
    if not x in lagog_seq_list:
        print('fail!', x)
    #else:
    #    print('success!', x)


print(len(ssb_lagog_list))
print(len(lagog_seq_list))


for x in lagog_seq_list:
    if not x in ssb_lagog_list:
        print('bad', x)