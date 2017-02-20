import sys
sys.path.append('src')
from ethereum import trie, db
import rlp

#initialize trie from previous hash; add new [key, value] where key has common prefix
state = trie.Trie(db.DB(), trie.BLANK_ROOT)
state.update(b'\x01\x01\x02', rlp.encode(['hello']))
print state.root_hash.encode('hex')
print state.root_node
print ''
state.update('\x01\x01\x03', rlp.encode(['hellothere']))
print 'root hash:', state.root_hash.encode('hex')
k, v = state.root_node
print 'root node:', [k, v]
print 'hp encoded key, in hex:', k.encode('hex')
print state._get_node_type(state.root_node) == trie.NODE_TYPE_EXTENSION
common_prefix_key, node_hash = state.root_node
print state._decode_to_node(node_hash)
print state._get_node_type(state._decode_to_node(node_hash)) == trie.NODE_TYPE_BRANCH
