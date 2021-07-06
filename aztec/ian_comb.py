import triangle.build_ballot_triangle as bbt
import triangle.build_tss as btss
import triangle.array_util as util

import mysql.connector

import ast


# attempt to comb from tss to ballot triangles

# got this working for n=4

bad5_list =  [[[2, 2, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [0, 0], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [0, 0], [0]], [[3, 3, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [0, 0], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [0, 0], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [0, 0], [0]], [[3, 3, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [0, 0], [0]], [[3, 3, 2, 2, 1], [2, 1, 1, 0], [1, 0, 0], [0, 0], [0]], [[3, 3, 2, 2, 1], [2, 1, 1, 1], [1, 0, 0], [0, 0], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 0], [0, 0], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 0], [0, 0], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 1], [0, 0], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 1], [0, 0], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 0], [0, 0], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 0], [0, 0], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 1], [0, 0], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 1], [0, 0], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 2, 1], [0, 0], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 2, 1], [0, 0], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [3, 2, 1], [0, 0], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [3, 2, 1], [0, 0], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [1, 0], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [1, 0], [0]], [[3, 3, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [1, 0], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [1, 0], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [1, 0], [0]], [[3, 3, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [1, 0], [0]], [[3, 3, 2, 2, 1], [2, 1, 1, 0], [1, 0, 0], [1, 0], [0]], [[3, 3, 2, 2, 1], [2, 1, 1, 1], [1, 0, 0], [1, 0], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 0], [1, 0], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 0], [1, 0], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 1], [1, 0], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 1], [1, 0], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 0], [1, 0], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 0], [1, 0], [0]], [[4, 3, 2, 1, 0], [2, 2, 2, 1], [2, 1, 0], [1, 0], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 1], [1, 0], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 1], [1, 0], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 2, 1], [1, 0], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 2, 1], [1, 0], [0]], [[4, 3, 2, 1, 0], [2, 2, 2, 1], [2, 2, 1], [1, 0], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [3, 2, 1], [1, 0], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [3, 2, 1], [1, 0], [0]], [[4, 3, 2, 1, 0], [2, 2, 2, 1], [3, 2, 1], [1, 0], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [1, 1], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [1, 1], [0]], [[3, 3, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [1, 1], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [1, 1], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [1, 1], [0]], [[3, 3, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [1, 1], [0]], [[3, 3, 2, 2, 1], [2, 1, 1, 0], [1, 0, 0], [1, 1], [0]], [[3, 3, 2, 2, 1], [2, 1, 1, 1], [1, 0, 0], [1, 1], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 0], [1, 1], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 0], [1, 1], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 1], [1, 1], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 1], [1, 1], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 0], [1, 1], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 0], [1, 1], [0]], [[4, 3, 2, 1, 0], [2, 2, 2, 1], [2, 1, 0], [1, 1], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 1], [1, 1], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 1], [1, 1], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 2, 1], [1, 1], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 2, 1], [1, 1], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [3, 2, 1], [1, 1], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [3, 2, 1], [1, 1], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [2, 1], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [2, 1], [0]], [[3, 3, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [2, 1], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [2, 1], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [2, 1], [0]], [[3, 3, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [2, 1], [0]], [[3, 3, 2, 2, 1], [2, 1, 1, 0], [1, 0, 0], [2, 1], [0]], [[3, 3, 2, 2, 1], [2, 1, 1, 1], [1, 0, 0], [2, 1], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 0], [2, 1], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 0], [2, 1], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 1], [2, 1], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 1], [2, 1], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 0], [2, 1], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 0], [2, 1], [0]], [[4, 3, 2, 1, 0], [2, 2, 2, 1], [2, 1, 0], [2, 1], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 1], [2, 1], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 1], [2, 1], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 2, 1], [2, 1], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 2, 1], [2, 1], [0]], [[4, 3, 2, 1, 0], [2, 2, 2, 1], [2, 2, 1], [2, 1], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [3, 2, 1], [2, 1], [0]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [3, 2, 1], [2, 1], [0]], [[4, 3, 2, 1, 0], [2, 2, 2, 1], [3, 2, 1], [2, 1], [0]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [0, 0], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [0, 0], [1]], [[3, 3, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [0, 0], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [0, 0], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [0, 0], [1]], [[3, 3, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [0, 0], [1]], [[3, 3, 2, 2, 1], [2, 1, 1, 0], [1, 0, 0], [0, 0], [1]], [[3, 3, 2, 2, 1], [2, 1, 1, 1], [1, 0, 0], [0, 0], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 0], [0, 0], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 0], [0, 0], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 1], [0, 0], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 1], [0, 0], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 0], [0, 0], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 0], [0, 0], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 1], [0, 0], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 1], [0, 0], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 2, 1], [0, 0], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 2, 1], [0, 0], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [3, 2, 1], [0, 0], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [3, 2, 1], [0, 0], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [1, 0], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [1, 0], [1]], [[3, 3, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [1, 0], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [1, 0], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [1, 0], [1]], [[3, 3, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [1, 0], [1]], [[3, 3, 2, 2, 1], [2, 1, 1, 0], [1, 0, 0], [1, 0], [1]], [[3, 3, 2, 2, 1], [2, 1, 1, 1], [1, 0, 0], [1, 0], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 0], [1, 0], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 0], [1, 0], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 1], [1, 0], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 1], [1, 0], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 0], [1, 0], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 0], [1, 0], [1]], [[4, 3, 2, 1, 0], [2, 2, 2, 1], [2, 1, 0], [1, 0], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 1], [1, 0], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 1], [1, 0], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 2, 1], [1, 0], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 2, 1], [1, 0], [1]], [[4, 3, 2, 1, 0], [2, 2, 2, 1], [2, 2, 1], [1, 0], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [3, 2, 1], [1, 0], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [3, 2, 1], [1, 0], [1]], [[4, 3, 2, 1, 0], [2, 2, 2, 1], [3, 2, 1], [1, 0], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [1, 1], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [1, 1], [1]], [[3, 3, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [1, 1], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [1, 1], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [1, 1], [1]], [[3, 3, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [1, 1], [1]], [[3, 3, 2, 2, 1], [2, 1, 1, 0], [1, 0, 0], [1, 1], [1]], [[3, 3, 2, 2, 1], [2, 1, 1, 1], [1, 0, 0], [1, 1], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 0], [1, 1], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 0], [1, 1], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 1], [1, 1], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 1], [1, 1], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 0], [1, 1], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 0], [1, 1], [1]], [[4, 3, 2, 1, 0], [2, 2, 2, 1], [2, 1, 0], [1, 1], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 1], [1, 1], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 1], [1, 1], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 2, 1], [1, 1], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 2, 1], [1, 1], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [3, 2, 1], [1, 1], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [3, 2, 1], [1, 1], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [2, 1], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [2, 1], [1]], [[3, 3, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [2, 1], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [2, 1], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [2, 1], [1]], [[3, 3, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [2, 1], [1]], [[3, 3, 2, 2, 1], [2, 1, 1, 0], [1, 0, 0], [2, 1], [1]], [[3, 3, 2, 2, 1], [2, 1, 1, 1], [1, 0, 0], [2, 1], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 0], [2, 1], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 0], [2, 1], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 1], [2, 1], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [1, 1, 1], [2, 1], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 0], [2, 1], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 0], [2, 1], [1]], [[4, 3, 2, 1, 0], [2, 2, 2, 1], [2, 1, 0], [2, 1], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 1], [2, 1], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 1, 1], [2, 1], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [2, 2, 1], [2, 1], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [2, 2, 1], [2, 1], [1]], [[2, 2, 2, 2, 1], [2, 1, 0, 0], [3, 2, 1], [2, 1], [1]], [[3, 2, 2, 2, 1], [2, 1, 0, 0], [3, 2, 1], [2, 1], [1]]]


