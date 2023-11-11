# Pablo Ceballos Gutiérrez A01660148
# Modelación de Sistemas Multiagentes y Gráficas Computacionales

import mesa 
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from cruce_model_script import mesa, CruceModel

def batch():
    paramas = {"width": 20, "height": 20}

    results = mesa.batch_run(
        CruceModel,
        parameters=paramas,
        iterations=10,
        max_steps=1000,
        number_processes=1,
        data_collection_period=1,
        display_progress=True,
    )

    results_df = pd.DataFrame(results)
    print(results_df.keys())
    
    df_no_duplicates = results_df.drop_duplicates()
    
    df_no_duplicates.to_excel("output.xlsx") 


def agent_portrayal(agent):

    if agent.val == 0:
        portrayal = {"Shape": "rect", "Filled": "true", "h": 1.0, "w": 1.0, "Color": "black", "Layer": 1}
    if agent.val == 1:
        portrayal = {"Shape": "circle", "Filled": "true", "r": 1.0, "Color": "grey", "Layer": 2}
    if agent.val == 2:
        portrayal = {"Shape": "circle", "Filled": "true", "r": 1.0, "Color": "green", "Layer": 3}
    if agent.val == 3:
        portrayal = {"Shape": "circle", "Filled": "true", "r": 1.0, "Color": "black", "Layer": 4}

    return portrayal

def main():
    batch()

    model = CruceModel(20, 20)
    model.step()

    grid = mesa.visualization.CanvasGrid(agent_portrayal, 20, 20)
    
    chart = mesa.visualization.ChartModule(
        [{"Label": "num_crashed_agents", "Color": "black", }], 
        data_collector_name = "datacollector"
    )
    server = mesa.visualization.ModularServer(
        CruceModel, [grid, chart], "Cruce Model", {"width": 20, "height": 20}
    )
    server.port = 8521  # The default
    server.launch()

main()