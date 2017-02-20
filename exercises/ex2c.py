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
state.update('\x01\x01', rlp.encode(['hellothere']))
print 'root hash:', state.root_hash.encode('hex')
print 'root node:', state.root_node
print state._decode_to_node(state.root_node[1])
