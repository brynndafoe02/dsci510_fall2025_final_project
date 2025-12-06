import pandas as pd
import os
import csv
import sys
# !!! followed online documentation on how to use scikit's logistic regression 
from sklearn.linear_model import LogisticRegression
# ^ the actual model to be used
from sklearn.preprocessing import OneHotEncoder
# ^ will make categorial features into numeric 
from sklearn.impute import SimpleImputer
# ^ will be used to fill missing data
from sklearn.compose import ColumnTransformer
# ^ allows to use different applications (like OneHotEncoder and SimpleImputer) on different columns
from sklearn.pipeline import Pipeline
# ^ creates the flow in which the model can work 

# need to access config from root
root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root)

from config import DATA_FOLDER, FINAL_TRAINING_FILE_MEN, FINAL_TRAINING_FILE_WOMEN, FINAL_TESTING_FILE_MEN, FINAL_TESTING_FILE_WOMEN, TESTING_DATA_RANKED_MEN, TESTING_DATA_RANKED_WOMEN, COEFFICIENTS_MEN, COEFFICIENTS_WOMEN

sys.path.remove(root)
# return to running from src

def running_logr_model(gender: str):
    
    base_directory = os.path.dirname(os.path.dirname(__file__))
    data_directory = os.path.join(base_directory, DATA_FOLDER)

    if gender == "men":
        training_file = os.path.join(data_directory, FINAL_TRAINING_FILE_MEN)
        testing_file = os.path.join(data_directory, FINAL_TESTING_FILE_MEN)
        data_ranked_file = os.path.join(data_directory, TESTING_DATA_RANKED_MEN)
        coefficients_file = os.path.join(data_directory, COEFFICIENTS_MEN)
    elif gender == "women":
        training_file = os.path.join(data_directory, FINAL_TRAINING_FILE_WOMEN)
        testing_file = os.path.join(data_directory, FINAL_TESTING_FILE_WOMEN)
        data_ranked_file = os.path.join(data_directory, TESTING_DATA_RANKED_WOMEN)
        coefficients_file = os.path.join(data_directory, COEFFICIENTS_WOMEN)
   
    # reading the training and testing files
    training_df = pd.read_csv(training_file)
    testing_df = pd.read_csv(testing_file)
    # put into DataFrames
    training_df.columns = training_df.columns.str.strip()
    testing_df.columns = testing_df.columns.str.strip()
    
    # Defining the Features, numeric and categorical
    features = ['Nation', 'Age', 'Gender', 'Avg Final Score', 'Avg Turn Points', 'Avg Time Points', 'Avg Air Points', 'Avg Rank', 'Standard Deviation FS', 'Olympic Year']

    # List of features to be used -> X
    X_training = training_df[features]
    X_testing = testing_df[features]
    Y_training = training_df['Made Top 5'] # -> target variable

    # Pre processing -> defining which features are numeric and categorical 
    numeric_features = ['Age', 'Avg Final Score', 'Avg Turn Points', 'Avg Time Points', 'Avg Air Points', 'Avg Rank', 'Standard Deviation FS', 'Olympic Year']
    categorical_features = ['Nation', 'Gender']

        # for numeric columns: if missing data, fill in with mean (average of all athlete's data from the column in which the missing data comes from)
        # for categorical columns: convert to binary 
            # handle_unknown='ignore' -> will not making model break when seeing a new categorical feature 
    preprocessor = ColumnTransformer(transformers=[
        ('num', SimpleImputer(strategy='mean'), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)])

    # creating logistic regression pipeline
        # 1. pre process
        # 2. run model 
            # max_iter=1000 -> controls max iterations, will prevent model from running too long
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(max_iter=1000))])

    # fit model with the training data
    model.fit(X_training, Y_training)

    # saving weights / coefficients for each variable
    feature_names = model.named_steps['preprocessor'].get_feature_names_out()
        # reverts from the binary encoding back to categorical feature name
    log_reg = model.named_steps['classifier']
    coefficients_df = pd.DataFrame({'feature': feature_names, 'coefficient': log_reg.coef_[0]})
        # makes DataFrame of coefficients
    coefficients_df['abs_coef'] = coefficients_df['coefficient'].abs()
    coefficients_df = coefficients_df.sort_values('abs_coef', ascending=False) 
        # ^ sort by absolute value of the variable, ascending
    coefficients_df[['feature', 'coefficient']].to_csv(coefficients_file, index=False)

    # predict probabilities of making top 5
    testing_df['predicted_prob_top5'] = model.predict_proba(X_testing)[:, 1]
    # uses threshold of 0.5 to show: made top 5, did not make top 5 (0 or 1)
    testing_df['predicted_top5'] = (testing_df['predicted_prob_top5'] >= 0.5).astype(int)

    # rank athletes by probability
    ranked_df = testing_df.sort_values(by='predicted_prob_top5', ascending=False)
    ranked_df['rank'] = range(1, len(ranked_df) + 1)
    ranked_df.to_csv(data_ranked_file, index=False)