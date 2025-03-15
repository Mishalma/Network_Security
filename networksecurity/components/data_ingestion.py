from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import numpy as np
import pymongo
import pandas as pd
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            logging.info("Data Ingestion Initialized.")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self):
        """Read data from MongoDB Atlas and convert it into a Pandas DataFrame."""
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            logging.info(
                f"Connecting to MongoDB at {MONGO_DB_URL} | DB: {database_name} | Collection: {collection_name}")
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            logging.info(f"Fetched {len(df)} records from MongoDB.")

            if df.empty:
                raise ValueError("No data found in the MongoDB collection!")

            if "_id" in df.columns:
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"na": np.nan}, inplace=True)

            logging.info(f"DataFrame Shape after cleaning: {df.shape}")
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        """Save the DataFrame to a CSV file (feature store)."""
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            # Create directory if it doesn't exist
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            logging.info(f"Feature store saved at {feature_store_file_path} with {dataframe.shape[0]} rows.")

            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        """Split the data into train and test sets and save them as CSV files."""
        try:
            train_size = 1 - self.data_ingestion_config.train_test_split_ratio
            logging.info(
                f"Splitting data with train size: {train_size}, test size: {self.data_ingestion_config.train_test_split_ratio}")

            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42
            )

            logging.info(f"Train Set Shape: {train_set.shape}, Test Set Shape: {test_set.shape}")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)

            logging.info(f"Train data saved at: {self.data_ingestion_config.training_file_path}")
            logging.info(f"Test data saved at: {self.data_ingestion_config.testing_file_path}")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self):
        """Execute the data ingestion pipeline: fetch, store, split, and return artifact."""
        try:
            logging.info("Starting data ingestion process...")
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)

            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

            logging.info("Data ingestion completed successfully.")
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
