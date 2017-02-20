from ethereum import trie, db, utils
import rlp

# Block number 233481
# hash 0xccc6da94c2f8d222ef723db7c0469fb54790d30c31c4c176837570953a11d4b5
# tx hash root 0x94855872b7fee469b12577beb875a3ad65b479a216cbbaf9f23ab1277393b084
# contain one tx with hash 0x0d3789c1341c2edb92429f8e8f669f057be5bad2b5dba9ac52069e5b2535e696
# whose content is 0xf86f824ed5850ba43b740083015f90941df99e975f2e6c2e6945cda3a377552cb582caf688477a615df3b28800801ca09e43bb22f0458d7f3025dfa01e9f223743f8dae2c7b11070529dc2733358f0fba07bfe8c286d21839d153733328d8f48e7e7b3fe79c2f31fd2bf992b2381980f48

tx = 'f86f824ed5850ba43b740083015f90941df99e975f2e6c2e6945cda3a377552cb582caf688477a615df3b28800801ca09e43bb22f0458d7f3025dfa01e9f223743f8dae2c7b11070529dc2733358f0fba07bfe8c286d21839d153733328d8f48e7e7b3fe79c2f31fd2bf992b2381980f48'.decode('hex')
txhash = utils.sha3(tx)
assert '0d3789c1341c2edb92429f8e8f669f057be5bad2b5dba9ac52069e5b2535e696' == txhash.encode('hex')
state = trie.Trie(db.DB(), trie.BLANK_ROOT)
assert '56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421' == state.root_hash.encode('hex')  # empty trie root hash
rlp_zero = rlp.encode(0)
state.update(rlp_zero, tx)
root = state.root_hash.encode('hex')
assert '94855872b7fee469b12577beb875a3ad65b479a216cbbaf9f23ab1277393b084' == root  # THIS FAILS

# Block Number 233488
# hash 0xdb252a8c065771f141fee97503db684f8b84804d2ce0b38967370ef85310e5ae
# Tx Hash root: 0xc7c50415e3368e97bf2af3743f5678c7833d449bce0621eb2f8d8dfe45c4984d
# contains two transaction: with hash:
# - 0x1328e8a3eb0db1376182d7d53fc6024be3c06553295ca36eaed0bbac395f125c     0xf86f820c86850ba43b74008252089403e2084aeca980ba3480a69e6bb572d0825be64489033a036835acc8c000801ba074e3927d28f11eb23128d66635077befbe8c14e2efadfb600c9471189616b5a4a00b9a8dd01b4a5a3eb86c3779f25fe9ad5bea1f8ecc8f4e1afcae8bcc5fc97414
# - 0x60e1bef234b5a9a97860d38bbd039a8b724b2d93c114fdfdc01400f813bd76c7     0xf86d80850ba43b740083015f909428d252ec46a4d6ac35a25a6518da44c6e54ee015888963dd8c2c5e0000801ba01016002eea0b7beebf280ca8db0201609e550e1fa3bf7e339fbb110427aec97ea01cd0cdabb336b59abea4d122afacb717dc566617fede137ddecf9dd5472e9180

tx0 = 'f86d80850ba43b740083015f909428d252ec46a4d6ac35a25a6518da44c6e54ee015888963dd8c2c5e0000801ba01016002eea0b7beebf280ca8db0201609e550e1fa3bf7e339fbb110427aec97ea01cd0cdabb336b59abea4d122afacb717dc566617fede137ddecf9dd5472e9180'.decode('hex')
tx1 = 'f86f820c86850ba43b74008252089403e2084aeca980ba3480a69e6bb572d0825be64489033a036835acc8c000801ba074e3927d28f11eb23128d66635077befbe8c14e2efadfb600c9471189616b5a4a00b9a8dd01b4a5a3eb86c3779f25fe9ad5bea1f8ecc8f4e1afcae8bcc5fc97414'.decode('hex')
assert '60e1bef234b5a9a97860d38bbd039a8b724b2d93c114fdfdc01400f813bd76c7' == utils.sha3(tx0).encode('hex')
assert '1328e8a3eb0db1376182d7d53fc6024be3c06553295ca36eaed0bbac395f125c' == utils.sha3(tx1).encode('hex')

state2 = trie.Trie(db.DB(), trie.BLANK_ROOT)
assert '56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421' == state2.root_hash.encode('hex')  # empty trie root hash
state2.update(rlp_zero, tx0)
rlp_one = rlp.encode(1)
state2.update(rlp_one, tx1)


state3 = trie.Trie(db.DB(), trie.BLANK_ROOT)
assert '56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421' == state3.root_hash.encode('hex')  # empty trie root hash
state3.update(rlp_one, tx1)
state3.update(rlp_zero, tx0)

assert state2.root_hash == state3.root_hash  # patricia trie are idempotent

assert 'c7c50415e3368e97bf2af3743f5678c7833d449bce0621eb2f8d8dfe45c4984d' == state2.root_hash.encode('hex')


# state2.update('\x81', "ciao")

# val = trie.bin_to_nibbles(rlp_zero)

root_node = state2.root_node
print utils.sha3(rlp.encode(root_node)).encode('hex')
print state2._get_node_type(root_node)
print root_node
print

node0 = state2._decode_to_node(root_node[0])
print utils.sha3(rlp.encode(node0)).encode('hex')
print state2._get_node_type(node0)
print node0
print

print node0[1].encode('hex')
print utils.sha3(node0[1]).encode('hex')

# node8 = state2._decode_to_node(root_node[8])
# print state2._get_node_type(node0)
# print node8



