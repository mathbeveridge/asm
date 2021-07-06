import nine.sandwich as sw

class SchroderPath:


    def __init__(self, sandwich_row):
        self.sandwich_row = sandwich_row
        self.hdv = sw.sandwich_to_hdv(sandwich_row)
        self.path = sw.sandwich_to_path(sandwich_row)
        self.pattern_map = sw.pattern_map_for_hdv(self.hdv)

    def init_pattern_map(self):
        pattern_map = dict()
        pattern_list = ['HH', 'HD', 'HV', 'DH', 'DD', 'DV', 'VH', 'VD', 'VV']

        for p in pattern_list:
            plist =  [char for char in p]
            pattern_map[p] = sw.has_hdv_pattern(self.hdv, plist)

        return pattern_map


    def __str__(self):
        return str(self.sandwich_row)

    def get_size(self):
        return len(self.sandwich_row)

    def get_sandwich_row(self):
        return self.sandwich_row

    def get_hdv(self):
        return self.hdv

    def get_path(self):
        return self.path

    def get_pattern_map(self):
        return self.pattern_map

    def has_pattern(self, pattern):
        return self.pattern_map[pattern]


#vec = [5, 4, 1, 0, 0]
#sp = SchroderPath(vec)
#print(sp.pattern_map)