# Pablo Ceballos Gutiérrez A01660148
# Modelación de Sistemas Multiagentes y Gráficas Computacionales

import mesa 
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import random
import math

class RellenoAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.val = 0
        self.chocado = 0

class CocheEstorbo(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.val = 1
        self.chocado = 0

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore = True, include_center = False
        )
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        
        if len(cellmates) <= 1:
            self.model.grid.move_agent(self, possible_steps[4])
        else:
            self.chocado = 0.5


    def step(self):
        self.move()

class CocheEstorboLento(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.val = 3
        self.chocado = 0
        self.movement = 0

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore = True, include_center = False
        )
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        
        if len(cellmates) <= 1:
            self.model.grid.move_agent(self, possible_steps[4])
        else:
            self.chocado = 0.5


    def step(self):
        if self.movement % 2 == 0: 
            self.move()

        self.movement += 1

class CochePrincipal(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.val = 2
        self.chocado = 0

    def move(self, m):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore = True, include_center = False
        )
        cellmates = self.model.grid.get_cell_list_contents([self.pos])

        if len(cellmates) <= 1:
            if m == 1:
                self.model.grid.move_agent(self, possible_steps[6])
        else:
            self.chocado = 0.5

    
    def step(self):
        m = random.randint(0, 1)
        self.move(m)



class CruceModel(mesa.Model):
    def __init__(self, width, height):
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.running = True
        R = 0
        w_2 = width//2
        h_2 = height//2

        for i in range(height):

            for j in range(width):
                
                r = RellenoAgent(R, self)
                self.schedule.add(r)

                x = j
                y = i

                self.grid.place_agent(r, (x, y))

                if (j == w_2 - 2):
                    self.grid.remove_agent(r)
                    self.schedule.remove(r)                    
                
                if (j == w_2 - 1):
                    self.grid.remove_agent(r)
                    self.schedule.remove(r)

                if j == w_2:
                    self.grid.remove_agent(r)
                    self.schedule.remove(r)

                if (j == w_2 + 1):
                    self.grid.remove_agent(r)
                    self.schedule.remove(r)

                if (i == h_2 - 2) and (self.grid.is_cell_empty([x, y]) == False):
                    self.grid.remove_agent(r)
                    self.schedule.remove(r)

                if (i == h_2 - 1) and (self.grid.is_cell_empty([x, y]) == False):
                    self.grid.remove_agent(r)
                    self.schedule.remove(r)

                if (i == h_2) and (self.grid.is_cell_empty([x, y]) == False):
                    self.grid.remove_agent(r)
                    self.schedule.remove(r)

                if (i == h_2 + 1) and (self.grid.is_cell_empty([x, y]) == False):
                    self.grid.remove_agent(r)
                    self.schedule.remove(r)
                    
                R += 1

        #############
        pos_CE = R + 1
        ce_pos_x = 1

        for i in range(2):
            
            i = pos_CE + i
            ce = CocheEstorbo(i, self)
            self.schedule.add(ce)

            y = 5
            x = 8 + ce_pos_x
            

            self.grid.place_agent(ce, (x, y))
            ce_pos_x += 1
            pos_CE = i
            
        #############

        #############
        
        cp_pos_y = 0
        for i in range(4):
        
            i = pos_CE + 1 + i
            cp = CochePrincipal(i, self)
            self.schedule.add(cp)

            x = random.randrange(0, w_2-2)
            y = 8 + cp_pos_y

            self.grid.place_agent(cp, (x, y))
            cp_pos_y += 1
            pos_CE = i
        #############

        #############
        cl_pos_x = 0
        for i in range(2):
            i = pos_CE + 1 + i
            cl = CocheEstorboLento(i, self)
            self.schedule.add(cl)

            y = 4
            x = 8 + cl_pos_x

            self.grid.place_agent(cl, (x, y))
            cl_pos_x += 3
            pos_CE = i


        #############

        self.datacollector = mesa.DataCollector(
            model_reporters={"num_crashed_agents": lambda m: sum([a.chocado for a in m.schedule.agents if a.chocado])},
            agent_reporters={"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )


    
    def step(self):
        agent_choques = [agent.chocado for agent in self.schedule.agents]
        sumaC = 0

        for i in agent_choques:
            sumaC += i
   
        self.datacollector.collect(self)
        self.schedule.step()

        if sumaC == 4:
            self.running = False

        

