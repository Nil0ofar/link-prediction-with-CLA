from cla import CLA
import os
import datetime

begin_time = datetime.datetime.now()
node_num = 1900
reward = 0.04
penalty = 0.01
iteration = 1
data_path = "./data/"

cla = CLA(node_num, penalty, reward, iteration)


def makeElementsUniqe(mat):
    for i in range(len(mat)):
        mat[i] = list(set(mat[i]))


for filename in os.listdir(data_path):
    with open(data_path + filename, 'r') as f:
        mat = [[] for i in range(node_num)]
        print(datetime.datetime.now() - begin_time)
        for line in f:
            x, y = map(int, line.split(' '))
            mat[x].append(y)
            mat[y].append(x)

        makeElementsUniqe(mat)

        cla.update(mat)
        print("AUC : " + str(cla.predict(mat)))

print(datetime.datetime.now() - begin_time)

