#Adam Sissoko
#Project 1 - CRUD MODULE - SUBLIME TEXT


import pymongo
from pymongo import MongoClient

import json
from bson.json_util import ObjectId
from bson.json_util import dumps, loads
from flask import Flask, jsonify

import csv
import pandas as pd


# CRUD module for accessing mongodb in Atlas at Mongodb.com
class CRUD(object):

	def __init__(self, client, db, col):
		self.cluster = MongoClient(client)
		self.db = self.cluster[db]
		self.collection = self.db[col]

	def mongoimport(self, csv_path, header):

	    """ Imports a csv file at path csv_name to a mongo colection
	    returns: count of the documants in the new collection
	    """
	    
	    # 'header' must mach the header of the csv doc
	    # to make things easier place csv file in same folder
	    csvfile = open(csv_path, 'r')
	    reader = csv.DictReader( csvfile )

	    for each in reader:
	    	row = {}
	    	for field in header:
	    		row[field]=each[field]

	    	self.collection.insert_one(row)

	#CREATE
	def create(self, data):
		s = json.dumps(data)	
		if data is None or data == {}:
			print("ERROR - No data was passed in")
		else:
			results = self.collection.find_one(data)
			if results is None:
				self.collection.insert_one(data)
				print("SUCCESS - " + s + " was successfully added.")
			else:
				print("ERROR - Data " + results["name"] + " already in database.")

	#READ
	def read(self, data):
		s = json.dumps(data)
		x = []
		if data is None or data == {}:
			print("ERROR - No data was passed in")
		else:
			results = self.collection.find(data)
			if results is None:
				print("ERROR - " + s + " was not found")
			else:
				results = self.collection.find(data)
				count = 0
				for item in results:
					print("SUCCESS - " + s + " was found")
					x.append(item)
					count+=1
				print("*** " + str(count) + " total document(s) containing " + s + " were found")
				return results


	#READ ALL
	def readAll(self, data):
		results = self.collection.find(data)
        
		return results


	#UPDATE
	def update(self, data, replace):
		d = json.dumps(data)
		r = json.dumps(replace)
		if data is None or data == {}:
			print("ERROR - No data was passed in")
		else:
			results = self.collection.find_one(data)
			if results is None:
				print("ERROR - " + s + " was not found")
			else:
				results = self.collection.find(data)
				for item in results:
					self.collection.update_one(data, {"$set": replace})
					print("SUCCESS - updated " + d + " to " + r)

	
	#DELETE
	def delete(self, data):
		d = json.dumps(data)
		if data is None or data == {}:
			print("ERROR - No data was passed in")
		else:
			results = self.collection.find_one(data)
			if results is None:
				print("ERROR - " + d + " was not found")
			else:
				self.collection.delete_one(data)
				s = json.dumps(data)
				print("SUCCESS - " + s + " deleted")
                
	#REFRESH DB
	def refresh(self, data):
		self.collection.delete_many({})
		self.collection.insert_many(data)
	