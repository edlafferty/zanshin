# Develop a blockchain
# Initialize the chain
genesis_block = {
    "prev_block_hash": "", 
    "index": 0, 
    "transactions": [] 
}
blockchain = [genesis_block]
open_transactions = []
owner = "EdLaff"

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
    transaction = {
        'sender': sender, 
        "recipient": recipient, 
        "amount": amount
    }
    open_transactions.append(transaction)
    


def mine_block():
    last_block = blockchain[-1]
    hashed_block = "-".join([str(last_block[key]) for key in last_block])
    print(hashed_block)
    # for keys in last_block:
    #     value = last_block[keys]
    #     hashed_block = hashed_block + str(value)
    block = {
        "prev_block_hash": hashed_block, 
        "index": len(blockchain), 
        "transactions": open_transactions
    }
    blockchain.append(block)

def get_transaction_data():
    """ Requests and returns transaction amount from the user (as a float)"""
    trans_recipient = input("Enter the transaction recipient: ")
    trans_amount = float(input("Your transaction amount please: "))
    return (trans_recipient, trans_amount)

def print_blockchain():
    # Output bloclchain
    for block in blockchain:
        print('Outputting Block')
        print(block)
    else:
        print("-" * 20)

def verify_chain():
    #block_index = 0
    chain_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        if blockchain[block_index][0] == blockchain[block_index - 1]:
            chain_valid = True
        else:
            chain_valid = False
            break
    
    # for block in blockchain:
    #     if block_index == 0:
    #         block_index += 1
    #         continue
    #     if block[0] == blockchain[block_index - 1]:
    #         chain_valid = True
    #     else:
    #         chain_valid = False
    #         break
    #     block_index += 1
    return chain_valid


def get_user_choice():
    user_input = input("Your choice: ")
    return user_input

waiting_for_input = True

while waiting_for_input:
    print("Please choose:")
    print("1: Add transaction amount")
    print("2: Mine a new block")
    print("3: Output blockchain blocks")
    print("h: Manipulate the chain")
    print("q: Quit")
    print("")
    user_choice = get_user_choice()
    if user_choice == "1":
        trans_data = get_transaction_data()
        recipient, amount = trans_data
        add_transaction(recipient, amount=amount)
        print(open_transactions)
    elif user_choice == "2":
        mine_block()
    elif user_choice == "3":
        print_blockchain()
    elif user_choice == "h":
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == "q":
        waiting_for_input = False
    else:
        print("Invalid input. Please choose from options provided.")
    # if not verify_chain():
    #     print_blockchain()
    #     print("Blockchain is invalid!!")
    #     break
else:
    print("User left")
print("Done")
