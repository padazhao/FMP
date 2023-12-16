from bardapi import BardCookies
import pandas as pd
import time
from cryptography.fernet import Fernet
import ipfshttpclient

# encode and upload file to IPFS
# create key
# key = "password"
# cipher_suite = Fernet(key)

# byte data to encrypt
# data_to_encrypt = open('data', 'rb').read()

# encrypt
# encrypted_data = cipher_suite.encrypt(data_to_encrypt)

# link to local ipfs
# api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

# upload data to IPFS and obtain cid
# result = api.add_bytes(encrypted_data)
# cid = result['Hash']

# bard api setting
cookie_dict = {
    "__Secure-1PSID": "xxxxxx.",
    "__Secure-1PSIDTS": "xxxxx",
    "__Secure-1PSIDCC": "xxxxxxx"
}

bard = BardCookies(cookie_dict=cookie_dict)


# according to different types of dataset, give the prompt and example.
# all files exist with csv style.
# my_data = pd.read_csv('')
# input_text = ""
# answer = bard.get_answer(f'{input_text} this data {my_data}')['content']
# 1.Numeric Data
# Description: Sea State
# url:https://data.world/us-doe-gov/0ba2293a-48b7-4dd5-9d9f-5e8e5710545c/workspace/project-summary?agentid=us-doe-gov&datasetid=0ba2293a-48b7-4dd5-9d9f-5e8e5710545c

# 2.Categorical data
# decription: This data set consists of three types of entities
# url: https://data.world/uci/automobile/workspace/project-summary?agentid=uci&datasetid=automobile

# 3.Image Data
# locate in images file
# image = open('img.png', 'rb').read()
# bard_answer = bard.ask_about_image("what is in the image?", image)
# print(bard_answer['content'])

# 4.Text Data
# url: https://www.kaggle.com/datasets/shivamkushwaha/bbc-full-text-document-classification
# description: BBC news?


# data=" "# pure text
# description = "William Shakespeare poem"
# prompt = "Compare the following dataset with its description and provide a similarity score, only give the score:\nDataset: "+data+"\nDescription:"+description
# print(bard.get_answer(prompt))

# 5.Audio Data : usually transcribe audio into text format.


# data = """
# Tyger Tyger, burning bright,
# In the forests of the night;
# What immortal hand or eye,
# Could frame thy fearful symmetry?
# """
# true
#        FROM off a hill whose concave womb reworded
# A plaintful story from a sistering vale,
# My spirits to attend this double voice accorded,
# And down I laid to list the sad-tuned tale;
# Ere long espied a fickle maid full pale,
# Tearing of papers, breaking rings a-twain,
# Storming her world with sorrow's wind and rain.
#
# Upon her head a platted hive of straw,
# Which fortified her visage from the sun,
# Whereon the thought might think sometime it saw
# The carcass of beauty spent and done:
# Time had not scythed all that youth begun,
# Nor youth all quit; but, spite of heaven's fell rage,
# Some beauty peep'd through lattice of sear'd age.
# """
# description = "William Shakespeare poem"
# # description = "Tiger poem"
# prompt = "Compare the following dataset with its description and provide a similarity score, only give the score:\nDataset: " + data + "\nDescription:" + description
#
# print(bard.get_answer(prompt)['content'])


# obtain the smart contract data
# the buyer use the offchain LLM to evaluate the dataset
#
def evaluate_data(cid, data_type, description):
    similarity_score = 1.00
    if data_type == 1:
        similarity_score = evaluate_numeric_data(cid, description)
    if data_type == 2:
        similarity_score = evaluate_categorical_data(cid, description)
    if data_type == 3:
        similarity_score = evaluate_image_data(cid, description)
    if data_type == 4:
        similarity_score = evaluate_text_data(cid, description)
    return similarity_score
def evaluate_numeric_data(cid, description):
    # use cid to find file
    # decode_save_file(cid, "csv")
    my_data = pd.read_csv('NumericDataset3.csv')
    description = description
    input_text = "Compare the following dataset with its description and provide a similarity score, only give the " \
                 "score:"

    answer = bard.get_answer(f'{input_text} description {description} this data {my_data} ')['content']
    return answer


def evaluate_text_data(cid, description):
    # use cid to find file
    # decode_save_file(cid, "txt")
    # Open the file in read mode
    with open('text/textDataset3.txt', 'r') as file:
        # Read the entire content of the file
        file_content = file.read()
    data = file_content  # pure text
    description = description
    input_text = "Compare the following dataset with its description and provide a similarity score, only give the " \
                 "score:"

    answer = bard.get_answer(f'{input_text} description {description} this data {data} ')['content']
    return answer


def evaluate_image_data(cid, description):
    # use cid to find file
    # decode_save_file(cid, "png")
    image = open('images/cat.png', 'rb').read()
    bard_answer = bard.ask_about_image(
        "Give the similarity score only the score, do not type other information, only return one value of similarity score for the image and the description" + description,
        image)
    return bard_answer['content']


def evaluate_categorical_data(cid, description):
    # use cid to find file
    # decode_save_file(cid, "csv")
    my_data = pd.read_csv('CategoricalDataset3.csv')
    description = description
    input_text = "Compare the following dataset with its description and provide a similarity score, only give the " \
                 "score:"

    answer = bard.get_answer(f'{input_text} description {description} this data {my_data} ')['content']
    return answer


# download file from ipfs
# def download_file_from_ipfs(cid):
#     return api.cat(cid)
#
#
# # decode and save as can evaluate file
# def decode_save_file(cid, filename_extension):
#     data = download_file_from_ipfs(cid)
#     decrypted_data = cipher_suite.decrypt(data)
#     with open("file." + filename_extension, "wb") as f:
#         f.write(decrypted_data)


data_type = "1"
data_description = """
This is a dataset about the numeric sea state
"""
data_cid = "1"
data_description1 = """
This a dataset about the categorical sea type

"""
data_description2 = """
This is a cat.

"""
data_description3 = """
It describes a story named Tom.

"""
start = time.time()
print(evaluate_numeric_data(1, data_description))
end = time.time()
print("Evaluation time:", end - start, "s")

start = time.time()
print(evaluate_categorical_data(1, data_description1))
end = time.time()
print("Evaluation time:", end - start, "s")

start = time.time()
print(evaluate_image_data(1, data_description2))
end = time.time()
print("Evaluation time:", end - start, "s")

start = time.time()
print(evaluate_text_data(1, data_description3))
end = time.time()
print("Evaluation time:", end - start, "s")
