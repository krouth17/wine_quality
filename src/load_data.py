## get the data from csv and save it in data/raw/
import os
import argparse
from get_data import read_params,get_data_value

def load_and_save(config_path):
    params = read_params(config_path)
    df = get_data_value(config_path)
    cols = [cols.replace(" ","_") for cols in df.columns]
    raw_data_path = params['raw_data']['raw_data_path']
    df.to_csv(raw_data_path,index=False,sep=",",header=raw_data_path)


if __name__=="__main__":
    args = argparse.ArgumentParser()
    config_path = os.path.join("config","params.yml")
    args.add_argument("--config", default=config_path)
    parsed_args = args.parse_args()
    load_and_save(config_path=parsed_args.config)