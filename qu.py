import asyncio
from hfc.fabric_network.gateway import Gateway
from hfc.fabric_network.network import Network
from hfc.fabric_network.contract import Contract
from hfc.fabric import Client

loop = asyncio.get_event_loop()

cli = Client(net_profile="test/fixtures/network.json")
org1_admin = cli.get_user(org_name='org1.example.com', name='Admin')

new_gateway = Gateway() # Creates a new gateway instance
options = {'wallet': ''}
response = loop.run_until_complete(new_gateway.connect('test/fixtures/network.json', options))
new_network = loop.run_until_complete(new_gateway.get_network('businesschannel', org1_admin))
new_contract = new_network.get_contract('example_cc')

response = loop.run_until_complete(new_contract.submit_transaction('businesschannel', ['a', 'b', '100'], org1_admin))

print(response)
response  = loop.run_until_complete(new_contract.evaluate_transaction('businesschannel', ['b'], org1_admin))


print(response)