def get_diag_sums(triangle):
    diags = []

    for i in range(len(triangle)):
        val = 0
        for j in range(i + 1):
            val += triangle[j][i - j]
        diags.append(val)

    return tuple(diags)

def add_tss_to_db(tss_list):

    tss_len =  len(tss_list)

    start_idx = 0
    batch_size = 10000

    conn = mysql.connector.connect(host='localhost', database='mysql', user='root', password='50Fl**rs')
    cur = conn.cursor(buffered=True)

    update_query = "INSERT INTO SIX_TSS (diag1, diag2, diag3, diag4, diag5, diag6, name) VALUES (%s,%s,%s,%s,%s,%s,%s)"

    while(start_idx < tss_len):
        print('\t', start_idx)
        end_idx = min(start_idx + batch_size, tss_len)

        param_list = []

        for tss in tss_list[start_idx:end_idx]:
            params = list(get_diag_sums(tss))
            params.append(str(tss))

            param_list.append(tuple(params))

        #cur.execute(update_query, (2,3,2,2,1, '[[2, 2, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [0, 0], [0]]'))
        cur.executemany(update_query, param_list)

        conn.commit()

        start_idx += batch_size


    cur.close()
    conn.close()


def add_bt_to_db(bt_list):


    bt_len =  len(bt_list)

    start_idx = 0
    batch_size = 10000

    conn = mysql.connector.connect(host='localhost', database='mysql', user='root', password='50Fl**rs')
    cur = conn.cursor(buffered=True)

    update_query = "INSERT INTO SIX_BT (diag1, diag2, diag3, diag4, diag5, diag6, name) VALUES (%s,%s,%s,%s,%s,%s,%s)"

    while(start_idx < bt_len):
        print('\t', start_idx)
        end_idx = min(start_idx + batch_size, bt_len)

        param_list = []

        for bt in bt_list[start_idx:end_idx]:
            params = list(get_diag_sums(bt))
            params.append(str(bt))

            param_list.append(tuple(params))

        #cur.execute(update_query, (2,3,2,2,1, '[[2, 2, 2, 2, 1], [2, 1, 0, 0], [0, 0, 0], [0, 0], [0]]'))
        cur.executemany(update_query, param_list)

        conn.commit()

        start_idx += batch_size


    cur.close()
    conn.close()


