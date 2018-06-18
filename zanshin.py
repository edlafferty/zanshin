# Develop a blockchain
# Initialize the chain
blockchain = []


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(trans_amt, last_transaction=[1]):
    """ Appends the passed value and the last blockchain value to the current blockchain 

    Arguments:
        :trans_amt: The amount of the transaction
        :last_transaction: The last blockchain transaction (default [1])"""
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, trans_amt])


def get_transaction_amount():
    """ Requests and returns transaction amount from the user (as a float)"""
    user_input = float(input("Your transaction amounnt please: "))
    return user_input

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
    print("2: Output blockchain blocks")
    print("h: Manipulate the chain")
    print("q: Quit")
    print("")
    user_choice = get_user_choice()
    if user_choice == "1":
        tx_amount = get_transaction_amount()
        add_transaction(tx_amount, get_last_blockchain_value())
    elif user_choice == "2":
        print_blockchain()
    elif user_choice == "h":
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == "q":
        waiting_for_input = False
    else:
        print("Invalid input. Please choose from options provided.")
    if not verify_chain():
        print_blockchain()
        print("Blockchain is invalid!!")
        break
else:
    print("User left")
print("Done")
