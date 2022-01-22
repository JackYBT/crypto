from sys import exit
from bitcoin.core.script import *
from bitcoin.wallet import CBitcoinSecret

from lib.utils import *
from lib.config import (my_private_key, my_public_key, my_address,
                    faucet_address, network_type)
from Q1 import send_from_P2PKH_transaction


cust1_private_key = CBitcoinSecret(
    'cRof19TrTZDKH6G2G6rR6ovjYDWsYmNkKwKM8K987t4QVZDq8APU')
cust1_public_key = cust1_private_key.pub
#mw2mSJQ8Sd9D9UVoH9HPeCCFDfLPjKHoiv
cust2_private_key = CBitcoinSecret(
    'cQnWgD4HGtqDPJrLEQZiR1ixBMQ87Gx16ueVuotJQEyGZUmha9kY')
cust2_public_key = cust2_private_key.pub
#mj2enPU7JBHauchHZnjp4eo34eyUL6L2Vf
cust3_private_key = CBitcoinSecret(
    'cUFss4XhSC1vCLp8AqT1DYnDaowWG4RGdNRsz9f9VRQ3Aq7XW3nq')
cust3_public_key = cust3_private_key.pub
#mzVZcjYGuix6cx1NPtRwLcFRn9pikP3P7L


######################################################################
# TODO: Complete the scriptPubKey implementation for Exercise 3

# You can assume the role of the bank for the purposes of this problem
# and use my_public_key and my_private_key in lieu of bank_public_key and
# bank_private_key.

Q3a_txout_scriptPubKey = [
        my_public_key, OP_CHECKSIGVERIFY, OP_1, cust1_public_key, cust2_public_key, cust3_public_key, OP_3, OP_CHECKMULTISIG
]
######################################################################

if __name__ == '__main__':
    ######################################################################
    # TODO: set these parameters correctly
    amount_to_send = 0.00075 # amount of BTC in the output you're sending minus fee
    txid_to_spend = (
        'f1f09b814be0de094c7d7e5bf23f217d8f1bb29964eaf9363ec8940eba9bb6d8')
    utxo_index = 1 # index of the output you are spending, indices start at 0
    ######################################################################

    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, 
        utxo_index, Q3a_txout_scriptPubKey, my_private_key, network_type)
    print(response.status_code, response.reason)
    print(response.text)

'''
201 Created
{
  "tx": {
    "block_height": -1,
    "block_index": -1,
    "hash": "7abe5262ed4ec049012132a5799d1225f758425b979781efaa97396213c7f72c",
    "addresses": [
      "mv3a1ZqW2w1k2DR8R2tFqao51xkSSTsumc",
      "zJfbc1wtJ4b6qZjY7K9wDjt4G54LUxg7Dy"
    ],
    "total": 75000,
    "fees": 25000,
    "size": 307,
    "vsize": 307,
    "preference": "medium",
    "relayed_by": "2a0c:5c84:1:6001::bdfd",
    "received": "2021-10-12T04:34:13.511910735Z",
    "ver": 1,
    "double_spend": false,
    "vin_sz": 1,
    "vout_sz": 1,
    "confirmations": 0,
    "inputs": [
      {
        "prev_hash": "f1f09b814be0de094c7d7e5bf23f217d8f1bb29964eaf9363ec8940eba9bb6d8",
        "output_index": 1,
        "script": "483045022100b94d8ebd8c9550f1294a559a3408b98a5571fb38557737ff7dd25149857ce5de02202febf4f50d507d9ccf85c52eb8ecf36afdc9d727cacce98fe69df1417c899ba60121036ff950c5002fb35639223a911fe4f663c599882388fbd9d1911087b7e89b7fee",
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
        "value": 75000,
        "script": "21036ff950c5002fb35639223a911fe4f663c599882388fbd9d1911087b7e89b7feead512102d14c3bceb217d76b99805689428fb688bb47d53a940c36930080cced7dccd13921033d7550904cb4d725b5465ea4c3da641120a121c4ed62b59dcf824492fd2c8cab2102e017d1f8cc42046b1b367238c483af2302f0b9c084d231eacd5f267cf8f0a48d53ae",
        "addresses": [
          "zJfbc1wtJ4b6qZjY7K9wDjt4G54LUxg7Dy"
        ],
        "script_type": "pay-to-multi-pubkey-hash"
      }
    ]
  }
}
'''