def load_db():
    print('doing tss')

    tss_list = btss.build_tss(6)

    print('\tto_db')
    add_tss_to_db(tss_list)

    # print('doing bt')
    #
    # bt_list = bbt.build_bt(6)
    #
    # print('\tto_db')
    # add_bt_to_db(bt_list)

def get_list_from_db(query):
    conn = mysql.connector.connect(host='localhost', database='mysql', user='root', password='50Fl**rs')
    cur = conn.cursor(buffered=True)

    cur.execute(query)
    records = cur.fetchall()

    tri_list  = [ ast.literal_eval(r[0]) for r in records]

    cur.close()
    conn.close()

    return tri_list



def comb(tss, debug=False):
    size = len(tss)

    triangle = util.clone_array(tss)

    if debug:
        prev = util.clone_array(tss)
        print("COMBING")
        util.print_array(triangle)

    for i in reversed(range(1,size)):
        print('dealing with row ', i)
        for j in range(i,size):
            print('\thandling row ', j)
            triangle = handle_row_swap(triangle, j)

            if debug and not prev == triangle:
                print('>>>>> i,j', i, j)
                util.print_array(triangle)
                prev = util.clone_array(triangle)

    # for i in range(1,size):
    #         handle_row_swap(triangle, i)
    #
    #         if debug and not prev == triangle:
    #             print('>>>>> i', i)
    #             util.print_array(triangle)
    #             prev = util.clone_array(triangle)
    #


    return triangle





##
## replace 3221 with 3200
##         200       221
##
## replace 2221 with 2000
##         100       321
##
def handle_row(triangle, row_idx):
    big_row = triangle[row_idx-1]
    small_row = triangle[row_idx]
#    print('handling rows', big_row, small_row)
    small_len = len(small_row)
    for k in range(small_len):
        # BT columns can only decrease by 1
        if big_row[k] - small_row[k] > 1:
            if k == 0 or small_row[k-1] >= big_row[k+1]:
                # swap the rest of the rows
                temp = [x for x in big_row]
                for j in range(k,small_len):
                    big_row[j+1] = small_row[j]
                    small_row[j] = temp[j+1]

            else:
                # It looks like
                # ...,   a,   a,   a,   a,  ....
                # ..., a-1, a-1, a-1, a-2, ...
                #
                # make it look like
                # ...,   a, a-2, a-2, a-2, a-2
                # ..., a+1, a+1, a+1, ...
                #
                #print('made it here')
                # hold one back
                a = big_row[k+1]
                start_idx = small_row.index(a-1)
                mid_idx = k

                temp = [x for x in big_row]

                for j in range(start_idx, mid_idx):
                    big_row[j+1] = a-2
                    small_row[j] = a+1

                for j in range(mid_idx, small_len):
                    big_row[j+1] = small_row[j]
                    small_row[j] = temp[j+1]


            # change_val = big_row[k] - small_row[k] -1
            # if k == 0 or small_row[k-1] >= small_row[k] + change_val:
            #     for j in range(k,small_len):
            #         #change = min(0, change_val - (big_row[k+1] - big_row[j]))
            #         change = change_val
            #         small_row[j] = small_row[j] + change
            #         big_row[j+1] = big_row[j+1] - change
            # else:
            #     for j in range(k-1,small_len):
            #         small_row[j] = small_row[j] + big_row[j+1]
            #         big_row[j+1] = 0
    # no need to return anything since rows are in a triangle

##
## replace 3221 with 3200
##         200       221
##
## replace 2221 with 2000
##         100       321
##
def handle_row_new(triangle, row_idx):
    size = len(triangle)
    big_row = triangle[row_idx - 1]
    small_row = triangle[row_idx]
    #print('new handling rows', big_row, small_row, 'for triangle', triangle)

    violation_list = get_violation_idx_list(big_row, small_row)

    small_size = len(small_row)

    while (len(violation_list) > 0):

        #print(violation_list)

        viol_idx = violation_list[0]

        delta = min(big_row[viol_idx] - small_row[viol_idx], big_row[viol_idx + 1])

        viol_idx = update_violation_idx(violation_list[-1], big_row, small_row, delta)

        # want to -delta if possible from big_row[viol_idx]

        delta_list = get_delta_list(big_row, small_row, viol_idx, delta)

        for k in range(viol_idx, small_size):
            big_row[k + 1] = big_row[k + 1] - delta_list[k]
            small_row[k] = small_row[k] + delta_list[k]

        violation_list = get_violation_idx_list(big_row, small_row)

    return triangle




