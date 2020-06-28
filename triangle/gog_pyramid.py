import triangle.gog_magog as gog_magog

class GogPyramid:

    def __init__(self, gog_triangle):
        self.gog = self.convert_gog(gog_triangle)
        self.size = len(self.gog)
        self.pyramid = self.init_pyramid()

    # xxxab pay attention to this!
    # switch indexing once up front to fit with legacy code
    def convert_gog(self, gog_triangle):
        ret_val = []
        for i in range(len(gog_triangle)):
            row = [ gog_triangle[j][i-j] for j in reversed(range(i+1))]
            ret_val.append(row)
        return ret_val

    def zero_triangle(self, k):
        ret_val = []
        for i in range(1,k+1):
            ret_val.append([0]*i)
        return ret_val

    def zero_pyramid(self):
        ret_val = []
        for k in range(self.size,0,-1):
            ret_val.append(self.zero_triangle(k))
        return ret_val


    def init_pyramid(self):
        pyr = self.zero_pyramid()
        #print('zero pyr', pyr)
        for i in range(self.size):
            #print('i=', i)
            for j in range(i+1):
                for k in range(self.size-i):
                    #print('i,j,k', i,j,k, "gog[i][j]", self.gog[i][j])
                    if self.gog[i][j] > k:
                        pyr[k][i][j]=1
        return pyr

    # pushes cubes down columns as far as possible.
    # this leaves home empty boxes, violating gravity
    # inspired by Ian's permutation pyramids
    def explode_columns(self):
        layers = self.get_layers_z()
        for idx,layer in enumerate(layers):
            print('layer', idx, layer)
            layer_size = len(layer)
            num_ones = [0] * layer_size
            for row in layer:
                for idx2, x in enumerate(row):
                    #print('num_ones', num_ones, 'x', x)
                    num_ones[idx2] = num_ones[idx2] + x

            print('num ones final', num_ones)

            for idx3 in range(layer_size):
                col_size = layer_size - idx3
                print('====================')
                for idx4 in range(idx3, layer_size):
                    #print('idx4, col_size', idx4, col_size)
                    print('k i j =', idx, idx4, idx3, 'col_size', col_size)
                    start_idx = col_size - num_ones[idx3] + idx3
                    print('\tcomparing', idx4, start_idx)
                    if idx4 < start_idx:
                        print('\tsetting to', 0)
                        self.pyramid[idx][idx4][idx3] = 0
                    else:
                        print('\tsetting to', 1)
                        self.pyramid[idx][idx4][idx3] = 1




    def print_gog(self):
        print('---gog--')
        for g in self.gog:

            print(g)
        print('---gog--')

    def print_layers_z(self):
        print('---z layers--')
        for x in self.get_layers_z():
            for y in x:
                print(y)
            print('--')
        print('---z layers--')


    def print_layers_x(self):
        print('---x layers--')
        for x in self.get_layers_x():
            print(x)
        print('---x layers--')


    def print_layers_y(self):
        print('---y layers--')
        for x in self.get_layers_y():
            print(x)
        print('---y layers--')

    def get_layers_z(self):
        ret_val = []
        for layer in self.pyramid:
            temp = []
            for row in layer:
                temp.append(row)
            ret_val.append(temp)
        return ret_val

    def get_layers_x(self):
        ret_val = []
        for idx in range(self.size):
            temp = self.get_layer_x(idx)
            ret_val.append(temp)
        return ret_val

    def get_layer_x(self, idx):
        ret_val = []
        for j in range(0, idx+1):
            tower = [ self.pyramid[k][idx][j] for k in range(self.size-idx)]
            ret_val.append(tower)
        return ret_val

    def get_layers_y(self):
        ret_val = []
        for idx in range(self.size):
            temp = self.get_layer_y(idx)
            ret_val.append(temp)
        return ret_val


    def get_layer_y(self, idx):
        ret_val = []
        for i in range(idx, self.size):
            tower = [ self.pyramid[k][i][idx] for k in range(self.size-i)]
            ret_val.append(tower)
        return ret_val