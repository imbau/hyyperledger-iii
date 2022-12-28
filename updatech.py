import nest_asyncio
nest_asyncio.apply()

import asyncio

from hfc.fabric import Client

loop = asyncio.get_event_loop()
cli = Client(net_profile="test/fixtures/network.json")

org1_admin = cli.get_user(org_name='org1.example.com', name='Admin') # User instance with the Org1 admin's certs
org2_admin = cli.get_user(org_name='org2.example.com', name='Admin') # User instance with the Org2 admin's certs
#orderer_admin = cli.get_user(org_name='orderer.example.com', name='Admin') # User instance with the orderer's certs
cli.new_channel('businesschannel')

import os
gopath_bak = os.environ.get('GOPATH')
gopath = os.path.normpath(os.path.join(
                      os.path.dirname(os.path.realpath('__file__')),
                      'test/fixtures/chaincode'
                     ))
# The response should be true if succeed
responses = loop.run_until_complete(cli.chaincode_install(
               requestor=org1_admin,
               peers=['peer0.org1.example.com',
                      'peer1.org1.example.com'],
               cc_path='github.com/example3',
               cc_name='example5',
               cc_version='v1.0'
               ))
# Instantiate Chaincode in Channel, the response should be true if succeed
args = ['a', '200', 'b', '300']

# This policy specifies the endorsement policy which is required while instantiating the chaincode
policy = {
    'identities': [
        {'role': {'name': 'member', 'mspId': 'Org1MSP'}},
    ],
    'policy': {
        '1-of': [
            {'signed-by': 0},
        ]
    }
}
response = loop.run_until_complete(cli.chaincode_instantiate(
               requestor=org1_admin,
               channel_name='businesschannel',
               peers=['peer0.org1.example.com'],
               args=args,
               cc_name='example5',
               cc_version='v1.0',
               cc_endorsement_policy=policy, # optional, but recommended
               collections_config=None, # optional, for private data policy
               transient_map=None, # optional, for private data
               wait_for_event=True # optional, for being sure chaincode is instantiated
               ))
# Invoke a chaincode
args = ['c', 'd', '50']
# The response should be true if succeed
response = loop.run_until_complete(cli.chaincode_invoke(
               requestor=org1_admin,
               channel_name='businesschannel',
               peers=['peer0.org1.example.com'],
               args=args,
               cc_name='example5',
               transient_map=None, # optional, for private data
               wait_for_event=True, # for being sure chaincode invocation has been commited in the ledger, default is on tx event
               #cc_pattern='^invoked*' # if you want to wait for chaincode event and you have a `stub.SetEvent("invoked", value)` in your chaincode
               ))

print(response)
# Query a chaincode
args = ['a']
# The response should be true if succeed
response = loop.run_until_complete(cli.chaincode_query(
               requestor=org1_admin,
               channel_name='businesschannel',
               peers=['peer0.org1.example.com'],
               args=args,
               cc_name='example5'
               ))
print(response)