##
## replace 3221 with 3200
##         200       221
##
## replace 2221 with 2000
##         100       321
##
def handle_row_swap(triangle, row_idx):
    size = len(triangle)
    big_row = triangle[row_idx-1]
    small_row = triangle[row_idx]
    #print('new handling rows', big_row, small_row, 'for triangle', triangle)


    # like combing, there will be multiple intervals!
    violation_list = get_violation_idx_list(big_row, small_row)

    small_size = len(small_row)

    while (len(violation_list) > 0):

        viol_idx = violation_list[0]

        if viol_idx > 0:
            small_border_diff = small_row[viol_idx-1] - small_row[viol_idx]


        # swap
        temp = [x for x in small_row]

        for k in range(viol_idx, small_size):
            small_row[k] = big_row[k+1]
            big_row[k+1] = temp[k]

        # look for forbidden increase in small_row
        if viol_idx > 0:
            new_border_diff =  small_row[viol_idx-1] - small_row[viol_idx]

            if new_border_diff < 0:
                # fix it
                diff = small_border_diff - new_border_diff
                # but stay within bounds
                diff = min(diff, small_size -  viol_idx +1 - small_row[viol_idx -1])

                for k in reversed(range(viol_idx)):
                    # but stay within bounds
                    #diff = min(diff, small_size - k - small_row[k])
                    big_row[k+1] = big_row[k+1] - diff
                    small_row[k] = small_row[k] + diff
                    if k > 0:
                        if small_row[k] <= small_row[k-1]:
                            # don't need to make more changes (I think)
                            break


        violation_list = get_violation_idx_list(big_row, small_row)


    return triangle




# this is a bijection for n=5. YAY!!!! but has problems for n=6 and triangle_6_2728
# potential solution: fixing 1,1,0,0 with a+1,a+1,a,... and 2,2,0,0 with a+1,a+1,a,... etc.
def handle_row_with_col_max_v1(triangle, row_idx, col_max_idx):
    size = len(triangle)
    big_row = triangle[row_idx-1]
    small_row = triangle[row_idx]
    small_size = len(small_row)
    #print('new handling rows', big_row, small_row, 'for triangle', triangle)

    # WARNING FOR FUTURE!!!
    # like combing, there will be multiple intervals!


    viol_idx = get_violation_idx(big_row, small_row, col_max_idx)

    if viol_idx == -1:
        return triangle

    #  possibly need to pad
    # if viol_idx > 0  then violation must look like one of
    #   a,   a,  a,       or   a,   a,  a-1
    # a-1, a-2,  x,          a-1, a-2,   x


    ##### HACK #1 ????????  wrong now
    if big_row[viol_idx] - big_row[viol_idx+1] > 1:
        # nothing can help: (just move it all down???)
        # TRYIING: move just this part since it makes a witness?
        if  viol_idx > 0:
            available = small_size - viol_idx + 1  - small_row[viol_idx-1]

            # hack??? added -1 for size 6
            #delta = min(big_row[viol_idx]-small_row[viol_idx]-1, available)
            delta = min(2, available)

            ## NEW
            small_row[viol_idx-1] = small_row[viol_idx-1] + delta
            big_row[viol_idx] = big_row[viol_idx] - delta

            #### OLD
            # for k in range(viol_idx-1,small_size):
            #     change = min(delta, big_row[k+1])
            #     small_row[k] = small_row[k] + change
            #     big_row[k+1] = big_row[k+1] - change

        else:
            # this time we move starting past the violation
            # this is inconsistent
            available = small_size - viol_idx   - small_row[viol_idx]

            delta = min(big_row[viol_idx+1], available)

            for k in range(viol_idx,small_size):
                change = min(delta, big_row[k+1])
                small_row[k] = small_row[k] + change
                big_row[k+1] = big_row[k+1] - change
    else:

        delta = 0

        if viol_idx > 0:
            # if big_row[viol_idx] == big_row[viol_idx+1]:
            #     delta = 2
            # else:
            #     delta = 0
            if small_row[viol_idx-1] < big_row[viol_idx+1]:
                # need to move more  to keep row weakly decreasing
                diff = small_row[viol_idx-1] - small_row[viol_idx]
                # MEGA HACK!!!!
                if diff == 2:
                    diff = 1
                delta = diff + big_row[viol_idx+1] - small_row[viol_idx-1]

                #### HACK # 2
                #available_list = [ small_size - k -  small_row[k] for k in range(viol_idx)]
                #available = min(available_list)
                #delta = min(delta, available)



        # swap
        temp = [x for x in small_row]

        for k in range(viol_idx, small_size):
            small_row[k] = big_row[k + 1]
            big_row[k + 1] = temp[k]

        if delta > 0:
            for k in reversed(range(viol_idx)):
                # HACK #2a. I worry about not taking a consistent amount
                available = small_size - k -  small_row[k]
                delta = min(delta, available)

                if delta == 1:
                    # confirm that we have a witness??? HACK!!!
                    if big_row[viol_idx] -  big_row[viol_idx+1] < 2:
                        delta = 0
                small_row[k] = small_row[k] + delta
                big_row[k+1] = big_row[k+1] - delta

    return triangle



