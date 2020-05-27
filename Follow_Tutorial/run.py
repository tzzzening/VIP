from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N-i) for i, xi in enumerate(x)) / (N*sum(x)) # harh what's this
    return 1 + (1 / N) - 2 * B


class MoneyAgent(Agent):
    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

    def step(self):
        self.move()
        if self.wealth > 0:
            self.give_money()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            other.wealth += 1
            self.wealth -= 1


class MoneyModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        # Create agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(
            model_reporters={"Gini": compute_gini},
            agent_reporters={"Wealth": "wealth"}) # quite sure it's wrong

    def step(self):
        """Advance the model by on step"""
        self.datacollector.collect(self)
        self.schedule.step()


fixed_params = {"width": 10, "height": 10}
variable_params = {"N": range(10, 500, 10)}

# The variables parameters will be invoked along with the fixed parameters allowing for either or both to be honored.

batch_run = BatchRunner(MoneyModel, variable_params, fixed_params, iterations=5,
                        max_steps=100, model_reporters={"Gini": compute_gini})
print(batch_run.run_all())

run_data = batch_run.get_model_vars_dataframe()
run_data.head()
plt.scatter(run_data.N, run_data.Gini)
plt.show()
# model = MoneyModel(50, 10, 10)
# for i in range(100):
#     model.step()

# gini = model.datacollector.get_model_vars_dataframe()
# df = pd.DataFrame(data=gini)
# print(df)
# agent_wealth = model.datacollector.get_agent_vars_dataframe()
# df = pd.DataFrame(agent_wealth)
# print(df)
# end_wealth = agent_wealth.xs(99, level="Step")["Wealth"] # what is cross section
# plt.hist(end_wealth, bins=range(agent_wealth.Wealth.max()+1))
# #plt.show()
#
# # agent_counts = np.zeros((model.grid.width, model.grid.height))
# # for cell in model.grid.coord_iter():
# #     cell_content, x, y = cell
# #     agent_count = len(cell_content)
# #     agent_counts[x][y] = agent_count
# #
# # plt.imshow(agent_counts, interpolation='nearest')
# # plt.colorbar()
# #
# # plt.show()
#
# # all_wealth = []
# # for j in range(100):
# #     # Run the model
# #     model = MoneyModel(10)
# #     for i in range(10):
# #         model.step()
# #
# #     # Store the results
# #     for agent in model.schedule.agents:
# #         all_wealth.append(agent.wealth)
# #
# # plt.hist(all_wealth, bins=range(max(all_wealth) + 1))
# # plt.show()
#
# d = {'num_legs': [4, 4, 4, 2, 2],
#      'num_wings': [0, 0, 0, 2, 2],
#      'class': ['mammal', 'mammal', 'mammal', 'bird', 'bird'],
#      'animal': ['tiger', 'lion', 'fox', 'eagle', 'penguin'],
#      'locomotion': ['walks', 'walks', 'walks', 'flies', 'walks']}
# df = pd.DataFrame(data=d)
# df = df.set_index(['class', 'animal', 'locomotion'])
# print(df.xs('locomotion'))