import pandas as pd
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

def running_logr_model(training_file_name: str, testing_file_name: str, output_file_name: str, coefficients_file_name: str):
    # reading the training and testing files
    train_df = pd.read_csv(training_file_name)
    test_df = pd.read_csv(testing_file_name)
    # put into DataFrames
    train_df.columns = train_df.columns.str.strip()
    test_df.columns = test_df.columns.str.strip()
    
    # Defining the Features, numeric and categorical
    features = ['Nation', 'Age', 'Gender', 'Avg Final Score', 'Avg Turn Points', 'Avg Time Points', 'Avg Air Points', 'Avg Rank', 'Standard Deviation FS', 'Olympic Year']

    # List of features to be used -> X
    X_train = train_df[features]
    X_test = test_df[features]
    y_train = train_df['Made Top 5'] # -> target variable

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
    model.fit(X_train, y_train)

    # saving weights / coefficients for each variable
    feature_names = model.named_steps['preprocessor'].get_feature_names_out()
        # reverts from the binary encoding back to categorical feature name
    logreg = model.named_steps['classifier']
    coefs_df = pd.DataFrame({'feature': feature_names, 'coefficient': logreg.coef_[0]})
        # makes DataFrame of coefficients
    coefs_df['abs_coef'] = coefs_df['coefficient'].abs()
    coefs_df = coefs_df.sort_values('abs_coef', ascending=False) 
        # ^ sort by absolute value of the variable, ascending
    coefs_df[['feature', 'coefficient']].to_csv(coefficients_file_name, index=False)

    # predict probabilities of making top 5
    test_df['predicted_prob_top5'] = model.predict_proba(X_test)[:, 1]
    # uses common threshold of 0.5 to show: made top 5, did not make top 5 (0, 1)
    test_df['predicted_top5'] = (test_df['predicted_prob_top5'] >= 0.5).astype(int)

    # rank athletes by probability
    ranked_df = test_df.sort_values(by='predicted_prob_top5', ascending=False)
    ranked_df['rank'] = range(1, len(ranked_df) + 1)
    ranked_df.to_csv(output_file_name, index=False)