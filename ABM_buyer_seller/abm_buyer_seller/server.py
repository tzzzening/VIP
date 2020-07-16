from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from abm_buyer_seller.model import WasteModel


recycling_rate_chart = ChartModule([{'Label': 'Recycling_Rate',
                      'Color': 'Black'}],
                    data_collector_name='data_collector')
# seller_savings_chart = ChartModule([{'Label': ''}])

server = ModularServer(WasteModel, [recycling_rate_chart],
                       'Waste Model',
                       {'seller_num': UserSettableParameter('slider', 'Number of sellers', 3, 1, 10),
                        'buyer_num': UserSettableParameter('slider', 'Number of buyers', 3, 1, 10),
                        'width': 1, 'height': 1})
server.port = 8521
# server.launch()





