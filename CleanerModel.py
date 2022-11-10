import mesa
import random
import time
import math


class Agents(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.counter = 0

    def step(self):
        if self.model.dirtyCellRatio() >= .999:
            self.model.endTime = time.time()
        self.move()
        self.clean()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.counter = self.counter + 1

    def clean(self):
        if self.model.isDirty(self.pos):
            self.model.setDirty(self.pos)



class CleanerModel(mesa.Model):
    def __init__(self, n, width, height, percent):
        self.num_agents = n
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.startTime = time.time()
        self.endTime = 0
        
        self.cellsDirty = math.ceil((width * height) * percent)
        self.cellsClean = math.ceil((width * height) * (1 - percent))

        self.dMatrix = [[False for _ in range(height)] for _ in range(width)]

        for i in range(self.cellsDirty):
            dx = random.randint(0, width - 1)
            dy = random.randint(0, height - 1)
            self.dMatrix[dx][dy] = True

        for i in range(self.num_agents):
            a = Agents(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (1, 1))

    def step(self):
        self.schedule.step()
        
    def isDirty(self, new_position):
        x, y = new_position
        return self.dMatrix[x][y]

    
    def setDirty(self, new_position):
        self.cellsDirty = self.cellsDirty - 1
        self.cellsClean = self.cellsClean + 1

        x, y = new_position

        self.dMatrix[x][y] = False

        if self.cellsDirty == 0:
            self.endTime = time.time()

    
    def counter(self):
        return [agent.counter for agent in self.schedule.agents]

    
    def dirtyCellRatio(self):
        return self.cellsClean / (self.cellsClean + self.cellsDirty)

    def programTime(self):
        return self.endTime - self.startTime
