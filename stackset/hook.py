class Hook:

    # A hook has one zero at the corner. The rest is ones
    def __init__(self, upper_left, lower_right):
        self.upper_left = upper_left
        self.lower_right = lower_right
        self.hooks_below = set([])
        self.hooks_above = set([])

    def update_comparison(self, other_hook):
        x = [self.upper_left, self.lower_right]
        y = [other_hook.upper_left, other_hook.lower_right]

        #print('>>>>> update_comparison', x, y)

        check = self.check_nested(x,y)

        #print('\tcheck nested=', check)

        if x[0][0] < y[0][0] and x[0][1] < y[0][1] and x[1][0] > y[1][0] and x[1][1] > y[1][1]:
            self.hooks_above.add(other_hook)
            other_hook.hooks_below.add(self)
            print('\tcomparable', x, 'and ', y, 'with check 1=', check)
            if (not check == 1):
                print('\tPROBLEM did not expect x nesting y', x, y)
            return True
        elif x[0][0] > y[0][0] and x[0][1] > y[0][1] and x[1][0] < y[1][0] and x[1][1] < y[1][1]:
            self.hooks_below.add(other_hook)
            other_hook.hooks_above.add(self)
            if (not check == -1):
                print('\tPROBLEM did not expect x nested in y', x, y)
            return True
        else:
            if (not check == 0):
                print('\tPROBLEM did not expect unnested', x, y)
            return False

    def is_minimal(self):
        return len(self.hooks_below) == 0

    def has_hooks_above(self):
        return len(self.hooks_above) > 0

    # NOTE: this only works for MINIMAL hooks (with nothing below!)
    def get_num_directly_above(self):
        count = 0
        for h in self.hooks_above:
            if len(h.hooks_below) == 1:
                count = count + 1

        return count

    def toString(self):
        return 'hook' + str(self.upper_left) + str(self.lower_right)

    def check_nested(self, ell1, ell2):
        x = ell1
        y = ell2

        if x[0][0] < y[0][0] and x[0][1] < y[0][1] and x[1][0] > y[1][0] and x[1][1] > y[1][1]:
            return 1
        elif x[0][0] > y[0][0] and x[0][1] > y[0][1] and x[1][0] < y[1][0] and x[1][1] < y[1][1]:
            return -1
        else:
            return 0