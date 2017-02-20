from ethereum import utils

helloworld='48656c6c6f20576f726c64210a'.decode('hex')
print utils.sha3(helloworld).encode('hex')  # dc85a6bbfd4658040ef305c9333cf0d5a82ede2854f112549f3925df6b2c0e71

# tx containing is 0x54bf558f2e7d7010543477f135e7e518f9730921d41e86a9dd7abafd8931f64e
# gas used Gas Used: 23,176