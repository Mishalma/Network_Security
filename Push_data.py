import sys
import os
import json
from dotenv import load_dotenv
import certifi
import pandas as pd
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# Load environment variables
load_dotenv()
MANGO_DB_URL = os.getenv("MANGO_DB_URL")
print(f"MongoDB URL: {MANGO_DB_URL}")

# Certificate for MongoDB connection
ca = certifi.where()


class NetworkDataExtract:
    def __init__(self):
        try:
            self.mongo_client = None  # Initialize mongo_client as None
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_converter(self, file_path):
        """Convert CSV file to JSON records."""
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            logging.info(f"Converted {len(records)} records from CSV to JSON")
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongo(self, records, database, collection):
        """Insert records into MongoDB collection."""
        try:
            self.database = database
            self.collection = collection
            self.records = records

            # Connect to MongoDB
            self.mongo_client = pymongo.MongoClient(MANGO_DB_URL, tlsCAFile=ca)
            db = self.mongo_client[self.database]
            coll = db[self.collection]

            # Insert records
            result = coll.insert_many(self.records)
            logging.info(f"Inserted {len(result.inserted_ids)} records into {database}.{collection}")
            return len(result.inserted_ids)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        finally:
            if self.mongo_client:
                self.mongo_client.close()
                logging.info("MongoDB connection closed")


if __name__ == "__main__":
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "MISHALAI"
    COLLECTION = "Network_Data"  # Fixed variable name to match convention

    try:
        # Instantiate the class
        network_obj = NetworkDataExtract()

        # Convert CSV to JSON records
        records = network_obj.csv_to_json_converter(file_path=FILE_PATH)

        # Insert records into MongoDB
        no_of_records = network_obj.insert_data_mongo(records, DATABASE, COLLECTION)
        print(f"Number of records inserted: {no_of_records}")
    except NetworkSecurityException as e:
        print(f"Error occurred: {e}")