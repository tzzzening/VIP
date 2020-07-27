from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from abm_buyer_seller.model import WasteModel


chart = ChartModule([{'Label': 'Recycling_Rate', 'Color': 'Black'},
                     {'Label': 'Seller_Savings', 'Color': 'Blue'},
                     {'Label': 'Buyer_Savings', 'Color': 'Red'},
                     {'Label': 'Overall_Savings', 'Color': 'Green'}],
                    data_collector_name='data_collector')

server = ModularServer(WasteModel, [chart],
                       'Waste Model',
                       {'seller_num': UserSettableParameter('slider', 'Number of sellers', 3, 1, 10),
                        'buyer_num': UserSettableParameter('slider', 'Number of buyers', 3, 1, 10),
                        'width': 1, 'height': 1})
server.port = 8521





