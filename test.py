from ethereum import trie, db

key1=b'\x01\x01\x02'
key2=b'\x01\x01\x03'
element1 = 'ciao'
element2 = 'bao'

state1 = trie.Trie(db.DB(), trie.BLANK_ROOT)
state1.update(key1, element1)
state1.update(key1, element1)


state2 = trie.Trie(db.DB(), trie.BLANK_ROOT)
