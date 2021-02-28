class Genome:

    def __init__(self, gene):
        self.gene = set(gene)

    def fitness(self, goal):
        # correct predicted links / total predicted links
        if len(self.gene) == 0:
            return 0
        return len(self.gene.intersection(goal)) / len(self.gene)