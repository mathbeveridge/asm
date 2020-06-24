def build_binary_lists(n):
    binary_lists = []
    if n == 1:
        return [[0], [1]]
    if n > 1:
        n_minus_one_lists = build_binary_lists(n-1)
        for old in n_minus_one_lists:
            new_list_zero = old + [0]
            new_list_one = old + [1]
            binary_lists += [new_list_one, new_list_zero]
    return binary_lists


def build_stacks(n):
    if n == 1:
        return [[[0]],[[1]]]
    if n > 1:
        old_stacks = build_stacks(n-1)
        next_layer_candidates = build_binary_lists(n)
        new_stacks = []
        for old_stack in old_stacks:
            last_layer = old_stack[len(old_stack)-1]
            ones = [i for i, x in enumerate(last_layer) if x == 1]
            for nl_candidate in next_layer_candidates:
                num_passed = 0
                for i in ones:
                    if sum(nl_candidate[i:n+1]) >= sum(last_layer[i:n]):
                        num_passed += 1
                if num_passed == sum(last_layer):
                    new_stack = old_stack + [nl_candidate]
                    new_stacks += [new_stack]
        return new_stacks

def build_inverted_stacks(n):
    stacks = build_stacks(n)
    inv_stacks = [ invert(s) for s in stacks]

    return inv_stacks



def invert(stack):
    inv_stack = []
    for s in stack:
        ones = [1] * len(s)
        zip_list = zip(ones, s)
        t = []
        for x,y in zip_list:
            t.append(x-y)
        inv_stack.append(t)

    return inv_stack


def reflect(stack):
    n = len(stack)
    new_stack = []

    for i in range(1,n+1):
        new_stack.append([0]*i)

    for i in range(len(stack)):
        row = stack[i]
        for j in range(len(row)):
            new_stack[n-1-j][n-1-i] = stack[i][j]

    return new_stack