from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from abm_buyer_seller.model import WasteModel


chart = ChartModule([{'Label': 'Recycling_Rate',
                      'Color': 'Black'}],
                    data_collector_name='data_collector')

server = ModularServer(WasteModel,
                       [chart],
                       'Waste Model',
                       {'num_per_agent': 1, 'width': 1, 'height': 1})
server.port = 8521
# server.launch()





