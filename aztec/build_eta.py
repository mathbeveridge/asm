

row_dict = dict()
row_dict[1] =[[k, ] for k in range(0, 2)]
row_dict[0] = [[0],]



cat_dict = dict()
cat_dict[1] =[[k, ] for k in range(0, 2)]
cat_dict[0] = [[0],]


def get_cat(size):
    if not size in cat_dict:
        new_cat = []
        prev_cat = get_cat(size-1)
        for idx in range(size+1):
            for prev in prev_cat:
                if idx >= prev[0]:
                    new_cat.append([idx] + prev)

        cat_dict[size] = new_cat

    return cat_dict[size]


def get_row(size):
    if not size in row_dict:
        cat_list = get_cat(size)
        row_list = []

        for cat in cat_list:
            row = [size-c for c in reversed(cat)]
            row_list.append(row)

        row_dict[size] = row_list

    return row_dict[size]


# initialize the eta dictionary
eta_dict = dict()
eta_dict[1] = [[[k, ],] for k in range(0,2)]



def get_eta(size):
    if not size in eta_dict:

        prev_list = get_eta(size-1)
        row_list = get_row(size)
        new_list = []

        for c in row_list:
            for p in prev_list:
                is_compatible = True
                for idx in range(len(c)-1):
                    if p[0][idx] >= c[idx]:
                        is_compatible = False
                        break

                if is_compatible:
                    new_list.append([c,] + p)

        eta_dict[size] = new_list

    return eta_dict[size]


def get_bad_diag(size):
    eta_list = get_eta(size)
    bad_list =  []

    for eta in eta_list:
        is_bad = False
        for idx in range(1,len(eta)):
            for idx2 in range(idx):
                if eta[idx-idx2][idx2] > eta[idx-idx2-1][idx2+1]:
                    is_bad = True
                    break
            if is_bad:
                break
        if is_bad:
            bad_list.append(eta)

    return bad_list



def print_triangle(t):
    for row in t:
        print(row)
    print('------')






if __name__ == '__main__':


    my_list = get_bad_diag(3)

    for m in my_list:
        print_triangle(m)

    print(len(my_list))


