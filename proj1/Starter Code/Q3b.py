from sys import exit
from bitcoin.core.script import *

from lib.utils import *
from lib.config import (my_private_key, my_public_key, my_address,
                    faucet_address, network_type)
from Q1 import P2PKH_scriptPubKey
from Q3a import (Q3a_txout_scriptPubKey, cust1_private_key, cust2_private_key,
                  cust3_private_key)


def multisig_scriptSig(txin, txout, txin_scriptPubKey):
    bank_sig = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey,
                                             my_private_key)
    cust1_sig = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey,
                                             cust1_private_key)
    cust2_sig = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey,
                                             cust2_private_key)
    cust3_sig = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey,
                                             cust3_private_key)
    ######################################################################
    # TODO: Complete this script to unlock the BTC that was locked in the
    # multisig transaction created in Exercise 3a.
    return [
        OP_0, cust1_sig, bank_sig
    ]
    ######################################################################


def send_from_multisig_transaction(amount_to_send, txid_to_spend, utxo_index,
                                   txin_scriptPubKey, txout_scriptPubKey, network):
    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = multisig_scriptSig(txin, txout, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx, network)

if __name__ == '__main__':
    ######################################################################
    # TODO: set these parameters correctly
    amount_to_send = 0.0005 # amount of BTC in the output you're sending minus fee
    txid_to_spend = (
        '7abe5262ed4ec049012132a5799d1225f758425b979781efaa97396213c7f72c')
    utxo_index = 0 # index of the output you are spending, indices start at 0
    ######################################################################

    txin_scriptPubKey = Q3a_txout_scriptPubKey
    txout_scriptPubKey = P2PKH_scriptPubKey(faucet_address)

    response = send_from_multisig_transaction(
        amount_to_send, txid_to_spend, utxo_index,
        txin_scriptPubKey, txout_scriptPubKey, network_type)
    print(response.status_code, response.reason)
    print(response.text)
'''
201 Created
{
  "tx": {
    "block_height": -1,
    "block_index": -1,
    "hash": "998dfad2d7b85bf727c23865f05c78043e469cbfa7f9c696fee0d0225cba6134",
    "addresses": [
      "zJfbc1wtJ4b6qZjY7K9wDjt4G54LUxg7Dy",
      "mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB"
    ],
    "total": 50000,
    "fees": 25000,
    "size": 231,
    "vsize": 231,
    "preference": "high",
    "relayed_by": "2a0c:5c84:1:6001::bdfd",
    "received": "2021-10-12T04:35:32.297629856Z",
    "ver": 1,
    "double_spend": false,
    "vin_sz": 1,
    "vout_sz": 1,
    "confirmations": 0,
    "inputs": [
      {
        "prev_hash": "7abe5262ed4ec049012132a5799d1225f758425b979781efaa97396213c7f72c",
        "output_index": 0,
        "script": "0047304402205b145094ec380095ce8372abe9d6ec1aba7960f03df78435502f2dad21dabf67022038281046eedb39df860d820048c0d9b906e85b0ac7c6a8d4b89c3209a8321f55014830450221009307a2f1a89a2876e6f3e9adeb0bcb27e9a083d328a4c172ac8e3166ee1cd6800220650aa97d530691ce72e736df166a719152f299837461064a3418ccbe36d22b8001",
        "output_value": 75000,
        "sequence": 4294967295,
        "addresses": [
          "zJfbc1wtJ4b6qZjY7K9wDjt4G54LUxg7Dy"
        ],
        "script_type": "pay-to-multi-pubkey-hash",
        "age": 0
      }
    ],
    "outputs": [
      {
        "value": 50000,
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