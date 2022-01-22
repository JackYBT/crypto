from bitcoin.core.script import *

######################################################################
# These functions will be used by Alice and Bob to send their respective
# coins to a utxo that is redeemable either of two cases:
# 1) Recipient provides x such that hash(x) = hash of secret
#    and recipient signs the transaction.
# 2) Sender and recipient both sign transaction
#
# TODO: Fill these in to create scripts that are redeemable by both
#       of the above conditions.
# See this page for opcode documentation: https://en.bitcoin.it/wiki/Script

# This is the ScriptPubKey for the swap transaction
def coinExchangeScript(public_key_sender, public_key_recipient, hash_of_secret):
    return [
        
        #Checks whether or not the recipient knows the hash of secret and has the right signature
        OP_IF, OP_HASH160, hash_of_secret, OP_EQUALVERIFY, public_key_recipient, OP_CHECKSIG,
        
        #If the first condition doesn't work out, then it checks if the 2 out of 2 multisig is satisfied
        OP_ELSE, 2,
        public_key_sender, public_key_recipient, 
        2, OP_CHECKMULTISIG, OP_ENDIF
    ]

#Assuming the stack looks

# This is the ScriptSig that the receiver will use to redeem coins
def coinExchangeScriptSig1(sig_recipient, secret):
    return [
        sig_recipient, secret, OP_TRUE
    ]

# This is the ScriptSig for sending coins back to the sender if unredeemed
def coinExchangeScriptSig2(sig_sender, sig_recipient):
    return [
        OP_0, sig_sender, sig_recipient, OP_FALSE
    ]
######################################################################

######################################################################
#
# Configured for your addresses
#
# TODO: Fill in all of these fields
#

alice_txid_to_spend     = "23eccbb1031b72db3e5ce13e5fbce1e81d6dd24bc56f7203374fbf7af8ed7c34"
alice_utxo_index        = 0
alice_amount_to_send    = 0.0008

bob_txid_to_spend       = "d76a01071bc11f72ca81b0189d3daea470cb74963996ec13171f7f7447851c5c"
bob_utxo_index          = 0
bob_amount_to_send      = 0.0009

# Get current block height (for locktime) in 'height' parameter for each blockchain (will be used in swap.py):
#  curl https://api.blockcypher.com/v1/btc/test3
btc_test3_chain_height  = 1579945

#  curl https://api.blockcypher.com/v1/bcy/test
bcy_test_chain_height   = 2548698

# Parameter for how long Alice/Bob should have to wait before they can take back their coins
# alice_locktime MUST be > bob_locktime
alice_locktime = 5
bob_locktime = 3

tx_fee = 0.0001

# While testing your code, you can edit these variables to see if your
# transaction can be broadcasted succesfully.
broadcast_transactions = False
alice_redeems = False

######################################################################
