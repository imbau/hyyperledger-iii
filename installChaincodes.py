import asyncio
from hfc.fabric import Client

loop = asyncio.get_event_loop()

cli = Client(net_profile="test/fixtures/network.json")
org1_admin = cli.get_user('org1.example.com', 'Admin')

# Make the client know there is a channel in the network
cli.new_channel('businesschannel')

# Install Example Chaincode to Peers
# GOPATH setting is only needed to use the example chaincode inside sdk
import os
gopath_bak = os.environ.get('GOPATH', '')
gopath = os.path.normpath(os.path.join(
                      os.path.dirname(os.path.realpath('__file__')),
                      'test/fixtures/chaincode'
                     ))
os.environ['GOPATH'] = os.path.abspath(gopath)

# The response should be true if succeed
responses = loop.run_until_complete(cli.chaincode_install(
               requestor=org1_admin,
               peers=['peer0.org1.example.com',
                      'peer1.org1.example.com'],
               cc_path='github.com/example_cc',
               cc_name='example_cc',
               cc_version='v1.0'
               ))

# Instantiate Chaincode in Channel, the response should be true if succeed
args = ['a', '200', 'b', '300']

# policy, see https://hyperledger-fabric.readthedocs.io/en/release-1.4/endorsement-policies.html
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
               cc_name='example_cc',
               cc_version='v1.0',
               cc_endorsement_policy=policy, # optional, but recommended
               collections_config=None, # optional, for private data policy
               transient_map=None, # optional, for private data
               wait_for_event=True # optional, for being sure chaincode is instantiated
               ))

# Invoke a chaincode
args = ['a', 'b', '100']
# The response should be true if succeed
response = loop.run_until_complete(cli.chaincode_invoke(
               requestor=org1_admin,
               channel_name='businesschannel',
               peers=['peer0.org1.example.com'],
               args=args,
               cc_name='example_cc',
               transient_map=None, # optional, for private data
               wait_for_event=True, # for being sure chaincode invocation has been commited in the ledger, default is on tx event
               #cc_pattern='^invoked*' # if you want to wait for chaincode event and you have a `stub.SetEvent("invoked", value)` in your chaincode
               ))

# Query a chaincode
args = ['b']
# The response should be true if succeed
response = loop.run_until_complete(cli.chaincode_query(
               requestor=org1_admin,
               channel_name='businesschannel',
               peers=['peer0.org1.example.com'],
               args=args,
               cc_name='example_cc'
               ))
print(response)

# Upgrade a chaincode
# policy, see https://hyperledger-fabric.readthedocs.io/en/release-1.4/endorsement-policies.html
policy = {
    'identities': [
        {'role': {'name': 'member', 'mspId': 'Org1MSP'}},
        {'role': {'name': 'admin', 'mspId': 'Org1MSP'}},
    ],
    'policy': {
        '1-of': [
            {'signed-by': 0}, {'signed-by': 1},
        ]
    }
}
response = loop.run_until_complete(cli.chaincode_upgrade(
               requestor=org1_admin,
               channel_name='businesschannel',
               peers=['peer0.org1.example.com'],
               args=args,
               cc_name='example_cc',
               cc_version='v1.0',
               cc_endorsement_policy=policy, # optional, but recommended
               collections_config=None, # optional, for private data policy
               transient_map=None, # optional, for private data
               wait_for_event=True # optional, for being sure chaincode is upgraded
               ))            
