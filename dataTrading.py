from web3 import Web3
import json
import time
import evaluateDataWithBard

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"  # Update with your Ganache URL
web3 = Web3(Web3.HTTPProvider(ganache_url))
# # Set up your gas parameters based on your requirements
gas_limit = 300000  # Adjust based on the complexity of your transaction
gas_price = web3.to_wei('50', 'gwei')  # Adjust based on network conditions

# Load contract ABIs
with open("DataProduct.json", "r") as file:
    data_product_abi = json.load(file)["abi"]

with open("DataTradingSmartContract.json", "r") as file:
    data_trading_abi = json.load(file)["abi"]

# Replace the following addresses with the deployed contract addresses
data_product_address = "xxxxx"
data_trading_address = "xxxx"

# # Set the default account (use one of your Ganache accounts)
account0 = web3.eth.accounts[0]
account1 = web3.eth.accounts[1]

start = time.time()

data_type = "1"
data_description = """
This data set contains four measurements of sea state: frequency, spectral amplotude, phase, and wavenumber. These sea states are extrapolated from conditions near Humboldt Bay, California. A total of five hundred rows and four columns

"""
data_cid = "1"
print(evaluateDataWithBard.evaluate_data(data_cid, data_type, data_description))
result = int(evaluateDataWithBard.evaluate_data(data_cid, data_type, data_description) * 100)
print(result)
end = time.time()
print("Evaluation time:", end - start, "s")


def set_similarity_score(data_trading_contract):
    result = int(evaluateDataWithBard.evaluate_data(data_cid, data_type, data_description) * 100)
    print(result)
    tx_hash = data_trading_contract.functions.setSimilarityScore(result).transact()
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Similarity Score Set:", receipt)


def test_SetSim_contracts(data_product_address, data_trading_address):
    # Create contract instances
    # data_product_contract = web3.eth.contract(abi=data_product_abi, address=data_product_address)
    data_trading_contract = web3.eth.contract(abi=data_trading_abi, address=data_trading_address)
    set_similarity_score(data_trading_contract)


# test_SetSim_contracts(data_product_address, data_trading_address)


# Deploy DataProduct contract
def deploy_data_product_contract():
    data_product_contract = web3.eth.contract(abi=data_product_abi, bytecode=data_product_abi["bytecode"])
    tx_hash = data_product_contract.constructor().transact()
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    data_product_address = tx_receipt["contractAddress"]
    print("DataProduct Contract Deployed at:", data_product_address)
    return data_product_address


# Deploy DataTradingSmartContract contract
def deploy_data_trading_contract(data_product_address):
    data_trading_contract = web3.eth.contract(abi=data_trading_abi, bytecode=data_trading_abi["bytecode"])
    tx_hash = data_trading_contract.constructor(data_product_address, account0,
                                                account1).transact()
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    data_trading_address = tx_receipt["contractAddress"]
    print("DataTradingSmartContract Contract Deployed at:", data_trading_address)
    return data_trading_address


# Interact with DataProduct and DataTradingSmartContract contracts
def test_contracts(data_product_address, data_trading_address):
    # Create contract instances
    data_product_contract = web3.eth.contract(abi=data_product_abi, address=data_product_address)
    data_trading_contract = web3.eth.contract(abi=data_trading_abi, address=data_trading_address)

    # Test functions
    upload_data_product(data_product_contract)
    initiate_data_purchase(data_trading_contract)
    pay_for_data_product(data_trading_contract)
    confirm_data_received(data_trading_contract)
    confirm_data_receipt(data_trading_contract)
    evaluate_data(data_trading_contract)
    set_similarity_score(data_trading_contract)
    withdraw_deposit(data_trading_contract)


# Example functions to interact with the contracts
def upload_data_product(data_product_contract):
    # test  : numeric dataset directly do not use to upload and download
    tx_hash = data_product_contract.functions.uploadDataProduct(
        "1",
        "It is the Sea State dataset.",
        "1",
        "SampleData",
        web3.to_wei(1, "ether")
    ).transact({"from": account0, "value": web3.to_wei(1, "ether"), "gas": gas_limit, "gasPrice": gas_price})
    # tx_hash = data_product_contract.functions.uploadDataProduct(
    #     "2",
    #     "This data set consists of three types of entities.",
    #     "IPFSCID",
    #     "SampleData",
    #     web3.toWei(1, "ether")
    # ).transact()
    #
    # tx_hash = data_product_contract.functions.uploadDataProduct(
    #     "3",
    #     "This image contains a cat.",
    #     "IPFSCID",
    #     "SampleData",
    #     web3.toWei(1, "ether")
    # ).transact()
    #
    # tx_hash = data_product_contract.functions.uploadDataProduct(
    #     "4",
    #     "It is about bbu business.",
    #     "IPFSCID",
    #     "SampleData",
    #     web3.toWei(1, "ether")
    # ).transact()
    #
    # tx_hash = data_product_contract.functions.uploadDataProduct(
    #     "Video",
    #     "Description",
    #     "IPFSCID",
    #     "SampleData",
    #     web3.toWei(1, "ether")
    # ).transact()
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Data Product Uploaded:", receipt)


def initiate_data_purchase(data_trading_contract):
    dataProductCID = "1"
    buyerAdress = account1
    tx_hash = data_trading_contract.functions.initiateDataPurchase(
        dataProductCID,
        buyerAdress
    ).transact()
    return_values = tx_hash
    data_type, data_description, data_cid = return_values
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Data Purchase Initiated:", receipt)


def pay_for_data_product(data_trading_contract):
    value = data_trading_contract.functions.dataDeposit().call() + data_trading_contract.functions.dataProductPrice().call()
    tx_hash = data_trading_contract.functions.payForDataProduct().transact({'value': value})
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Data Product Paid:", receipt)


def confirm_data_received(data_trading_contract):
    tx_hash = data_trading_contract.functions.confirmDataReceived(True).transact()
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Data Received Confirmed:", receipt)


def confirm_data_receipt(data_trading_contract):
    tx_hash = data_trading_contract.functions.confirmDataReceipt(True).transact()
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Data Receipt Confirmed:", receipt)


def evaluate_data(data_trading_contract):
    data_trading_contract.functions.evaluateData().transact()


def withdraw_deposit(data_trading_contract):
    tx_hash = data_trading_contract.functions.withdrawDeposit().transact()
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Deposit Withdrawn:", receipt)

# Deploy contracts by using the remix online
# data_product_address = deploy_data_product_contract()
# data_trading_address = deploy_data_trading_contract(data_product_address)
# test
# test_contracts(data_product_address, data_trading_address)
# only use the python script interact with data trading SC setSimilarityScore to evaluate the dataset
