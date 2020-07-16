class Hook:

    # A hook has one zero at the corner. The rest is ones
    def __init__(self, upper_left, lower_right, num_zeros):
        self.upper_left = upper_left
        self.lower_right = lower_right
        self.num_zeros = num_zeros
        self.hooks_below = set([])
        self.hooks_above = set([])

    def update_comparison(self, other_hook):
        x = [self.upper_left, self.lower_right]
        y = [other_hook.upper_left, other_hook.lower_right]

        #print('>>>>> update_comparison', x, y)


        # First check if nested. Then check if hook zeros overlap.
        if x[0][0] < y[0][0] and x[0][1] < y[0][1] and x[1][0] > y[1][0] and x[1][1] > y[1][1]:
            #if self.upper_left[1] + self.num_zeros - 1 < other_hook.upper_left[1]:
            if self.upper_left[1] + self.num_zeros > other_hook.upper_left[1]:
                self.hooks_above.add(other_hook)
                other_hook.hooks_below.add(self)
                return True
            else:
                return False
        elif x[0][0] > y[0][0] and x[0][1] > y[0][1] and x[1][0] < y[1][0] and x[1][1] < y[1][1]:
            #if other_hook.upper_left[1] + other_hook.num_zeros - 1 < self.upper_left[1]:
            if other_hook.upper_left[1] + other_hook.num_zeros  > self.upper_left[1]:
                self.hooks_below.add(other_hook)
                other_hook.hooks_above.add(self)
                return True
            else:
                return False
        else:
            return False

    def is_minimal(self):
        return len(self.hooks_below) == 0

    def has_hooks_above(self):
        return len(self.hooks_above) > 0

    # NOTE: this only works for MINIMAL hooks (with nothing below!)
    # MUST COME BACK AND MAKE THIS POSET IMPLEMENTATION BETTER!!!
    def get_num_directly_above(self):
        count = 0
        for h in self.hooks_above:
            intersect = self.hooks_above.intersection(h.hooks_below)

            if len(intersect) == 0:
                count = count + 1

        print('num directly above', count)

        return count


    def get_height_above(self):
        height = 0
        current_hooks_above = self.hooks_above.copy()
        current_hooks_below = self.hooks_below.copy()

        current_hooks_below.add(self)

        # add any incomparables to self to current_hooks_below
        for h in self.hooks_above:
            for hh in h.hooks_below:
                if hh not in current_hooks_below and hh not in self.hooks_above:
                      current_hooks_below.add(hh)

        #print('levels of', self.toString())

        while len(current_hooks_above) > 0:
            height = height + 1
            current_level = set()

            for h in current_hooks_above:
                if h.hooks_below.issubset(current_hooks_below):
                    current_level.add(h)

            # update the whole level at once
            #print('\tlevel ', height)
            for current_hook in current_level:
                current_hooks_below.add(current_hook)
                current_hooks_above.remove(current_hook)
                #print('\t\t',  current_hook.toString())


            print('height is', height)
        return height


    def toString(self):
        return 'hook'.join([ str(self.upper_left) , str(self.lower_right) , str(self.num_zeros) ])

    def check_nested(self, ell1, ell2):
        x = ell1
        y = ell2

        if x[0][0] < y[0][0] and x[0][1] < y[0][1] and x[1][0] > y[1][0] and x[1][1] > y[1][1]:
            return 1
        elif x[0][0] > y[0][0] and x[0][1] > y[0][1] and x[1][0] < y[1][0] and x[1][1] < y[1][1]:
            return -1
        else:
            return 0