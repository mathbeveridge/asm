

lehmer_dict = dict()
lehmer_dict[1] = [ [0],]
lehmer_dict[2] = [ [0,0], [1,0]]


def get_lehmer_code(size):
    if not size in lehmer_dict:
        prev_list = get_lehmer_code(size-1)

        new_list = []
        for x in range(size):
            for prev in prev_list:
                new_list.append([x,] + prev )
        lehmer_dict[size] = new_list

    return lehmer_dict[size]

###### 321 avoiding  NOT QUITE
# code[i] - code[j] <= j - i
def is_321_avoiding_not_quite(code):
    for i in range(len(code)):
        for j in range(i,len(code)):
            if code[i] - code[j] > j-i:
                return False
    return True



# THIS GIVES THE LARGE SCHRODER NUMBERS
# but isn't quite 123 avoiding
def is_123_avoiding_schroder(code):
    size = len(code)
    for i in range(size):
        for j in range(i,len(code)):
            if code[j] > code[i] and code[j] - code[i]   >  i - j and not code[j] == size-1 - j:
                #print('code', code, i, j, 'fail', code[j], str(size-1-j))
                return False
    return True


# this gives the odd bell numbers
def is_123_avoiding_odd_bell(code):
    size = len(code)
    for i in range(size-1):
        if  code[i+1] >= code[i] and not code[i+1] == size-i-2:
                #print('code', code, i, i+1, 'fail', code[i+1], str(size-i-1))
                return False
    return True

####  123 avoiding
# if r(j) > r(i) then r(j) = n-j
def is_123_avoiding(code):
    size = len(code)
    for i in range(size-1):
        for j in range(i+1, size):
            if  code[j] >= code[i] and not code[j] == size-1-j:
                #print('code', code, i, j, 'fail', code[j], str(size-j))
                return False
    return True


# is 213  avoiding is known
# is 132 avoiding is known


####  312 avoiding
# r(i+1) >= r(i) - 1
# allowed to decrease by 1
def is_312_avoiding(code):
    size = len(code)
    for i in range(size-1):
        if code[i+1] < code[i] - 1:
            return False

    return True


####  321 avoiding BELL NUMBERS
# if r(i) > r(i+1) then r(i+1)=0
# allowed to decrease by 1
def is_321_avoiding_bell(code):
    size = len(code)
    for i in range(size-1):
        if code[i+1] < code[i] and code[i+1] > 0:
            return False

    return True


####  321 avoiding B
    # if r(j) >= r(i) - # 0's between i and j
def is_321_avoiding(code):
    size = len(code)
    for i in range(size-1):
        for j in range(i+1,size):
            if code[j] > 0:
                zeros = sum([1 for k in range(i+1,j) if code[k]==0])
                if code[j] < code[i] - zeros:
                    return False

    return True


####  not quite 231 avoiding, but it is a Catalan family!!!
# if r(i) > 1 then r(i) > r(j)
# allowed to decrease by 1
def is_231_avoiding_something_else(code):
    size = len(code)
    for i in range(size-1):
        for j  in range(i+1, size):
            if code[i] > 0 and  code[i] <= code[j]:
                return False

    return True

####  231 avoiding,
# if r(i) > 0 then next r(i) satisify r(k) <= r(i) -  (k-i)
def is_231_avoiding(code):
    size = len(code)
    for i in range(size-1):
        for j  in range(i+1, size):
            if code[i] > 0:
                for j in range(i+1, i+code[i]+1):
                    if code[j] > code[i] - j + i:
                        return False

    return True


for size in range(3,9):
    my_list =  get_lehmer_code(size)

    #print(len(my_list))

    avoiding_list = [code for code in my_list if is_321_avoiding_bell(code)]

    #for code in avoiding_list:
    #    print(code)

    print(len(avoiding_list))



print('test', is_321_avoiding_bell([0,0,2,0,0]))