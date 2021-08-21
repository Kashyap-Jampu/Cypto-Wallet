
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
import binascii
import Crypto.Random
from Crypto.Hash import SHA256
import json
import hashlib as hl
"""Provides verification helper methods."""

def hash_string_256(string):
    """Create a SHA256 hash for a given input string.

    Arguments:
        :string: The string which should be hashed.
    """
    return hl.sha256(string).hexdigest()


def hash_block(block):
    """Hashes a block and returns a string representation of it.

    Arguments:
        :block: The block that should be hashed.
    """
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [
        tx.to_ordered_dict() for tx in hashable_block['transactions']
    ]
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())

class Verification:
    """A helper class which offer various static and class-based verification
    and validation methods."""
    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        """Validate a proof of work number and see if it solves the puzzle
        algorithm (two leading 0s)

        Arguments:
            :transactions: The transactions of the block for which the proof
            is created.
            :last_hash: The previous block's hash which will be stored in the
            current block.
            :proof: The proof number we're testing.
        """
        # Create a string with all the hash inputs
        guess = (str([tx.to_ordered_dict() for tx in transactions]
                     ) + str(last_hash) + str(proof)).encode()
        # Hash the string
        # IMPORTANT: This is NOT the same hash as will be stored in the
        # previous_hash. It's a not a block's hash. It's only used for the
        # proof-of-work algorithm.
        guess_hash = hash_string_256(guess)
        # Only a hash (which is based on the above inputs) which starts with
        # two 0s is treated as valid
        # This condition is of course defined by you. You could also require
        # 10 leading 0s - this would take significantly longer (and this
        # allows you to control the speed at which new blocks can be added)
        return guess_hash[0:2] == '00'

    @classmethod
    def verify_chain(cls, blockchain):
        """ Verify the current blockchain and return True if it's valid, False
        otherwise."""
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not cls.valid_proof(block.transactions[:-1],
                                   block.previous_hash,
                                   block.proof):
                print('Proof of work is invalid')
                return False
        return True

    @staticmethod
    def verify_sign(transaction):
        public_key = RSA.importKey(binascii.unhexlify(transaction.sender))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA256.new((str(transaction.sender) + str(transaction.recipient) +
                        str(transaction.amount)).encode('utf8'))
        print(verifier.verify(h,str(binascii.unhexlify(transaction.sign))))
        return verifier.verify(h, binascii.unhexlify(transaction.sign))

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        """Verifies all open transactions."""
        return all([cls.verify_transaction(tx, get_balance, False)
                    for tx in open_transactions])
