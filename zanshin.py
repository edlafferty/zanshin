# Develop a blockchain
# Initialize the chain
from functools import reduce
from collections import OrderedDict
from colorama import Fore, Style
import hashlib as hl
import json
import pickle

from hash_util import create_hash_256, hash_block

# The reward to give to miners
MINING_REWARD = 10

blockchain = []
open_transactions = []
owner = "EdLaff"
participants = {"EdLaff"}


def save_data():
    """Write blockchain and any open transactions to a file"""
    # use pickle format and methods to save data. Data is stored in binary
    # with open('blockchain.p', mode='wb') as bc_data:
    #     save_data = {
    #         'chain': blockchain,
    #         'ot': open_transactions
    #     }
    #     bc_data.write(pickle.dumps(save_data))
    # use json library and methods to save data. Data is stored in plain text
    try:
        with open('blockchain.data', mode='w') as bc_data:
            bc_data.write(json.dumps(blockchain))
            bc_data.write("\n")
            bc_data.write(json.dumps(open_transactions))
        # 'with' command will auto close the file object, so no need to call the close method
    except(IOError):
        print('File save error!')


def load_data():
    global blockchain
    global open_transactions
    try:
        """Read blockchain data file and load it into blockchain object"""
        # use pickle library and methods to load data from binary file
        # with open('blockchain.p', mode='rb') as bc_data:
        #     file_content = pickle.loads(bc_data.read())
        #     blockchain = file_content['chain']
        #     open_transactions = file_content['ot']
        # use json library and methods to load data from text file
        with open('blockchain.data', mode='r') as bc_data:
            bc_data_content = bc_data.readlines()
            blockchain = json.loads(bc_data_content[0][:-1])
            updated_blockchain = []
            for block in blockchain:
                updated_block = {
                    'prev_block_hash': block['prev_block_hash'],
                    'index': block['index'],
                    'proof': block['proof'],
                    'transactions': [OrderedDict(
                        [('sender', tx['sender']),
                        ('recipient', tx['recipient']),
                        ('amount', tx['amount'])]) for tx in block['transactions']]
                }
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain    
            open_transactions = json.loads(bc_data_content[1])
            updated_open_transactions = []
            for tx in open_transactions:
                updated_open_tx = OrderedDict(
                [('sender', tx['sender']),
                ('recipient', tx['recipient']),
                ('amount', tx['amount'])])
                updated_open_transactions.append(updated_open_tx)
            open_transactions = updated_open_transactions    
        # 'with' command will auto close the file object, so no need to call the close method
    except(IOError):
        # The initial block in the chain
        genesis_block = {
            "prev_block_hash": "", 
            "index": 0, 
            "transactions": [],
            "proof": 100
        }
        blockchain = [genesis_block]
        open_transactions = []


load_data()


def valid_proof(transactions, last_hash, proof):
    # Create a string w/ the hash inputs
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    # Hash the string. This is not the hash that is stored in the chain! This is proof of work
    guess_hash = create_hash_256(guess)
    #print("valid_proof hash: ", guess_hash)
    return guess_hash[0:2] == '00'


def proof_of_work():
        last_block = blockchain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not valid_proof(open_transactions, last_hash, proof):
            proof += 1
        return proof


def get_balance(participant):
    # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
    # This fetches sent amounts of transactions that were already included in blocks of the blockchain
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
    # This fetches sent amounts of open transactions (to avoid double spending)
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    #amount_sent = 0
    #for tx in tx_sender:
    #    if len(tx) > 0:
    #        amount_sent += tx[0]
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    #amount_received = 0
    #for tx in tx_recipient:
    #    if len(tx) > 0:
    #        amount_received += tx[0]
    return amount_received - amount_sent

def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient, sender=owner, amount=1.0):
    """ Appends the passed value and the last blockchain value to the current blockchain 

    Arguments:
        :sender: Sender of coins
        :recipient: Recipient of transaction
        :amount: Value of transaction
    """
    #transaction = {
    #    'sender': sender, 
    #    "recipient": recipient, 
    #    "amount": amount
    #}
    transaction = OrderedDict(
        [('sender', sender),
        ('recipient', recipient),
        ('amount', amount)]
    )
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(recipient)
        participants.add(sender)
        save_data()
        return True
    return False
    


def mine_block():
    """Create a new block and add open transactions to it."""
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    # reward_transaction = {
    #     'sender': 'MINING',
    #     'recipient': owner,
    #     'amount': MINING_REWARD
    # }
    reward_transaction = OrderedDict(
        [('sender', 'MINING'),
        ('recipient', owner),
        ('amount', MINING_REWARD)]
    )
    # Work on a copy of open_transactions, not the REAL one
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        "prev_block_hash": hashed_block, 
        "index": len(blockchain), 
        "transactions": copied_transactions,
        "proof": proof
    }
    blockchain.append(block)
    return True


def get_transaction_data():
    """ Requests and returns transaction amount from the user (as a float)"""
    trans_recipient = input("Enter the transaction recipient: ")
    trans_amount = float(input("Your transaction amount please: "))
    return (trans_recipient, trans_amount)


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']
    

def print_blockchain():
    # Output bloclchain
    for block in blockchain:
        print('Outputting Block')
        print(block)
    else:
        print("-" * 20)

def verify_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block["prev_block_hash"] != hash_block(blockchain[index-1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['prev_block_hash'], block['proof']):
            print("Proof of work is invalid!")
            return False
    return True


def verify_open_transactions():
    is_valid = True
    for tx in open_transactions:
        if verify_transaction(tx):
            is_valid = True
        else:
            is_valid = False
    return is_valid


def get_user_choice():
    user_input = input("Your choice: ")
    return user_input

waiting_for_input = True

while waiting_for_input:
    print("Please choose:")
    print("1: Add transaction amount")
    print("2: Mine a new block")
    print("3: Output blockchain blocks")
    print("4: Output participants")
    print("5: Check transaction validity")
    print("h: Manipulate the chain")
    print("q: Quit")
    print("")
    user_choice = get_user_choice()
    if user_choice == "1":
        trans_data = get_transaction_data()
        recipient, amount = trans_data
        if add_transaction(recipient, amount=amount):
            print("Added transaction")
        else:
            print("Transaction failed")
        #print(open_transactions)
    elif user_choice == "2":
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == "3":
        print_blockchain()
    elif user_choice == "4":
        print(participants)
    elif user_choice == "5":
        if verify_open_transactions():
            print("All transactions are valid")
        else:
            print("There are invalid transactions")
    elif user_choice == "h":
        if len(blockchain) >= 1:
            blockchain[0] = {
                "prev_block_hash": "", 
                "index": 0, 
                "transactions": [{"sender": "Joe", "recipient": "Ed", "amount": 500.0}]
            }
    elif user_choice == "q":
        waiting_for_input = False
    else:
        print("Invalid input. Please choose from options provided.")
    if not verify_chain():
        print_blockchain()
        print("Blockchain is invalid!!")
        break
    print('{}\'s balance: {:5.2f}'.format('EdLaff', get_balance('EdLaff')))
else:
    print("User left")
print("Done")
