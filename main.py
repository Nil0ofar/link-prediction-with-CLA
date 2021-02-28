from cla import CLA
import os
import datetime

begin_time = datetime.datetime.now()
node_num = 1900
reward = 0.04
penalty = 0.01
iteration = 1
data_path = "./data/"

cla = CLA(node_num, reward, penalty, iteration)

for filename in os.listdir(data_path):
    with open(data_path + filename, 'r') as f:
        mat = [set([]) for i in range(node_num)]
        print(datetime.datetime.now() - begin_time)
        for line in f:
            x, y = map(int, line.split(' '))
            mat[x].add(y)
            mat[y].add(x)
        # print(datetime.datetime.now() - begin_time)
        cla.update(mat)
        print("AUC : " + str(cla.predict(mat)))



