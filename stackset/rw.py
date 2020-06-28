import random as random

# curious about whether we can  generate gogs

def step(i,j,k):
    r = random.random()

    if i == 1 and j == 1:
        if (k == 0):
            if r < 1/4:
                ret_val = (1,1,0)
            elif r < 2/4:
                ret_val = (1,1,1)
            elif r < 3/4:
                ret_val = (1,2,0)
            else:
                ret_val = (2,1,0)
        else:
            # k == 1
            if r < 1/3:
                ret_val = (1,1,1)
            #elif r < 2/4:
            #    ret_val = (1,1,1)
            elif r < 2/3:
                ret_val = (1,2,1)
            else:
                ret_val = (2,1,1)

    elif i == 1 and j == 2:
        if k == 0:
            if r < 1/3:
                ret_val = (1,2,0)
            elif r < 2/3:
                ret_val = (1,2,1)
            else:
                ret_val = (1,2,2)
        elif k == 1:
            if r < 1/2:
                ret_val = (1, 2, 1)
            else:
                ret_val = (1, 2, 2)
        else:
            ret_val = (1,2,2)
    else:
        # must be at (2,1,k)
        if k == 0:
            if r < 1/2:
                ret_val = (2,1,0)
            else:
                ret_val = (2,1,1)
        else:
            ret_val = (2,1,1)

    return ret_val



def step_height_reset(i,j,k):
    r = random.random()

    if i == 1 and j == 1:
        if r < 1/4:
            ret_val = (1,1,0)
        elif r < 2/4:
            ret_val = (1,1,1)
        elif r < 3/4:
            ret_val = (1,2,0)
        else:
            ret_val = (2,1,0)

    elif i == 1 and j == 2:

        if r < 1/3:
            ret_val = (1,2,0)
        elif r < 2/3:
            ret_val = (1,2,1)
        else:
            ret_val = (1,2,2)

    else:
        # must be at (2,1,k)
        if r < 1/2:
            ret_val = (2,1,0)
        else:
            ret_val = (2,1,1)


    return ret_val




results = dict()
results[(1, 2, 0)] = 0
results[(1, 2, 1)] = 0
results[(1, 2, 2)] = 0
results[(2, 1, 0)] = 0
results[(2, 1, 1)] = 0


for i in range(10000):
    s = (1, 1, 0)
    while (s not in results):
        s = step(s[0], s[1], s[2])

    s = step(s[0], s[1], s[2])
    results[s] = results[s] + 1

total = 0
for key in results:
    total = total + results[key]

for key in results:
    print(key, results[key]/total)
