'''
Created on 2018年11月7日

@author: sunrui
'''
from flask import Flask, request, json
import datetime
from block import Block

node = Flask(__name__)
this_nodes_transactions = []

def create_genesis_block():
    return Block(0,
                 datetime.datetime.now(),
                 {'proof-of-work': 17, 'transactions': []},
                 '0')

@node.route('/txion', methods=['POST'])
def transaction():
    if request.method == 'POST':
        new_txion = request.get_json()
        this_nodes_transactions.append(new_txion)
        print("New transaction")
        print("FROM: {}".format(new_txion['from']))
        print("TO: {}".format(new_txion['to']))
        print("AMOUNT: {}\n".format(new_txion['amount']))
        return "Transaction submission successful\n"

miner_address = 'random-miner-address'
def proof_of_work(last_proof):
    incrementor = last_proof + 1
    while not (incrementor % 17 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    return incrementor

@node.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain[-1]
    last_proof = last_block.data['proof-of-work']
    proof = proof_of_work(last_proof)
    this_nodes_transactions.append({'from': 'network',
                                    'to': miner_address,
                                    'amount': 1})
    mined_block = Block(last_block.index + 1,
                        datetime.datetime.now(),
                        {'proof-of-work': proof, 'transactions': list(this_nodes_transactions)},
                        last_block.hash)
    this_nodes_transactions[:] = []
    blockchain.append(mined_block)
    return json.dumps({'index': mined_block.index,
                       'timestamp': mined_block.timestamp,
                       'data': mined_block.data,
                       'hash': last_block.hash}) + '\n'

@node.route('/blocks', methods=['GET'])
def get_blocks():
    chain_to_send = []
    for block in blockchain:
        chain_to_send.append({'index': str(block.index),
                              'timestamp': str(block.timestamp),
                              'data': str(block.data),
                              'hash': str(block.hash)})
    return json.dumps(chain_to_send)

def find_new_chains():
    other_chains = []
    return other_chains

def consensus():
    global blockchain
    longest_chain = blockchain
    other_chains = find_new_chains()
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    blockchain = longest_chain

blockchain = [create_genesis_block()]
node.run('0.0.0.0')
