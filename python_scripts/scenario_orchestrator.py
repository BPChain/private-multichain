import asyncio
import websockets
import yaml

addresses = []


def get_master_address():
    return str(master_rpc.getaddresses())[2:-2]


def generate_assets(asset_name, quantity, units):
    get_master_address()
    master_rpc.issue(get_master_address(), asset_name, quantity, units)
    print('Issue ' + str(quantity) + ' of asset ' + asset_name)


def grant_send_permission(address):
    master_rpc.grant(address, 'send')


def grant_receive_permission(address):
    master_rpc.grant(address, 'receive')


async def collect_slave_address(websocket, path):
    if len(addresses) == 2:
        print("#######################")
        await websocket.close()
        asyncio.get_event_loop().stop()


    else:
        address = await websocket.recv()
        addresses.append(address)
        grant_send_permission(address)
        await websocket.send("Send permission granted")
        grant_receive_permission(address)
        await websocket.send("Receive permission granted")



def create_web_socket_server():
    uri = yaml.safe_load(open('python_scripts/config.yml'))
    print(uri['networking']['masterAddress'])
    return websockets.serve(collect_slave_address,
                            host=uri['networking']['masterAddress'],
                            port=uri['networking']['masterPort'])


def start_simulation(rpc_api):
    global master_rpc
    master_rpc = rpc_api
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_web_socket_server())
    loop.run_forever()

    print("#######################")
    print('Simulation scenario started')
    generate_assets('asset1', 1000, 0.01)
    asyncio.get_event_loop().run_forever()
