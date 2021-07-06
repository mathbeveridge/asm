
import triangle.array_util as util
import sst_explore
from stackset import build_stack_set as build_stack_set
from stackset import stack_set_stats as stack_set_stats


involution_dict = dict()
involution_dict[1] = [[1,],]
involution_dict[2] = [[1,2],[2,1]]

def get_involutions(size):
    if not size in involution_dict:
        prev_list = get_involutions(size-1)

        new_list = []

        for prev in prev_list:
            # add [n,] as a singleton
            new_list.append(prev + [size,])

            for idx,x in enumerate(prev):
                if x == idx +1:
                    new_inv = [ y for y in prev]
                    new_inv[idx] = size
                    new_inv.append(idx+1)
                    new_list.append(new_inv)

        involution_dict[size] = new_list

    return involution_dict[size]

word_dict = dict()
word_dict[1] = [[0], [1]]

def get_words(size):
    if not size in word_dict:
        prev_words = get_words(size-1)

        new_words =  [ [0,] + prev for prev in prev_words]

        for i in range(1, size):
            for prev in prev_words:
                if prev.count(i) == 1:
                    new_words.append([i,] + prev)

        for prev in prev_words:
            new_words.append([size,] + prev)

        word_dict[size] = new_words


    return word_dict[size]

def word_to_triangle(word):
    size = len(word)
    tri = util.get_all_zero_triangle(size)

    for idx,w in enumerate(word):
        if w > 0:
            tri[size-w][idx] = 1

    for idx in range(size):
        if sum(tri[idx]) == 0:
            del tri[idx]
            for k in range(idx):
                tri[k].append(0)
            tri.insert(0,[0,])

    return tri




def check_sst(triangle):
    for idx in range(len(triangle)-1):
        if not check_sst_row(triangle[idx], triangle[idx+1]):
            return False

    return True

def check_sst_row(row1,row2):
    for idx in range(len(row1)):
        if (sum(row1[idx:]) > sum(row2[idx:])):
            return False

    return True


def get_key(triangle):
    key = 0
    t = util.flip_triangle(triangle)

    for idx,row in enumerate(t):
        if sum(row) > 0:
            key = key + 2**idx

    return key

def compare_words():
    for size in range(4,5):

        sst_list = build_stack_set.build_stacks(size)
        sst_list = stack_set_stats.one_one_per_col(sst_list, size)

        words = get_words(size)
        bad_count = 0

        good_tri_list = []

        bad_map = dict()


        for w in words:
            t = word_to_triangle(w)
            is_sst = check_sst(t)

            if not is_sst:
                print(w)
                util.print_array(t)
                key = get_key(t)

                if not key in bad_map:
                    bad_map[key] = []

                bad_map[key].append(t)

                bad_count += 1
            else:
                good_tri_list.append(t)

        print('size', size)
        print('total', len(words))
        print('bad', bad_count)
        print('good', len(words)-bad_count)


        sst_unmatched_map = dict()

        for sst in sst_list:
            if not sst in good_tri_list:
                key = get_key(sst)

                if not key in sst_unmatched_map:
                    sst_unmatched_map[key]= []
                sst_unmatched_map[key].append(sst)
        print('bad map', len(bad_map))
        print('sst unmatched map', len(sst_unmatched_map))

        print('--------------')



    for key in bad_map:
        print('==================')
        word_list = bad_map[key]
        sst_list = sst_unmatched_map[key]
        print('KEY', key, 'bad', len(word_list), 'sst', len(sst_list))
        print('words')
        for w in word_list:
            util.print_array(w)
        print('sst')
        for s in sst_list:
            util.print_array(s)

def tree_to_involution(tree):
    inv = []
    for path in tree:
        path_length = len(path)
        if path_length % 2 == 0:
            for idx in range(int(path_length/2)):
                inv.append([path[idx], path[-1-idx]])
        else:
            for idx in range(int((path_length -1)/2)):
                inv.append([path[idx+1], path[-1-idx]])

            inv.append([path[0]])

    return inv

def build_trees(size):
    sst_list = build_stack_set.build_stacks(size)
    sst_list = stack_set_stats.one_one_per_col(sst_list, size)


    tree_list = []

    for sst in sst_list:
        index_list = []
        for row in sst:
            index_list.append([i for i, x in enumerate(row) if x==1])

        #### match to the rightmost available
        #m = len(index_list[-1])
        #path_list = []
        # for idx in range(1,m+1):
        #     path = [index_list[-1][-idx]+1]
        #     for row_idx in range(2,size+1):
        #         print(index_list[-row_idx], 'has size', len(index_list[-row_idx]))
        #         if len(index_list[-row_idx]) >= idx:
        #             path.append(index_list[-row_idx][-idx]+1)
        #
        #     path_list.append(path)

        #### match to the "first available"
        #### this actually seems to do worse. ugh!
        path_list = [[x,] for x in index_list[-1]]

        print('processing ', sst)

        for k in reversed(range(size-1)):
            taken_idx_list = []
            row_idx_list = index_list[k]

            for val in reversed(row_idx_list):
                for i,path in enumerate(path_list):
                    if not i in taken_idx_list and val < path[-1]:
                        print('\tmatching', val, 'to', path[-1] )
                        taken_idx_list.append(i)
                        path.append(val)
                        break

        path_list =  [[x+1 for x in path] for path in  path_list]

        print('\t\t', path_list)

        tree_list.append(path_list)

    print('THE INVOLUTIONS')


    sst_inv_list = []


    for sst,tree in zip(sst_list,tree_list):
        #print(tree)
        inv = tree_to_involution(tree)
        #print(inv)

        temp = [0] * size

        for x in inv:
            if len(x) == 1:
                val = x[0]
                temp[val-1] = val
            else:
                v1 = x[0]
                v2 = x[1]
                temp[v1-1] = v2
                temp[v2-1] = v1

        print(temp)

        if str(temp) == '[3, 4, 1, 2, 5]':
            print('duplicate', inv, 'tree', tree)
            util.print_array(sst)

        sst_inv_list.append(temp)
        #util.print_array(sst)

    print(len(sst_inv_list))

    inv_list = get_involutions(size)
    for x in inv_list:
        if not x in sst_inv_list:
            print('missing', x)
    print(len(inv_list))


build_trees(4)


