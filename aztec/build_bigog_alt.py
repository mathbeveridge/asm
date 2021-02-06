import aztec.build_omega as build_omega

col_dict = dict()
col_dict[1] =[[k, ] for k in reversed(range(0, 2))]
col_dict[0] = [(0,), ]


def get_column(size):
    if size not in col_dict:
        omega_row_list = build_omega.get_row(size)
        col_list = [ [abs(x) for x in row] for row in  omega_row_list]
        col_dict[size] = col_list

    return col_dict[size]


bigog_dict = dict()
bigog_dict[1] = [[[k, ],] for k in range(0,2)]

def get_bigog(size):
    if not size in bigog_dict:
        new_list = []
        prev_list = get_bigog(size-1)
        col_list = get_column(size)

        for col in col_list:
            for prev in  prev_list:
                is_compatible = True
                #for idx in range(len(prev)):
                #    if prev[-1][idx] > col[idx]:
                #        is_compatible = False
                #        break

                if is_compatible:
                    new_list.append(prev + [col])

        bigog_dict[size] = new_list

    return bigog_dict[size]


if __name__ == '__main__':

    my_list = get_bigog(3)

    for x in my_list:
        for col in x:
            print(col)
        print('-----')

    print(len(my_list))

    #print(get_column(3))