

row_map = dict()
row_map[0] = [ []]
row_map[1] = [ [0,], [1,]]

# creates the sandwich schroder path representation
def get_row(n):
    if not n in row_map:

        row_list = []

        for k in range(n+1):

            if k == 0:
                prev_row_list1 = get_row(n - 1)
            else:
                prev_row_list1 = get_row(n-k)

            if k > 1:
                prev_row_list2 = get_row(k-1)

                for r1 in prev_row_list1:
                    for r2 in prev_row_list2:
                        new_row = [k,] + r2 + r1
                        row_list.append(new_row)
            else:
                for r1 in prev_row_list1:
                    new_row = [k,] + r1
                    row_list.append(new_row)

        row_map[n] = row_list


    return row_map[n]

def sandwich_to_hdv(sandwich_row):
    path = []

    idx = 0

    while (idx < len(sandwich_row)):
        value = sandwich_row[idx]
        if value == 0:
            path.append('D')
            idx = idx + 1
        else:
            path.append('H')

            if value > 1:
                sub_sandwich_row = sandwich_row[idx+1:idx+value]
                path = path + sandwich_to_hdv(sub_sandwich_row)

            path.append('V')
            idx = idx + value

    return path


def sandwich_to_path(sandwich_row):
    hdv = sandwich_to_hdv(sandwich_row)

    x = 0
    y = len(sandwich_row)

    path = [ (x,y)]

    for val in hdv:
        if val == 'H':
            x += 1
        elif val == 'D':
            x += 1
            y += -1
        elif val == 'V':
            y += -1

        path.append((x,y))

    return path


## really has_sublist
def has_hdv_pattern(hdv_list, pattern):

    for i in range(len(hdv_list) - len(pattern) + 1):
            if hdv_list[i] == pattern[0]:
                n = 1
                while (n < len(pattern)) and (hdv_list[i + n] == pattern[n]):
                    n += 1

                if n == len(pattern):
                    return True


    return False


pattern_list = ['HH', 'HD', 'HV', 'DH', 'DD', 'DV', 'VH', 'VD', 'VV']

def pattern_map_for_hdv(hdv_list):
    pattern_map = dict()

    for p in pattern_list:
        plist = [char for char in p]
        pattern_map[p] = has_hdv_pattern(hdv_list, plist)

    return pattern_map

# size = 5
# row_list = get_row(size)
#
# pattern_count = 0
#
# for r in row_list:
#     print(r, sandwich_to_hdv(r), sandwich_to_path(r))
#     hdv = sandwich_to_hdv(r)
#
#     if has_hdv_pattern(hdv, ['V', 'H']):
#         pattern_count = pattern_count + 1
#         print('\t', has_hdv_pattern(hdv, ['V', 'H']))
# print('total', len(row_list))
# print('pattern count', pattern_count)
# print( str(len(row_list) - pattern_count))