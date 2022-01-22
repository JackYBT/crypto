from bitcoin import SelectParams
from bitcoin.base58 import decode
from bitcoin.core import x
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2PKHBitcoinAddress


SelectParams('testnet')

faucet_address = CBitcoinAddress('mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB')

# For questions 1-3, we are using 'btc-test3' network. For question 4, you will
# set this to be either 'btc-test3' or 'bcy-test'
network_type = 'btc-test3'


######################################################################
# This section is for Questions 1-3
# TODO: Fill this in with your private key.
#
# Create a private key and address pair in Base58 with keygen.py
# Send coins at https://testnet-faucet.mempool.co/

my_private_key = CBitcoinSecret(
    'cVNpD5uBjorCpsGG1yC6YnzAdVECrJypwJRDqLCzoEtKB9Hm2MYy')
#Address: mv3a1ZqW2w1k2DR8R2tFqao51xkSSTsumc
#TxID: a71ef519b5bed984fdb4a1423ec27e6836bde4b9eff03e10a27a3f19ed8901bf

my_public_key = my_private_key.pub
my_address = P2PKHBitcoinAddress.from_pubkey(my_public_key)
######################################################################


######################################################################
# NOTE: This section is for Question 4
# TODO: Fill this in with address secret key for BTC testnet3
#
# Create address in Base58 with keygen.py
# Send coins at https://testnet-faucet.mempool.co/

# Only to be imported by alice.py
# Alice should have coins!!
alice_secret_key_BTC = CBitcoinSecret(
    'cMqfHCnrDKoU6iy3FfrsdeVJrbi8cPthbjT9jcgEJE4D2vjjKQND')
#Address: miLUvxP4t1nQqDiSYa3UmsjR2emvgZbVHa
#TxID: 23eccbb1031b72db3e5ce13e5fbce1e81d6dd24bc56f7203374fbf7af8ed7c34

# Only to be imported by bob.py
bob_secret_key_BTC = CBitcoinSecret(
    'cQ6Ba7p1e5eu8j9XzQxfmRvA4DcV7c41XPSGSS5wbpyUAoBhndJn')
#Address: n3hkbvUEqXdiHcvF6Juus2n1HWuF2BY9cR
#TxID: e3b5b7381adeef874b0051c039607586b15455517b2e01feb4d8b6e6a0475299
 

# Can be imported by alice.py or bob.py
alice_public_key_BTC = alice_secret_key_BTC.pub
alice_address_BTC = P2PKHBitcoinAddress.from_pubkey(alice_public_key_BTC)

bob_public_key_BTC = bob_secret_key_BTC.pub
bob_address_BTC = P2PKHBitcoinAddress.from_pubkey(bob_public_key_BTC)
######################################################################


######################################################################
# NOTE: This section is for Question 4
# TODO: Fill this in with address secret key for BCY testnet
#
# Create address in hex with
# curl -X POST https://api.blockcypher.com/v1/bcy/test/addrs?token=c8e2c6c726d2475a9e75ae81831b8b1e
# This request will return a private key, public key and address. Make sure to save these.
#
# Send coins with
# curl -d '{"address": "BCY_ADDRESS", "amount": 1000000}' https://api.blockcypher.com/v1/bcy/test/faucet?token=YOURTOKEN
# This request will return a transaction reference. Make sure to save this.

# TOKEN: c8e2c6c726d2475a9e75ae81831b8b1e

# Only to be imported by alice.py
alice_secret_key_BCY = CBitcoinSecret.from_secret_bytes(
    x('a0e2f7f37b824eef46d770fe7654484809f188b07ffa55416deb3bab18be9f3a'))
#  "private": "a0e2f7f37b824eef46d770fe7654484809f188b07ffa55416deb3bab18be9f3a",
#  "public": "028af4c1f22e56cb9f6a0f17afd2ca1ec50aae4f7f14c93b823f5f22d0029b5b34",
#  "address": "C7ksw2Snx47LaPGhbzJwXdhpigWaWF48WY",
#  "wif": "Btimocd9w5yTV1ydgUd6VfRSkTHgfpM1QeL7Lw8gFKHXm9a3Pvr5"
#  Ran curl -d, and "tx_ref": "9e6b40959366d6607c66f91edca9ea40b1126cf2dde41fcc21c69263418be96e"

# Only to be imported by bob.py
# Bob should have coins!!
bob_secret_key_BCY = CBitcoinSecret.from_secret_bytes(
    x('3300aad8ca5171be0e4472c17d5be3e39871eebbff6d487766680725790702a4'))
#  "private": "3300aad8ca5171be0e4472c17d5be3e39871eebbff6d487766680725790702a4",
#  "public": "02eff668b81091def395d63684a8d1e5d1ed7836e5b6abfc26f98f09a5dd4723d0",
#  "address": "CFogJDeCh92ssoaFxS2regbNufZsxA8WBU",
#  "wif": "Bq3Azprwo6hjnk4zQq1FjskiiZ88FPUrxc7ahkGPXDJd8kDgtEZD"
#  Ran curl -d, and "tx_ref": "d76a01071bc11f72ca81b0189d3daea470cb74963996ec13171f7f7447851c5c"

# Can be imported by alice.py or bob.py
alice_public_key_BCY = alice_secret_key_BCY.pub
alice_address_BCY = P2PKHBitcoinAddress.from_pubkey(alice_public_key_BCY)

bob_public_key_BCY = bob_secret_key_BCY.pub
bob_address_BCY = P2PKHBitcoinAddress.from_pubkey(bob_public_key_BCY)
######################################################################