def handle_row_with_col_max(triangle, row_idx, col_max_idx):
    size = len(triangle)
    big_row = triangle[row_idx-1]
    small_row = triangle[row_idx]
    small_size = len(small_row)
    #print('new handling rows', big_row, small_row, 'for triangle', triangle)

    # WARNING FOR FUTURE!!!
    # like combing, there will be multiple intervals!


    viol_idx = get_violation_idx(big_row, small_row, col_max_idx)

    if viol_idx == -1:
        return triangle

    #  possibly need to pad
    # if viol_idx > 0  then violation must look like one of
    #   a,   a,  a,       or   a,   a,  a-1
    # a-1, a-2,  x,          a-1, a-2,   x


    ##### HACK #1 ????????  wrong now
    if big_row[viol_idx] - big_row[viol_idx+1] > 1:
        # nothing can help: (just move it all down???)
        # TRYING: move just this part since it makes a witness?
        if  viol_idx > 0:
            available = small_size - viol_idx + 1  - small_row[viol_idx-1]

            # hack??? added -1 for size 6
            #delta = min(big_row[viol_idx]-small_row[viol_idx]-1, available)
            delta = min(2, available)

            ## NEW
            small_row[viol_idx-1] = small_row[viol_idx-1] + delta
            big_row[viol_idx] = big_row[viol_idx] - delta

            ## HACK for triangle_6_2728
            ## very bad: changing 3 rows!
            if big_row[viol_idx] - small_row[viol_idx] > 1:
                d = big_row[viol_idx] - small_row[viol_idx] - 1
                big_row[viol_idx] = big_row[viol_idx] - d
                bigger_row = triangle[row_idx - 2]
                bigger_row[viol_idx+1] = bigger_row[viol_idx+1] + d


            #### OLD
            # for k in range(viol_idx-1,small_size):
            #     change = min(delta, big_row[k+1])
            #     small_row[k] = small_row[k] + change
            #     big_row[k+1] = big_row[k+1] - change

        else:
            # this time we move starting past the violation
            # this is inconsistent
            available = small_size - viol_idx   - small_row[viol_idx]

            delta = min(big_row[viol_idx+1], available)

            for k in range(viol_idx,small_size):
                change = min(delta, big_row[k+1])
                small_row[k] = small_row[k] + change
                big_row[k+1] = big_row[k+1] - change
    else:

        delta = 0

        if viol_idx > 0:
            # if big_row[viol_idx] == big_row[viol_idx+1]:
            #     delta = 2
            # else:
            #     delta = 0
            if small_row[viol_idx-1] < big_row[viol_idx+1]:
                # need to move more  to keep row weakly decreasing
                diff = small_row[viol_idx-1] - small_row[viol_idx]
                # MEGA HACK!!!!
                if diff == 2:
                    diff = 1
                delta = diff + big_row[viol_idx+1] - small_row[viol_idx-1]

                #### HACK # 2
                #available_list = [ small_size - k -  small_row[k] for k in range(viol_idx)]
                #available = min(available_list)
                #delta = min(delta, available)
            #elif small_row[viol_idx-1] == big_row[viol_idx+1]:
            #    #### ANOTHER SERIOUS HACK-- trying to get 6 to work
            #    if small_row[viol_idx-1] - small_row[viol_idx] > 1 and big_row[viol_idx] > small_row[viol_idx-1]:
            #        delta = 1


        # swap
        temp = [x for x in small_row]

        for k in range(viol_idx, small_size):
            small_row[k] = big_row[k + 1]
            big_row[k + 1] = temp[k]

        if delta > 0:


            #  hack to fix triangle_6_2728
            #  BUT THIS DOESN'T WORK for triangle triangle_6_1080
            # before_viol_delta = min(delta, small_size - viol_idx +1 -  small_row[viol_idx-1])
            # if before_viol_delta < delta:
            #     d = delta - before_viol_delta
            #     small_row[viol_idx] = small_row[viol_idx] - d
            #     big_row[viol_idx+1] = big_row[viol_idx+1] + d

            for k in reversed(range(viol_idx)):
                # HACK #2a. I worry about not taking a consistent amount
                available = small_size - k -  small_row[k]
                delta = min(delta, available)

                if delta == 1:
                    # confirm that we have a witness??? HACK!!!
                    if big_row[viol_idx] -  big_row[viol_idx+1] < 2:
                        delta = 0
                small_row[k] = small_row[k] + delta
                big_row[k+1] = big_row[k+1] - delta

    return triangle


