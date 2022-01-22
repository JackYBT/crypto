from sys import exit
from bitcoin.core.script import *

from lib.utils import *
from lib.config import (my_private_key, my_public_key, my_address,
                    faucet_address, network_type)
from Q1 import P2PKH_scriptPubKey
from Q2a import Q2a_txout_scriptPubKey


######################################################################
# TODO: set these parameters correctly
amount_to_send = 0.0006 # amount of BTC in the output you're sending minus fee
txid_to_spend = (
        '56ee07fbd2bfe7825b43ba23dd288ec0cd81fc2824f216c76eb99babd199ff26')
utxo_index = 0 # index of the output you are spending, indices start at 0
######################################################################

txin_scriptPubKey = Q2a_txout_scriptPubKey
######################################################################
# TODO: implement the scriptSig for redeeming the transaction created
# in  Exercise 2a.

unlock_x = 5#str.encode(hex(6345))#bytes.fromhex((hex(6345)[2:]))
unlock_y = 1#str.encode(hex(404))#bytes.fromhex((hex(404)[2:]))

txin_scriptSig = [
        unlock_x, unlock_y
]
######################################################################
txout_scriptPubKey = P2PKH_scriptPubKey(faucet_address)

response = send_from_custom_transaction(
    amount_to_send, txid_to_spend, utxo_index,
    txin_scriptPubKey, txin_scriptSig, txout_scriptPubKey, network_type)
print(response.status_code, response.reason)
print(response.text)

'''
{
  "tx": {
    "block_height": -1,
    "block_index": -1,
    "hash": "ed7de1fa306f747ae1d846677498d21ff7ac3c1bf888d66aad3080b4bc46ce37",
    "addresses": [
      "mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB"
    ],
    "total": 59999,
    "fees": 20001,
    "size": 87,
    "vsize": 87,
    "preference": "high",
    "relayed_by": "2607:6b80:5:1::2123",
    "received": "2021-10-12T00:53:49.150126879Z",
    "ver": 1,
    "double_spend": false,
    "vin_sz": 1,
    "vout_sz": 1,
    "confirmations": 0,
    "inputs": [
      {
        "prev_hash": "56ee07fbd2bfe7825b43ba23dd288ec0cd81fc2824f216c76eb99babd199ff26",
        "output_index": 0,
        "script": "5551",
        "output_value": 80000,
        "sequence": 4294967295,
        "script_type": "unknown",
        "age": 0
      }
    ],
    "outputs": [
      {
        "value": 59999,
        "script": "76a9149f9a7abd600c0caa03983a77c8c3df8e062cb2fa88ac",
        "addresses": [
          "mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB"
        ],
        "script_type": "pay-to-pubkey-hash"
      }
    ]
  }
}
'''
