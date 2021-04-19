##Load the train and test data
##Train the model with the training data
##Save the parameters
import os
import json
import joblib
import argparse
import numpy as np 
import pandas as pd 
from get_data import read_params
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score


def train_evaluate(config_path):
    config = read_params(config_path)
    test_data_path = config['split_data']['test_data_path']
    train_data_path = config['split_data']['train_data_path']
    random_state = config['split_data']['random_state']
    model_store_dir = config['train_evaluate']['model_store_dir']
    alpha = config['train_evaluate']['alpha']
    l1_ratio = config['train_evaluate']['l1_ratio']
    target_col = [config['train_evaluate']['target_col']]
    scores_json = config['reports']['scores_json']
    params_file = config['reports']['params_json']

    train_data = pd.read_csv(train_data_path,sep=",")
    test_data = pd.read_csv(test_data_path,sep=",")

    train_x = train_data.drop(columns=target_col,axis=1)
    test_x = test_data.drop(columns=target_col,axis=1)

    train_y = train_data[target_col]
    test_y = test_data[target_col]

    lr = ElasticNet(alpha=alpha,l1_ratio=l1_ratio,random_state=random_state)
    lr.fit(train_x,train_y)

    predicted_qualities = lr.predict(test_x)
    rmse,mae,r2 = evaluate_metrics(test_y,predicted_qualities)
    print(rmse,mae,r2)

    with open(params_file,'w') as rb:
        params = {
            "alpha": alpha,
            "l1_ratio": l1_ratio,
        }
        json.dump(params,rb,indent=4)
    
    with open(scores_json,'w') as rb:
        scores = {
            "rmse": rmse,
            "mae": mae,
            "r2": r2
        }
        json.dump(scores,rb,indent=4)

    os.makedirs(model_store_dir,exist_ok=True)
    model_path = os.path.join(model_store_dir,"model.joblib")
    joblib.dump(lr,model_path)


def evaluate_metrics(actual,predicted):
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    mae = mean_absolute_error(actual, predicted)
    r2 = r2_score(actual, predicted)
    return rmse,mae,r2


if __name__=='__main__':
    args = argparse.ArgumentParser()
    config_path = os.path.join("config","params.yml")
    args.add_argument("--config", default=config_path)
    parsed_args = args.parse_args()
    train_evaluate(config_path=parsed_args.config)


