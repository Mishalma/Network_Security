from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig

import sys

if __name__ == "__main__":
    try:
        # Setup logging (if not already done in logger.py)
        logging.info("Initializing Training Pipeline Configuration...")

        trainingpipelineconfig = TrainingPipelineConfig()  # Check if arguments are needed
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)  # Ensure this is correct

        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("Starting Data Ingestion Process...")

        dataingestionartifact = data_ingestion.initiate_data_ingestion()

        logging.info("Data Ingestion Completed Successfully.")
        print(f"Data Ingestion Artifact: {dataingestionartifact}")

    except Exception as e:
        logging.error(f"Data Ingestion Failed: {str(e)}")
        raise NetworkSecurityException(e, sys)
