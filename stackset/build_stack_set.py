import triangle.array_util as util
import triangle.gog_magog as gog_magog
import aztec.binary_comb as binary_comb

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


# inverted stacks satisfy:
# partial sum of row i+1 can exceed row i by at most 1.
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

        print('stack', stack, 'inverted', inv_stack)

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


def stack_to_kagog(stack):
    kagog = []
    for row in stack:
        krow = []
        for idx in range(len(row)):
            if row[idx] == 1:
                krow.append(idx+1)
            else:
                krow.insert(0,0)
        kagog.append(krow)
    return kagog

# take an SST directly to a magog
# the 0's indicate a diagonal step (block removal)
# with each 1 we encounter, we fill in the column
def stack_to_magog(stack):
    size = len(stack)
    magog = util.get_all_zero_triangle(size)

    print('CONVERTING')
    util.print_array(stack)

    for idx in range(size):

        stack_row = stack[size - 1 - idx]

        start_idx = idx
        mrow_idx =  size - 1
        for i in reversed(range(len(stack_row))):
            if stack_row[i] == 0:
                start_idx += 1
            else:
                mrow_len = len(magog[mrow_idx])
                for j in range(start_idx, mrow_len):
                    magog[mrow_idx][j] = magog[mrow_idx][j] + 1
                mrow_idx += -1

        print('------ idx=', idx)
        util.print_array(magog)

    return magog


def test_to_magog(size):

    magogs = gog_magog.build_magog(size)

    magogs = [[row for row in reversed(magog)] for magog in magogs]

    stacks = build_stacks(size)
    # stacks = [[[1], [0,1]]]
    for s in stacks:
        #        print('******************')
        # util.print_array(s)
        m = stack_to_magog(s)
        if not m in magogs:
            util.print_array(stack_to_magog(s))

            #    for m in magogs:
            #        util.print_array(m)


def write_file(size):
    size = 4
    my_list = build_inverted_stacks(size)
    #    my_list = build_stacks(size)


    lines = util.get_tex_header()

    for s in my_list:
        s = [[x for x in reversed(row)] for row in s]

        lines.append('\\begin{tikzpicture}[scale=.5]')

        lines.append('\\node at (0,' + str(size / 2) + ') {' + util.to_tex_ytableau(s) + '};')
        lines.append('\\begin{scope}[shift={(' + str(1.5 * size) + ',0)}]')

        omega = binary_comb.get_std_omega_for_cliff(s)

        lines.append(util.omega_to_tangle(omega))

        lines.append('\\end{scope}')

        lines.append('\\end{tikzpicture}')
        lines.append('')
        lines.append('\smallskip')

    lines = lines + util.get_tex_footer()

    file_name = '/Users/abeverid/PycharmProjects/asm/data/sst/sst' + str(size) + '.tex'

    file = open(file_name, 'w')

    for line in lines:
        file.write(line)
        file.write('\n')

    file.close()



def to_file():
    size = 3
    stack_list = build_stacks(size)
    magog_list = [stack_to_magog(s) for s in stack_list]
    kagog_list = [stack_to_kagog(s) for s in stack_list]

    lines = util.get_tex_header()

    for idx in range(len(stack_list)):
        lines.append('\\subsection*{Count ' + str(idx) + '}')
        lines.append(util.to_tex_ytableau(stack_list[idx]))
        lines.append('\\quad')
        lines.append(util.to_tex_ytableau(magog_list[idx]))
        lines.append('\\quad')
        lines.append(util.to_tex_ytableau(kagog_list[idx]))
        lines.append('\\quad')
        lines.append('')

    lines = lines + util.get_tex_footer()

    file_name = '/Users/abeverid/PycharmProjects/asm/data/sst/sst-magog-kagog' + str(size) + '.tex'

    file = open(file_name, 'w')

    for line in lines:
        file.write(line)
        file.write('\n')

    file.close()

if __name__ == '__main__':
    size = 3
    stack_list = build_stacks(size)

    #for idx in range(len(stack_list)):
        #print(util.to_tex_ytableau(s))


    print(stack_list)