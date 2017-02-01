#!/usr/bin/python
# coding:  utf-8

from client import Client
from secmongo import SecMongo
from bson.json_util import dumps
from secmongo.index.avltree import AVLTree
from secmongo.index.encryptednode import EncryptedNode
from secmongo.crypto.ore import ORE
import re
import linecache
import json

#
# Input data
#
docs = [
    {
        "name": "John Snow",
        "age":  18,
        "address": "Castle Black, over a table",

    },
    {
        "name": "Eddard Stark",
        "age":  40,
        "address": "King's landing, in a spear",
    },
    {
        "name": "Catherine Stark",
        "age":  34,
        "address": "Hell, 123",
    },
    {
        "name": "Rob Stark",
        "age":  20,
        "address": "Hell, 124",
    },
    {
        "name": "Aria Stark",
        "age":  12,
        "address": "Braavos",
    },
    {
        "name": "Sansa Stark",
        "age":  16,
        "address": "North",
    },
    {
        "name": "Theon Greyjoy",
        "age":  19,
        "address": "No Dick's land",
    },
    {
        "name": "Tywin Lannister",
        "age":  55,
        "address": "King's landing",
    },
    {
        "name": "Cersei Lannister",
        "age":  35,
        "address": "King's landing",
    },
    {
        "name": "Jaime Lannister",
        "age":  35,
        "address": "King's landing",
    },
    {
        "name": "Robert Baratheon",
        "age":  41,
        "address": "King's landing",
    },
    {
        "name": "Joffrey Baratheon",
        "age":  17,
        "address": "King's landing",
    },
    {
        "name": "Lady Melissandre",
        "age":  201,
        "address": "Castle Black, naked",
    }
]
# Setup client
client = Client(Client.keygen())

client.set_attr("title", "static")
client.set_attr("year", "index")

# Setup the MongoDB driver
s = SecMongo(add_cipher_param=pow(client.ciphers["h_add"].keys["pub"]["n"], 2),
             url='mongodb://localhost:27017')
s.open_database("test_sec")
s.set_collection("gameofthrones2")
s.drop_collection()
s.load_scripts()

docs = []
for i in range(5000):
    data = json.loads(linecache.getline('movies.json', i+1))
    year = 0
    if data['year'] and data['year'][0]:
        year = int(data['year'][0])

    docs.append({'title': data['title'].encode('ascii','ignore'), 'year': year})

root = None

for doc in docs[:5000]:
    enc_doc = client.encrypt(doc)
    inserted_doc = s.insert(enc_doc)
    node = EncryptedNode(client.ciphers["index"].encrypt(doc["year"]),
                         inserted_doc)
    s.insert_index(node)

result = [client.decrypt(x)["title"] for x in s.find()]

print("")
print("Movie from 2015:")
for doc in s.find(index=client.get_ctL(2015)):
    print(client.decrypt(doc))
    # pass
