

# deal with gog by adding the largest diagonal
def diag_layer_list(size):
    if size == 1:
        return [[k, ] for k in range(0,2)]
    else:
        layer_list = []
        prev_list = diag_layer_list(size - 1)
        for x in range(size+1):
            for prev_layer in prev_list:
                if  x <= prev_layer[0] + 1:
                    layer_list.append([x, ] + prev_layer)
        #print('diag layer list', size, layer_list)
        return layer_list


# columns increase
def check_gog_col(prev_diag, diag):
    for idx in range(len(prev_diag)):
        if prev_diag[idx] > diag[idx]:
            #print('failing', idx, prev_diag, diag)
            return False
    return True

# columns increase
def check_gog_col_strict_decr(prev_diag, diag):
    for idx in range(len(prev_diag)):
        if prev_diag[idx] >= diag[idx]:
            #print('failing', idx, prev_diag, diag)
            return False
    return True

# diag cannot decrease by more than 1
def check_gog_row(prev_layer, layer):
    for idx in range(len(prev_layer)):
        if prev_layer[idx] > layer[idx+1]:
            return False
    return True

# gog rules:
# rows weakly increasing
# columns weakly decreasing
# diagonals can increase; or decrease by at most 1
# a(i,j) <= n-i
def build_gog(n):
    if n == 1:
        return [[[0],],[[1],]]
    else:
        current_gogs = []
        prev_gogs = build_gog(n-1)
        diag_list = diag_layer_list(n)
        for gog in prev_gogs:
            #print('gog=', gog)
            prev_diag = [gog[i][i] for i in range(n-1)]
            #print('prev_diag', prev_diag)
            for diag in diag_list:
                if check_gog_col(prev_diag, diag) and check_gog_row(prev_diag, diag):
                    new_gog = [[diag[0]],]
                    for idx in range(n-1):
                        new_gog.append( gog[idx] + [diag[idx+1]])
                    current_gogs.append(new_gog)
        return current_gogs



#########
def no_eq_diag_layer_list(size):
    if size == 1:
        return [[k, ] for k in range(0,2)]
    else:
        layer_list = []
        prev_list = no_eq_diag_layer_list(size - 1)
        for x in range(size+1):
            for prev_layer in prev_list:
                if  x == prev_layer[0] + 1 or x < prev_layer[0]:
                    #print(x,prev_layer)
                    layer_list.append([x, ] + prev_layer)
        #print('diag layer list', size, layer_list)
        return layer_list

#########
# def num_eq_diag_layer_list(size,  num_eq):
#     if size == 1:
#         if num_eq == 0:
#             return [[k, ] for k in range(0,2)]
#         else:
#             return []
#     else:
#         layer_list = []
#         prev_list = no_eq_diag_layer_list(size - 1)
#         for x in range(size+1):
#             for prev_layer in prev_list:
#                 if  x == prev_layer[0] + 1 or x < prev_layer[0]:
#                     #print(x,prev_layer)
#                     layer_list.append([x, ] + prev_layer)
#         #print('diag layer list', size, layer_list)
#         return layer_list


def build_no_eq_gog(n):
    if n == 1:
        return [[[0],],[[1],]]
    else:
        current_gogs = []
        prev_gogs = build_no_eq_gog(n-1)
        diag_list = no_eq_diag_layer_list(n)
        for gog in prev_gogs:
            #print('gog=', gog)
            prev_diag = [gog[i][i] for i in range(n-1)]
            #print('prev_diag', prev_diag)
            for diag in diag_list:
                if check_gog_col(prev_diag, diag) and check_gog_row(prev_diag, diag):
                    new_gog = [[diag[0]],]
                    for idx in range(n-1):
                        new_gog.append( gog[idx] + [diag[idx+1]])
                    current_gogs.append(new_gog)
        return current_gogs


def build_gog_col_strict_decr(n):
    if n == 1:
        return [[[0],],[[1],]]
    else:
        current_gogs = []
        prev_gogs = build_gog_col_strict_decr(n-1)
        diag_list = diag_layer_list(n)
        for gog in prev_gogs:
            #print('gog=', gog)
            prev_diag = [gog[i][i] for i in range(n-1)]
            #print('prev_diag', prev_diag)
            for diag in diag_list:
                if check_gog_col_strict_decr(prev_diag, diag) and check_gog_row(prev_diag, diag):
                    new_gog = [[diag[0]],]
                    for idx in range(n-1):
                        new_gog.append( gog[idx] + [diag[idx+1]])
                    current_gogs.append(new_gog)
        return current_gogs


def build_gog_unimodal_diag(n):
    if n == 1:
        return [[[0],],[[1],]]
    else:
        current_gogs = []
        prev_gogs = build_gog_unimodal_diag(n-1)
        diag_list = diag_unimodal_list(n)
        for gog in prev_gogs:
            #print('gog=', gog)
            prev_diag = [gog[i][i] for i in range(n-1)]
            #print('prev_diag', prev_diag)
            for diag in diag_list:
                if check_gog_col(prev_diag, diag) and check_gog_row(prev_diag, diag):
                    new_gog = [[diag[0]],]
                    for idx in range(n-1):
                        new_gog.append( gog[idx] + [diag[idx+1]])
                    current_gogs.append(new_gog)
        return current_gogs


def diag_unimodal_list(size):
    if size == 1:
        return [[k, ] for k in range(0,2)]
    else:
        layer_list = []
        prev_list = diag_unimodal_list(size - 1)
        for x in range(size+1):
            for prev_layer in prev_list:
                next_num = prev_layer[0]
                if  x <= next_num + 1:
                    for idx in range(len(prev_layer)):
                        if not prev_layer[idx] == next_num:
                            break

                    if prev_layer[idx] == next_num:
                        #print('constant layer', x, prev_layer)
                        layer_list.append([x, ] + prev_layer)
                    elif prev_layer[idx] < next_num:
                        if next_num <= x:
                            #print('down slope', x, prev_layer)
                            layer_list.append([x, ] + prev_layer)
                        elif min(prev_layer) == prev_layer[-1]:
                            #print('monotone down slope', x, prev_layer)
                            layer_list.append([x, ] + prev_layer)
                    elif prev_layer[idx] > next_num:
                        if next_num >= x:
                            #print('up slope', x, prev_layer)
                            layer_list.append([x, ] + prev_layer)
                        elif max(prev_layer) == prev_layer[-1]:
                            #print('monotone up slope', x, prev_layer)
                            layer_list.append([x, ] + prev_layer)


        #print('diag layer list', size, layer_list)
        return layer_list


def reflect(triangle):
    size = len(triangle)
    ret_val = [[0] * k for k in range(1, size + 1)]
    for i in range(size):
        for j in range(i + 1):
            # print('>>>>>',i,j, size-1-j, size-1-i)
            ret_val[i][j] = triangle[size - 1 - j][size - 1 - i]

    #ret_val.reverse()
    return ret_val



def reflect_list(triangle_list):
    return [ reflect(t) for t in triangle_list]






#print(no_eq_diag_layer_list(3))
#print(diag_layer_list(3))


def test():
    for n in range(1,4 ):
        gogs = build_gog_col_strict_decr(n)

        for g in gogs:
            for row in g:
                print(row)
            print('----')
        print(len(gogs))

    #for n in range(1,10):
    #    print(len(diag_layer_list(n)))


for n in range(1,7):
    gogs = build_gog_unimodal_diag(n)

    #for x in gogs:
    #    print(x)
    print(len(gogs))