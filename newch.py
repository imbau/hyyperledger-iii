import asyncio
from hfc.fabric import Client
cli = Client(net_profile="test/fixtures/network.json")
loop = asyncio.get_event_loop()
org1_admin = cli.get_user(org_name='org1.example.com', name='Admin') # User instance with the Org1 admin's certs
org2_admin = cli.get_user(org_name='org2.example.com', name='Admin') # User instance with the Org2 admin's certs
orderer_admin = cli.get_user(org_name='orderer.example.com', name='Admin') # User instance with the orderer's certs
# Create a New Channel, the response should be true if succeed
response = loop.run_until_complete(cli.channel_create(
            orderer='orderer.example.com',
            channel_name='businesschannel',
            requestor=org1_admin,
            config_yaml='test/fixtures/e2e_cli/',
            channel_profile='TwoOrgsChannel'
            ))
print(response == True)
# Join Peers into Channel, the response should be true if succeed
orderer_admin = cli.get_user(org_name='orderer.example.com', name='Admin')
responses = loop.run_until_complete(cli.channel_join(
               requestor=org1_admin,
               channel_name='businesschannel',
               peers=['peer0.org1.example.com',
                      'peer1.org1.example.com'],
               orderer='orderer.example.com'
               ))
print(responses)
# For operations on peers from org2.example.com, org2_admin is required as requestor
responses = loop.run_until_complete(cli.channel_join(
               requestor=org2_admin,
               channel_name='businesschannel',
               peers=['peer0.org2.example.com',
                      'peer1.org2.example.com'],
               orderer='orderer.example.com'
               ))
print(responses)

