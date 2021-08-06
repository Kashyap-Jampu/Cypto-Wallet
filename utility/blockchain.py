from utility.block import Block
import hashlib as hl
import json
from utility.verification import Verification
from utility.transaction import Transaction



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


class Blockchainn():


#blocks

    def __init__(self,public_key):
        genesis_block=Block(0, '', [], 100, 0)
        self.blockchain=[genesis_block]
        self.opentransactions=[]
        self.public_key=public_key
        self.load_data()

    def load_data(self):
        block_chain=Blockchain.objects.get().totalblockchain
        if block_chain=="":
            block_chain=[]
        else:
            block_chain = json.loads(blockchain)
        op_tx=Blockchain.objects.get().open_transactions
        if op_tx=="":
            op_tx=[]
        else:
            op_tx = json.loads(op_tx)
        for block in block_chain:
            converted_tx=[]
            for tx in block['transactions']:
                 converted_tx.append(Transaction(tx['sender'],tx['recipient'],tx['signature'],tx['amount']) )


            updated_block = Block(block['index'],block['previous_hash'],converted_tx,block['proof'],block['timestamp'])
            self.blockchain.append(updated_block)
        converted_tx=[]
        for tx in op_tx:
             converted_tx.append(Transaction(tx['sender'],tx['recipient'],tx['signature'],tx['amount']) )
        self.opentransactions=converted_tx[:]

    def save_data(self):
        saveable_chain=[]
        for block in self.blockchain:
            tx_arr=[]
            for tx in block.transaction:
                tx_arr.append(tx.__dict__)
            saveable_chain.append(Block(block.index,block.previous_hash,tx_arr,block.proof,block.timestamp).__dict__)


        block_chain=json.dumps(saveable_chain)

        saveable_tx=[]
        for tx in self.opentransactions:
            saveable_tx.append(tx.__dict__)
        op_tx=json.dumps(saveable_tx)



        block_chain_2=Blockchain(totalblockchain=block_chain,open_transaction=op_tx)
        block_chain_2.save()
        return True





    def add_transaction(self,sender,recevier,amount,sign):

        transaction=Transaction(sender,recipient,amount,sign)
        if get_balance(sender)<amount:
            print("insuff balance")
            return False
        else:
            public_key = RSA.importKey(binascii.unhexlify(transaction.sender))
            verifier = PKCS1_v1_5.new(self.public_key)

            self.opentransations.append(transation)
            if self.save_data():
                return True
            else:
                print("cannot save")
                return False
    def get_balance(self,sender):
        balance=0
        for block in self.blockchain:
            for transation in block.transactions:
                if transaction.receiver==sender:
                    balance+=transation.amount
                elif transaction.sender==sender:
                    balance=-transaction.amount
        for transaction in self.opentransactions:
                if transaction.sender==sender:
                    balance=-transaction.amount
        print(balance)
        return balance
    def mine(self):
        if len(self.opentransations)==0:
            return
        last_block=self.blockchain[-1]
        hashed_block=hash_block(last_block)
        proof=self.proof_of_work(hashed_block)
        reward_transaction = Transaction(
            'MINING', self.public_key, '', MINING_REWARD)
        copied_transactions = self.opentransactions[:]
        verification=Verification()
        for tx in copied_transactions:
            if not verification.verify_sign(tx):
                print(" mine failed")
                return False
        copied_transactions.append(reward_transaction)
        block = Block(len(self.blockchain), hashed_block,
                      copied_transactions, proof)
        self.blockchain.append(block)
        self.opentransactions = []
        if self.save_data():
            return True




    def proof_of_work(self,hashed_block):
        """Generate a proof of work for the open transactions, the hash of the
        previous block and a random number (which is guessed until it fits)."""
        last_hash = hashed_block
        proof = 0
        # Try different PoW numbers and return the first valid one
        while not Verification.valid_proof(
            self.opentransactions,
            last_hash, proof
        ):
            proof += 1
        return proof
