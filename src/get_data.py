import os
import yaml
import pandas as pd
import argparse

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def get_data_value(config_path):
    config = read_params(config_path)
    data_path = config["data_source"]["s3_source"]
    df = pd.read_csv(data_path, sep=",", encoding='utf-8')
 #   print(df.head(10))
    return df


if __name__=="__main__":
    args = argparse.ArgumentParser()
    config_path = os.path.join("config","params.yml")
    args.add_argument("--config", default=config_path)
    parsed_args = args.parse_args()
    data = get_data_value(config_path=parsed_args.config)