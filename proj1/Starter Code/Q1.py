from bitcoin.core.script import *
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress

from lib.utils import *
from lib.config import (my_private_key, my_public_key, my_address,
                    faucet_address, network_type)


def P2PKH_scriptPubKey(address):
    ######################################################################
    # TODO: Complete the standard scriptPubKey implementation for a
    # PayToPublicKeyHash transaction
    
    #hash_address = address# Hash160(address)
    return [
        OP_DUP, OP_HASH160, address, OP_EQUALVERIFY, OP_CHECKSIG

    ]
    ######################################################################


def P2PKH_scriptSig(txin, txout, txin_scriptPubKey, private_key, public_key):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey,
                                             private_key)
    ######################################################################
    # TODO: Complete this script to unlock the BTC that was sent to you
    # in the PayToPublicKeyHash transaction.
    return [
        signature, public_key
    ]
    ######################################################################

def send_from_P2PKH_transaction(amount_to_send,
                                txid_to_spend,
                                utxo_index,
                                txout_scriptPubKey,
                                sender_private_key,
                                network):

    sender_public_key = sender_private_key.pub
    sender_address = P2PKHBitcoinAddress.from_pubkey(sender_public_key)

    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptPubKey = P2PKH_scriptPubKey(sender_address)
    txin = create_txin(txid_to_spend, utxo_index) #What does this do?
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey,
        sender_private_key, sender_public_key)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx, network)


if __name__ == '__main__':
    ######################################################################
    # TODO: set these parameters correctly
    amount_to_send = 0.00001 # amount of BTC in the output you're sending minus fee
    txid_to_spend = (
        'a71ef519b5bed984fdb4a1423ec27e6836bde4b9eff03e10a27a3f19ed8901bf')
    #Should this be different everytime then?
    #Were i previously transferred myself 0.001 BTC, there is a transaction ID for that specific transaction. There was one UTXO (index 0) that was "change" for the tranaction, and then there was another UTXO (index 1) taht was my 0.001 BTC.
    # I'm putting the unspent output Transaction ID from that one transaction: mv3a1ZqW2w1k2DR8R2tFqao51xkSSTsumc
    utxo_index = 1 # index of the output you are spending, indices start at 0
    ######################################################################

    txout_scriptPubKey = P2PKH_scriptPubKey(faucet_address)
    response = send_from_P2PKH_transaction(
        amount_to_send,
        txid_to_spend,
        utxo_index,
        txout_scriptPubKey,
        my_private_key,
        network_type,
    )
    print(response.status_code, response.reason)
    print(response.text)

    '''
    201 Created
{
  "tx": {
    "block_height": -1,
    "block_index": -1,
    "hash": "71487c7e20084a9faa7ed222e632493a2fb34a773a21d6d9ed1cc581001c10f2",
    "addresses": [
      "mv3a1ZqW2w1k2DR8R2tFqao51xkSSTsumc",
      "mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB"
    ],
    "total": 1000,
    "fees": 99000,
    "size": 192,
    "vsize": 192,
    "preference": "high",
    "relayed_by": "128.12.123.200",
    "received": "2021-10-11T20:57:22.621430328Z",
    "ver": 1,
    "double_spend": false,
    "vin_sz": 1,
    "vout_sz": 1,
    "confirmations": 0,
    "inputs": [
      {
        "prev_hash": "a71ef519b5bed984fdb4a1423ec27e6836bde4b9eff03e10a27a3f19ed8901bf",
        "output_index": 1,
        "script": "4830450221008359b360049ea6665489b094f74d3f40e638d2449a4349d99d8b00b14495082a02207a53dc974c70b5de5f067d31597661502f882f0585a1cab2793c7350782f142e0121036ff950c5002fb35639223a911fe4f663c599882388fbd9d1911087b7e89b7fee",
        "output_value": 100000,
        "sequence": 4294967295,
        "addresses": [
          "mv3a1ZqW2w1k2DR8R2tFqao51xkSSTsumc"
        ],
        "script_type": "pay-to-pubkey-hash",
        "age": 2098428
      }
    ],
    "outputs": [
      {
        "value": 1000,
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
