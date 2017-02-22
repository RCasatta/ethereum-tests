from web3 import Web3, KeepAliveRPCProvider
import time
from ethereum import trie, db
import rlp


web3 = Web3(KeepAliveRPCProvider(host="localhost", port=8545))
# web3 = Web3(KeepAliveRPCProvider(host="192.168.1.218", port=8545))


def getRawTransaction(hash):
    return web3._requestManager.request_blocking(
        "eth_getRawTransactionByHash",
        [hash]
    )


def new_block_callback(block_hash):
    print("New Block: {0}".format(block_hash))
    block = web3.eth.getBlock(block_hash, full_transactions=True)
    state = trie.Trie(db.DB(), trie.BLANK_ROOT)
    list_tx_hash = []
    list_tx_raw = []
    print block
    print "total transactions: " + str(len(block[u'transactions']))
    for i, tx_rpc in enumerate(block[u'transactions']):
        list_tx_hash.append(tx_rpc[u'hash'])
        rlp_i = rlp.encode(i)
        try:
            tx_raw = tx_rpc[u'raw'][2:]  # Parity RPC have raw attribute
        except:
            tx_raw = getRawTransaction()[2:] # Geth haven't raw attribute
        list_tx_raw.append(tx_raw)
        state.update(rlp_i, tx_raw.decode('hex'))
        print "RLP " + rlp_i.encode('hex')

    for i, (tx_hash, tx_raw) in enumerate(zip(list_tx_hash, list_tx_raw)):
        create_proof(block, state, tx_hash, i, tx_raw)


def get_append_and_prepend(inside, total):
    idx = total.index(inside, 0, len(total))
    return [total[0:idx], total[idx + len(inside):]]


def create_proof(block, state, tx_hash, i, tx_raw):
    my_root = state.root_hash
    block_root = block[u'transactionsRoot'][2:].decode('hex')
    assert my_root == block_root
    nibbles = trie.bin_to_nibbles(rlp.encode(i))
    current_node = state.root_node
    ops = []
    for i, el in enumerate(nibbles):
        print [cur_el.encode('hex') for cur_el in current_node]
        encoded = rlp.encode(current_node)
        current_node_encoded = encoded.encode('hex')
        print current_node_encoded
        if len(current_node) == 17:

            current_el = current_node[el]
            current_el_hex = current_el.encode('hex')
            [prepend, append] = get_append_and_prepend(current_el_hex, current_node_encoded)
            ops.append("keccak")
            ops.append("append " + append)
            ops.append("prepend " + prepend)

            current_node = state._decode_to_node(current_el)
        else:
            if len(current_node) == 2:
                if str(el) == current_node[0]:
                    tx_raw_hex = current_node[1].encode('hex')
                    [prepend, append] = get_append_and_prepend(tx_raw_hex, current_node_encoded)
                    ops.append("keccak")
                    ops.append("append " + append)
                    ops.append("prepend " + prepend)

    return ops

new_block_callback('0xa684821fe21a67143973a517561619903fac659f2bef31290a5998fdd33a5e5a')
#new_block_filter = web3.eth.filter('latest')
#new_block_filter.watch(new_block_callback)
#time.sleep(100)
