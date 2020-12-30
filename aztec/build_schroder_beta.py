

### NOTE: you can get http://oeis.org/search?q=2%2C6%2C22%2C92%2C426%2C2150&sort=&language=english&go=Search
### if you "reset" at the zeros


# column are weakly increasing when you ignore zeros
def column_list(size):
    if size == 1:
        return [[k, ] for k in range(0, 2)]
    else:
        col_list = []
        prev_list = column_list(size - 1)
        for x in range(0,size + 1):
            for prev_col in prev_list:
                if x == 0 or x >= max(prev_col):
                    col_list.append(prev_col + [x, ])
        return col_list


def get_catalan_column(col):
    cat = []

    for i in range(len(col)):
        if col[i] == 0:
            cat.append(i+1)
        else:
            cat.append(col[i])

    cat = sorted(cat)

    return cat


def is_compatible(small, big):
    for i in range(len(small)):
        if small[i] > big[i+1]:
            return False

    return True


if __name__ == '__main__':

    num = 0

    small_list = column_list(1)
    big_list = column_list(2)

    for x in range(1,8):
        print(len(column_list(x)))

    # count = 0
    #
    # for s in small_list:
    #     for b in big_list:
    #         if is_compatible(s,b):
    #             print(s,b)
    #             count+=1
    #         else:
    #             print('fail', s, b)
    #
    #
    # print(count)

    #big = [1,1,3]
    #small = [1,1]

    #print(is_compatible(small, big))