def comb_with_col_max(tss, debug=False):
    size = len(tss)

    triangle = util.clone_array(tss)

    if debug:
        prev = util.clone_array(tss)
        print("COMBING with col max")
        util.print_array(triangle)

    for col_max in range(1,size+1):
        if debug:
            print('dealing with col_max ', col_max)
        for j in range(1,size):
            if debug:
                print('\thandling row ', j)
            triangle = handle_row_with_col_max(triangle, j, col_max)

            if debug and not prev == triangle:
                print('>>>>> col_max,j', col_max, j)
                util.print_array(triangle)
                prev = util.clone_array(triangle)

    # for i in range(1,size):
    #         handle_row_swap(triangle, i)
    #
    #         if debug and not prev == triangle:
    #             print('>>>>> i', i)
    #             util.print_array(triangle)
    #             prev = util.clone_array(triangle)
    #

    # final time needed?
    if debug:
        print('one more time')
    for j in reversed(range(1,size)):
        if debug:
            print('\thandling row ', j)
        triangle = handle_row_with_col_max(triangle, j, col_max)

        if debug and not prev == triangle:
            print('>>>>> col_max,j', col_max, j)
            util.print_array(triangle)
            prev = util.clone_array(triangle)

    return triangle


# want to move delta, but can take at most what is in big and
# what can fit in small
def get_delta_list(big_row, small_row, viol_idx, delta):


    small_size = len(small_row)
    small_avail = [small_size - small_row[i] for i in range(small_size)]

    delta_vec = [0,] * viol_idx

    for k in range(viol_idx, small_size):
        delta_vec.append(min(delta, big_row[k+1], small_avail[k]))

    return delta_vec



def get_violation_idx(big_row, small_row, max_col_idx):
    viol_list = get_violation_idx_list(big_row, small_row)
    if len(viol_list) == 0:
        return -1
    elif viol_list[0] < max_col_idx:
        return viol_list[0]
    else:
        return -1


def get_violation_idx_list(big_row, small_row):
    small_size = len(small_row)
    ret_val =  [k for k in range(small_size) if big_row[k] - small_row[k] > 1]
    return ret_val


def update_violation_idx(viol_idx, big_row, small_row, delta):
    # want to -2 from big_row[viol_idx] but this could cause a problem
    # example:
    # 22221 to 22000
    # 2100     2321
    # so instead:
    # 20000
    # 4321

    while(viol_idx > 0 and small_row[viol_idx-1] < small_row[viol_idx] + delta):
        viol_idx += -1

    return viol_idx


temp = [[2,2,2,1],[1,0,0]]

#print(temp)
#handle_row(temp,1)
#print(temp)



combed_map = dict()

##############
def compare(size):

    # rows decr by at most 1
    tss_list = btss.build_tss(size)

    # row weak decr
    # col weak incr or decr by 1
    bt_list = bbt.build_bt(size)

    combed_list = []
    combed_str_set = set()

    fail_list = []

    print('total', len(tss_list))

    #tss_list = tss_list[0:1000]

    print('========= TSS')
    for count,tss in enumerate(tss_list):

        if count % 1000 == 0:
            print(count)
        #print('handling TSS')
        #util.print_array(tss)
        #tri = comb(tss, True)
        tri = comb_with_col_max(tss, False)

        #tri = comb(tri)
        #tri = comb(tri)
        combed_list.append(tri)
        combed_str_set.add(str(tri))
        #util.print_array(tri)
        #print('=================')
        if not tri in bt_list:
            fail_list.append([tss, tri])
            print('fail', count, tss, '\t', tri)

        combed_key = str(tri)
        if not combed_key in combed_map:
            combed_map[combed_key] = [tss,]
        else:
            combed_map[combed_key].append(tss)


    missing_list = []
    # # print('========= BT')
    for bt in bt_list:
        if not bt in combed_list:
            missing_list.append(bt)
    # #     util.print_array(bt)


    for f in fail_list:
        util.print_array(f[0])
        util.print_array(f[1])
        print('************')
    print('num failures', len(fail_list))

    # t = [[2, 2, 1], [0, 0], [0]]
    #
    # util.print_array(t)
    # util.print_array(comb(t))
    #
    print('MISSING')

    missing_file = open('/Users/abeverid/PycharmProjects/asm/data/tss/missing_bt.txt', 'w')
    for b in missing_list:
        missing_file.write(str(b))
        missing_file.write('\n')
    missing_file.close()
    #   util.print_array(b)
    print('num missing:', len(missing_list))


    print('combed tri size', len(combed_list))
    print('combed str size', len(combed_str_set))



    bad_list = [ x[0] for  x in fail_list]

    print(bad_list)

    print('repeats!!!!')
    rep_count = 0

    repeat_tss_file = open('/Users/abeverid/PycharmProjects/asm/data/tss/repeat_tss.txt', 'w')
    repeat_bt_file = open('/Users/abeverid/PycharmProjects/asm/data/tss/repeat_bt.txt', 'w')

    for key in combed_map:
        if len(combed_map[key]) > 1:
            print(key, len(combed_map[key]), combed_map[key])
            rep_count +=1

            repeat_bt_file.write(key)
            repeat_bt_file.write('\n')
            rep_list = combed_map[key]
            for rep in rep_list:
                repeat_tss_file.write(str(rep))
                repeat_tss_file.write('\n')

    repeat_tss_file.close()
    repeat_bt_file.close()

    print('repcount', rep_count)





