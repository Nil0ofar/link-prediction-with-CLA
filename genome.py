class Genome :
    #gene = []

    def __init__(self , gene):
        self.gene = gene

    def fitness(self, goal):
        total = 0
        correct = 0

        for idx in range(len(self.gene)):
            g = self.gene[idx]
            if g == 1:
                total += 1
                if goal[idx] == 1:
                    correct += 1
        if total == 0:
            return 0
        #print(correct , total)
        return correct / len(self.gene)