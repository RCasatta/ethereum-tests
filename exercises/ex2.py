import sys
sys.path.append('src')
from ethereum import trie, db
import rlp

state = trie.Trie(db.DB(), trie.BLANK_ROOT)
state.update(b'\x01\x01\x02', rlp.encode(['hello']))

#initialize trie from previous hash; add new entry with same key.
print state.root_hash.encode('hex')
print state.root_node
print ''
state.update('\x01\x01\x02', rlp.encode(['hellothere']))
print state.root_hash.encode('hex')
print state.root_node
# we now have two tries, addressed in the database by their respective hashes, though they each have the same key