def ponder_bad():
    tri = bad5_list[10]

    print('START')
    util.print_array(tri)

    combed = comb(tri)

    print('END')
    util.print_array(combed)

    print(len(bad5_list))



    print('hello')
    bad_map = dict()

    for bad in bad5_list:
        #print(bad)
        key = get_diag_sums(bad)
        if not str(key) in bad_map:
            bad_map[str(key)] = []

        bad_map[str(key)].append(bad)

    for key in bad_map:
        print(key, len(bad_map[key]))

    print('here are the baddies')
    for x in  bad_map['[2, 4, 3, 2, 1]']:
        print('BAD ==========')
        util.print_array(x)
        util.print_array(comb(x))


def sort_missing_repeats():
    missing_bt_file = open('/Users/abeverid/PycharmProjects/asm/data/tss/missing_bt.txt', 'r')
    missing_bt_list = []
    for line in missing_bt_file.readlines():
        line = line.strip()
        missing_bt_list.append(ast.literal_eval(line))

    repeat_tss_file = open('/Users/abeverid/PycharmProjects/asm/data/tss/repeat_tss.txt', 'r')
    repeat_tss_list = []
    for line in repeat_tss_file.readlines():
        line = line.strip()
        repeat_tss_list.append(ast.literal_eval(line))


    repeat_bt_file = open('/Users/abeverid/PycharmProjects/asm/data/tss/repeat_bt.txt', 'r')
    repeat_bt_list = []
    for line in repeat_bt_file.readlines():
        line = line.strip()
        repeat_bt_list.append(ast.literal_eval(line))

    for repeat in repeat_bt_list:
        util.print_array(repeat)


    missing_bt_map = dict()
    for missing in missing_bt_list:
        key = get_diag_sums(missing)

        if not key in missing_bt_map:
            missing_bt_map[key] = [ missing,]
        else:
            missing_bt_map[key].append(missing)

    repeat_bt_map = dict()
    for rep in repeat_bt_list:
        key = get_diag_sums(rep)

        if not key in repeat_bt_map:
            repeat_bt_map[key] = [rep, ]
        else:
            repeat_bt_map[key].append(rep)

    repeat_tss_map = dict()
    for rep in repeat_tss_list:
        key = get_diag_sums(rep)

        if not key in repeat_tss_map:
            repeat_tss_map[key] = [rep, ]
        else:
            repeat_tss_map[key].append(rep)

    print('************************************')
    for key in missing_bt_map:
        print(key)

        print('\tmissing ballot')
        miss_list = missing_bt_map[key]
        for m in miss_list:
            print('\t\t',  m)

        print('\trepeated ballot')
        rep_list = repeat_bt_map[key]
        for m in rep_list:
            print('\t\t',  m)

        print('\ttss that clash ')
        rep_list = repeat_tss_map[key]
        for m in rep_list:
            print('\t\t',  m)

def check_diagonal_sum():
    q_tss = 'SELECT name FROM SIX_TSS WHERE diag1=4 and diag2=5 and diag3=5 and diag4=3 and diag5=1 and diag6=1'
    q_bt = 'SELECT name FROM SIX_BT WHERE diag1=4 and diag2=5 and diag3=5 and diag4=3 and diag5=1 and diag6=1'

    tss_list = get_list_from_db(q_tss)
    bt_list = get_list_from_db(q_bt)
    combed_list = []

    print('combing TSS')
    for t in tss_list:
        combed = comb_with_col_max(t)
        if not combed in bt_list:
            print('fail:', t, combed)
        elif combed in combed_list:
            print('repeat:', t, combed)
        else:
            combed_list.append(combed)
            print('passed!')

    print('missing BT')
    for t in bt_list:
        if not t in combed_list:
            print(t)


# x = bad5_list[0]
# util.print_array(x)
# util.print_array(comb(x, True))


