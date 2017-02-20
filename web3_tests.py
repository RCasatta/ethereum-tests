from web3 import Web3, KeepAliveRPCProvider
from ethereum import utils, trie, db
import rlp
import sys


web3 = Web3(KeepAliveRPCProvider(host="192.168.1.218", port=8545))

def new_block_callback(block_hash):
    sys.stdout.write("New Block: {0}".format(block_hash))

def getRawTransaction(hash):
    return web3._requestManager.request_blocking(
        "eth_getRawTransactionByHash",
        [hash]
    )

# new_block_filter = web3.eth.filter('latest')
# new_block_filter.watch(new_block_filter)


def getAppendAndPrepend(inside, total):
    idx = total.index(inside, 0, len(total))
    return [total[0:idx], total[idx + len(inside):]]


def get_proof(block_number, timestamping_tx_hash, timestamping_root):
    block = web3.eth.getBlock(block_number)

    tx_root = block[u'transactionsRoot']
    state = trie.Trie(db.DB(), trie.BLANK_ROOT)
    print tx_root

    for i, tx_hash in enumerate(block[u'transactions']):
        print
        print tx_hash
        tx_raw = getRawTransaction(tx_hash)
        print tx_raw
        rlp_i = rlp.encode(i)
        state.update(rlp_i, tx_raw[2:].decode('hex'))
        if tx_hash[2:] == timestamping_tx_hash:
            my_i = rlp_i

    assert state.root_hash.encode('hex') == tx_root[2:]

    val = trie.bin_to_nibbles(my_i)

    current_node = state.root_node
    ops = []

    for i, el in enumerate(val):
        print
        print el
        print [cur_el.encode('hex') for cur_el in current_node]
        encoded = rlp.encode(current_node)
        current_node_encoded = encoded.encode('hex')
        print encoded.encode('hex')
        print utils.sha3(encoded).encode('hex')
        if len(current_node) == 17:

            current_el = current_node[el]
            current_el_hex = current_el.encode('hex')
            [prepend, append] = getAppendAndPrepend(current_el_hex, current_node_encoded)
            ops.append("keccak")
            ops.append("append " + append)
            ops.append("prepend " + prepend)

            current_node = state._decode_to_node(current_el)
        else:
            if len(current_node) == 2:
                if str(el) == current_node[0]:
                    tx_raw_hex = current_node[1].encode('hex')
                    [prepend, append] = getAppendAndPrepend(tx_raw_hex, current_node_encoded)
                    ops.append("keccak")
                    ops.append("append " + append)
                    ops.append("prepend " + prepend)


    print
    print tx_raw_hex
    print timestamping_root

    [prepend, append] = getAppendAndPrepend(timestamping_root, tx_raw_hex)

    print
    print "File sha256 hash: " + timestamp_root_hex
    print "Timestamp:"
    print "prepend " + prepend
    print "append " + append
    # print "keccak"  # result is tx hash 0x1328e8a3eb0db1376182d7d53fc6024be3c06553295ca36eaed0bbac395f125c
    while len(ops):
        print ops.pop()

timestamp_root_hex = "e54ee015888963dd8c2c5e0000801ba01016002eea0b7beebf280ca8db020160"
tx_hash_hex = "60e1bef234b5a9a97860d38bbd039a8b724b2d93c114fdfdc01400f813bd76c7"
get_proof(233488, tx_hash_hex , timestamp_root_hex)

# MANUAL TEST

timestamp_root = timestamp_root_hex.decode('hex')
tx_prepend = "f86d80850ba43b740083015f909428d252ec46a4d6ac35a25a6518da44c6".decode('hex')
tx_append = "9e550e1fa3bf7e339fbb110427aec97ea01cd0cdabb336b59abea4d122afacb717dc566617fede137ddecf9dd5472e9180".decode('hex')
tx = tx_prepend + timestamp_root + tx_append
tx_hash = utils.sha3(tx)
assert tx_hash.encode('hex') == tx_hash_hex

last_node_prepend = "f87230b86f".decode('hex')
last_node_rlp = last_node_prepend + tx
# print last_node_rlp.encode('hex')
a = utils.sha3(last_node_rlp)
assert a.encode('hex') == "219b81e00693bba2d8daa738ebf86699a40dbd4458de5032f2b58bb1152d6bb9"

node_prepend = "f851a0d087174aa678152bceb160cb4431cb3ae31b980e330b9850ae06bd0603b65db280808080808080a0".decode('hex')
node_append = "8080808080808080".decode('hex')
b = utils.sha3(node_prepend + a + node_append)

assert b.encode('hex') == "c7c50415e3368e97bf2af3743f5678c7833d449bce0621eb2f8d8dfe45c4984d"

print "verify EthereumBlockHeaderAttestation(233488)"

# print tx
#tx = transactions.Transaction(tx[u'nonce'],
#                              tx[u'gasPrice'],
#                              tx[u'gas'],
#                              tx[u'to'],
#                              tx[u'value'],
#                              tx[u'data'] if u'data' in tx else '',
#                              27,
#                              #tx[u'v'],
#                              tx[u'r'][2:].decode('hex'),
#                              tx[u's']
#                              )

# print tx.hash
# print web3.eth.getRawTransaction(txhas)
# nonce, gasprice, startgas, to, value, data, v=0, r=0, s=0):

#while True:
#    time.sleep(1)
#    print web3.eth.blockNumber


