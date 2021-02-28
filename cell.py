from la import LA
from genome import Genome


class Cell:
    threshold = 0.1

    def __init__(self, sz, penalty, reward, num):
        self._size = sz
        self.penalty = penalty
        self.reward = reward
        self.LAs = []
        self.neighbor = []
        self.chosen_neighbor = []
        self.num = num
        for i in range(sz):
            self.LAs.append(LA())

        self.genome = Genome([])

    def update_genome(self, goal):
        temp = []
        for idx, l in enumerate(self.LAs):
            if l.get_action() == 1:
                temp.append(idx)
        new_genome = Genome(temp)

        if self.genome.fitness(goal[self.num]) < new_genome.fitness(goal[self.num]):
            self.genome = new_genome

    def update_chosen_neighbor(self, goal):
        self.chosen_neighbor.clear()
        for other in self.neighbor:
            if other.genome.fitness(goal[other.num]) > Cell.threshold:
                self.chosen_neighbor.append(other)

    def __update(self, idx, choice, punish):
        if punish:
            self.LAs[idx].probability[choice] = (1 - self.penalty) * self.LAs[idx].probability[choice]
        else:
            self.LAs[idx].probability[choice] += self.reward * (1 - self.LAs[idx].probability[choice])

        self.LAs[idx].probability[1 - choice] = 1 - self.LAs[idx].probability[choice]

    def update_by_reinforcement_signal(self):
        for idx in range(self._size):
            one = 0
            zero = 0

            for ne in self.chosen_neighbor:
                if idx in ne.genome.gene:
                    one += 1
                else:
                    zero += 1

            if idx in self.genome.gene:
                self.__update(idx, 1, one < zero)
            else :
                self.__update(idx, 0, zero < one)