# tss_list = btss.build_tss(5)
# bt_list = bbt.build_bt(5)
#
# tss_list = [ tss for tss in tss_list if get_diag_sums(tss) == [2, 4, 3, 2, 1]]
# bt_list = [ bt for bt in bt_list if get_diag_sums(bt) == [2, 4, 3, 2, 1]]
#
# comb_list = [comb(tss) for tss in tss_list]
#
# for bt in bt_list:
#     if not bt in comb_list:
#         util.print_array(bt)





#util.print_array(bad5_list[0])

#util.print_array(comb(bad5_list[0], True))


triangle1 = [[2,2,2,1,0], [1,0,0,0], [0,0,0], [0,0], [0,]]
triangle2 = [[2,2,2,1,1], [1,0,0,0], [0,0,0], [0,0], [0,]]
triangle3 = [[2,2,2,2,1], [1,0,0,0], [0,0,0], [0,0], [0,]]
triangle4 = [[2,2,2,2,1], [1,1,0,0], [0,0,0], [0,0], [0,]]
triangle5 = [[2,2,2,2,1], [2,1,0,0], [0,0,0], [0,0], [0,]]
triangle6 = [[3,2,2,2,1], [2,1,0,0], [0,0,0], [0,0], [0,]]
triangle7 = [[3,3,3,2,1], [2,1,0,0], [0,0,0], [0,0], [0,]]
triangle8 = [[3,3,3,2,1], [2,1,1,0], [0,0,0], [0,0], [0,]]
triangle9 = [[3,3,3,2,1], [2,1,1,1], [0,0,0], [0,0], [0,]]


triangle_3a = [[2,2,1],[1,0],[0]]
triangle_3b = [[2,1,0],[2,1],[0]]

triangle_3c = [[3,1,0],[0,0],[0]]


triangle_5a = [[3, 1, 0, 0, 0], [4, 3, 2, 1], [1, 0, 0], [0, 0], [0]]
triangle_5b = [[3, 3, 3, 2, 1], [2, 1, 0, 0], [0, 0, 0], [0, 0], [0]]
triangle_5c = [[3, 3, 3, 2, 1], [2, 0, 0, 0], [1, 0, 0], [0, 0], [0]]
triangle_5d = [[2, 2, 2, 2, 1], [3, 2, 1, 0], [1, 0, 0], [0, 0], [0]]
triangle_5e = [[2, 2, 2, 2, 1], [3, 1, 0, 0], [2, 0, 0], [1, 0], [0]]
triangle_5f = [[2, 2, 2, 2, 1], [4, 1, 0, 0], [3, 0, 0], [2, 0], [1]]
triangle_5g = [[4, 3, 2, 1, 0], [2, 2, 2, 1], [1, 1, 0], [0, 0], [0]]



triangle_6_419 = [[3, 3, 2, 2, 1, 0], [2, 1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0], [0, 0], [0]]
triangle_6_422 = [[3, 3, 3, 2, 1, 0], [2, 1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0], [0, 0], [0]]
triangle_6_2728 = [[3, 3, 3, 2, 2, 1], [2, 2, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0], [0, 0], [0]]
triangle_6_2922 = [[4, 3, 2, 1, 0, 0], [2, 2, 2, 1, 0], [1, 0, 0, 0], [0, 0, 0], [0, 0], [0]]
triangle_6_1080 = [[4, 4, 4, 3, 2, 1], [3, 2, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0], [0, 0], [0]]
triangle_6_2922 = [[4, 3, 2, 1, 0, 0], [2, 2, 2, 1, 0], [1, 0, 0, 0], [0, 0, 0], [0, 0], [0]]


t6a = [[3, 3, 3, 2, 2, 1], [2, 2, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0], [0, 0], [0]]

triangle = t6a

#triangle = [[3, 3, 2, 1], [2, 1, 0], [0, 0], [0]]


util.print_array(triangle)

#triangle = handle_row_swap(triangle, 1)


#triangle = comb_with_col_max(triangle, True)


util.print_array(triangle)


tss1 = [[2, 2, 2, 2, 1], [3, 2, 1, 1], [1, 0, 0], [0, 0], [1]]
tss2 = [[2, 1, 0, 0, 0], [4, 3, 2, 1], [2, 1, 1], [0, 0], [1]]
tss3 = [[3, 3, 2, 2, 1], [2, 1, 0, 0], [1, 0, 0], [0, 0], [0]]
tss4 = [[4, 3, 3, 2, 1], [2, 2, 2, 1], [0, 0, 0], [2, 1], [1]]

# #xlist = btss.build_tss(5)
#
# t = tss4
#
# #t = [[4, 1, 1, 0, 0], [4, 2, 0, 0],[2, 2, 0],[1, 1],[0]]
#
# util.print_array(t)
#
# t = comb_with_col_max(t, True)
#
# util.print_array(t)


#compare(6)

#sort_missing_repeats()

#check_diagonal_sum()




### A NEW IDEA: use rows of TSS as columns of BT since they already
### decrease by at most 1.
### now we need columns weakly decreasing.



