import functools
#Initialize the mining reward for block miner
MINING_REWARD = 10

# Initializing our (empty) blockchain list
genesis_block={
"previous_hash":"",
"index":0,
"transactions":[]
}
blockchain = []
blockchain.append(genesis_block)
open_transactions=[]
owner="Max"
participants={"Max"}

def get_last_blockchain_value():
    """ Returns the last value of the current blockchain. """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

# This function accepts two arguments.
# One required one (transaction_amount) and one optional one (last_transaction)
# The optional one is optional because it has a default value => [1]


def add_transaction(recipient,sender=owner, amount=1.0):
    """ Append a new value as well as the last blockchain value to the blockchain.

    Arguments:
        :transaction_amount: The amount that should be added.
        :last_transaction: The last blockchain transaction (default [1]).
    """
    transction={"sender":sender,
        "recipient":recipient,
        "amount":amount}
    if verify_transaction(transction):
        open_transactions.append(transction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False

def hash_block(block):
    return "-".join([str(block[key]) for key in block])

def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    print(tx_sender)
    # Calculate the total amount of coins sent
    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    # This fetches received coin amounts of transactions that were already included in blocks of the blockchain
    # We ignore open transactions here because you shouldn't be able to spend coins before the transaction was confirmed + included in a block
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    # Return the total balance
    return amount_received - amount_sent



def verify_transaction(transction):
    """
    Check if the sender has sufficient amount
    """
    sender_balance=get_balance(transction["sender"])
    return sender_balance>=transction["amount"]

def verify_transactions():
    """
    Verify all the transactions
    """
    return all([verify_transaction(t) for t in open_transactions])


def mine_block():
    last_block=blockchain[-1]
    hashed_block=hash_block(last_block)
    #print(hashed_block)
    reward_transaction={
    "sender":"MINING",
    "recipient":owner,
    "amount":MINING_REWARD
    }

    copied_transactions=open_transactions[:]
    copied_transactions.append(reward_transaction)
    block={
    "previous_hash":hashed_block,
    "index": len(blockchain),
    "transactions":copied_transactions
    }
    blockchain.append(block)
    return True


def get_transaction_value():
    """ Returns the input of the user (a new transaction amount) as a float. """
    # Get the user input, transform it from a string to a float and store it in user_input
    tx_recipient=input("Enter the recipient of the transaction: ")
    tx_amount = float(input('Your transaction amount please: '))
    return tx_recipient,tx_amount


def get_user_choice():
    """Prompts the user for its choice and return it."""
    user_input = input('Your choice: ')
    return user_input


def print_blockchain_elements():
    """ Output all blocks of the blockchain. """
    # Output the blockchain list to the console
    for block in blockchain:
        print('Outputting Block')
        print(block)
    else:
        print('-' * 20)


def verify_chain():
    """ Verify the current blockchain and return True if it's valid, False otherwise."""
    for (index,block) in enumerate(blockchain):
        if index==0:
            continue
        if block["previous_hash"]!=hash_block(blockchain[index-1]):
            return False
    return True



waiting_for_input = True

# A while loop for the user input interface
# It's a loop that exits once waiting_for_input becomes False or when break is called
while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print("2: Mine the new block")
    print('3: Output the blockchain blocks')
    print("4: Ouput the participants")
    print("5: Check transaction validity")
    print('h: Manipulate the chain')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        # Add the transaction amount to the blockchain
        recipient,amount=tx_data
        if add_transaction(recipient,amount=amount):
            print('Added transaction!')
        else:
            print('Transaction failed!')
        print(open_transactions)
    elif user_choice=="2":
        mine_block()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice=="4":
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions are valid')
        else:
            print('There are invalid transactions')
    elif user_choice == 'h':
        # Make sure that you don't try to "hack" the blockchain if it's empty
        if len(blockchain) >= 1:
            blockchain[0]={
            "previous_hash":"",
            "index":0,
            "transactions":{"sender":"Chufan","recipient":"Max","amount":100}
            }
    elif user_choice == 'q':
        # This will lead to the loop to exist because it's running condition becomes False
        waiting_for_input = False
    else:
        print('Input was invalid, please pick a value from the list!')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        # Break out of the loop
        break
    print("Balance of {} is {:6.2f}".format("Max",get_balance("Max")))
else:
    print('User left!')


print('Done!')
