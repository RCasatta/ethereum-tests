import sys
sys.path.append('src')
from ethereum import trie
import rlp
from ethereum import db

#initialize trie
state = trie.Trie(db._EphemDB(), trie.BLANK_ROOT)
state.update(b'\x01\x01\x02', rlp.encode(['hello']))
print 'root hash', state.root_hash.encode('hex')
k, v = state.root_node
print 'root node:', [k, v]
print 'hp encoded key, in hex:', k.encode('hex')
