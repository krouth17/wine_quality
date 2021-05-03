## Split the data and put it in data/preprocessed folder
import os
import yaml
import argparse
import pandas as pd
from get_data import read_params,get_data_value
from sklearn.model_selection import train_test_split

def split_and_save_data(config_path):
    config = read_params(config_path)
    test_data_path = config['split_data']['test_data_path']
    train_data_path = config['split_data']['train_data_path']
    raw_data = config['raw_data']['raw_data_path']
    split_ratio = config['split_data']['split_ratio']
    random_state = config['split_data']['random_state']

    df = pd.read_csv(raw_data,sep=",", encoding='utf-8')

    train,test = train_test_split(df,test_size=split_ratio,random_state=random_state)

    train.to_csv(train_data_path,sep=",",index=False,encoding='utf-8')
    test.to_csv(test_data_path,sep=",",index=False,encoding='utf-8')


if __name__=="__main__":
    args = argparse.ArgumentParser()
    config_path = os.path.join("config","params.yml")
    args.add_argument("--config", default=config_path)
    parsed_args = args.parse_args()
    split_and_save_data(config_path=parsed_args.config)

    

