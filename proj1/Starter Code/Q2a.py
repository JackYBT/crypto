from sys import exit
from bitcoin.core.script import *

from lib.utils import *
from lib.config import (my_private_key, my_public_key, my_address,
                    faucet_address, network_type)
from Q1 import send_from_P2PKH_transaction


######################################################################
# TODO: Complete the scriptPubKey implementation for Exercise 2

#True SUID: 00050001 06345405
#Fake SUID: 00050001
# Assuming that the Stack looks like: x | y
x = 6 #6749 #bytes.fromhex("1a5d")#hex(6345 + 404))
y = 4 #0x1735#5941 #bytes.fromhex("1735")#str.encode(hex(6345 - 404)) 
Q2a_txout_scriptPubKey = [
        OP_2DUP, OP_ADD, x, OP_EQUALVERIFY, OP_SUB, y, OP_EQUAL
    ]
    #OP_2DUP, OP_ADD, hex(634), OP_EQUALVERIFY, OP_SUB, hex(5404), OP_EQUALVERIFY
######################################################################

if __name__ == '__main__':
    ######################################################################
    # TODO: set these parameters correctly
    amount_to_send = 0.0008 # amount of BTC in the output you're sending minus fee
    txid_to_spend = (
        '5b35b0e9689c426561160e532267044b2b94f0a253bc0d6b0653e1d5a7dff273')
    utxo_index = 0 # index of the output you are spending, indices start at 0
    ######################################################################

    response = send_from_P2PKH_transaction(
        amount_to_send, txid_to_spend, utxo_index,
        Q2a_txout_scriptPubKey, my_private_key, network_type)
    print(response.status_code, response.reason)
    print(response.text)
'''
201 Created
{
  "tx": {
    "block_height": -1,
    "block_index": -1,
    "hash": "56ee07fbd2bfe7825b43ba23dd288ec0cd81fc2824f216c76eb99babd199ff26",
    "addresses": [
      "mv3a1ZqW2w1k2DR8R2tFqao51xkSSTsumc"
    ],
    "total": 80000,
    "fees": 20000,
    "size": 174,
    "vsize": 174,
    "preference": "high",
    "relayed_by": "2607:6b80:5:1::2123",
    "received": "2021-10-12T00:49:19.54714645Z",
    "ver": 1,
    "double_spend": false,
    "vin_sz": 1,
    "vout_sz": 1,
    "confirmations": 0,
    "inputs": [
      {
        "prev_hash": "5b35b0e9689c426561160e532267044b2b94f0a253bc0d6b0653e1d5a7dff273",
        "output_index": 0,
        "script": "483045022100a50d3136f9387f521f8bdeb9533ba53f9fccdd841796cbe6ddbbeedcb7917920022055338dc6c32854ab1771143b00de789301de7053e5278c77d570396fe3996cb30121036ff950c5002fb35639223a911fe4f663c599882388fbd9d1911087b7e89b7fee",
        "output_value": 100000,
        "sequence": 4294967295,
        "addresses": [
          "mv3a1ZqW2w1k2DR8R2tFqao51xkSSTsumc"
        ],
        "script_type": "pay-to-pubkey-hash",
        "age": 0
      }
    ],
    "outputs": [
      {
        "value": 80000,
        "script": "6e935688945487",
        "addresses": null,
        "script_type": "unknown"
      }
    ]
  }
}

'''