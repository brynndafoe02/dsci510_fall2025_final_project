import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def running_logistic_regression(training_file_name: str, testing_file_name: str, output_file_name: str, coefficients_file_name: str):
    # load data
    train_df = pd.read_csv(training_file_name)
    test_df = pd.read_csv(testing_file_name)

    train_df.columns = train_df.columns.str.strip()
    test_df.columns = test_df.columns.str.strip()

    # define features
    features = ['Nation', 'Age', 'Gender', 'Avg Final Score', 'Avg Turn Points', 'Avg Time Points', 'Avg Air Points', 'Avg Rank', 'Standard Deviation FS', 'Olympic Year']

    X_train = train_df[features]
    y_train = train_df['Made Top 5']
    X_test = test_df[features]

    # pre processing 
    numeric_features = ['Age', 'Avg Final Score', 'Avg Turn Points', 'Avg Time Points', 'Avg Air Points', 'Avg Rank', 'Standard Deviation FS', 'Olympic Year']
    categorical_features = ['Nation', 'Gender']

    preprocessor = ColumnTransformer(transformers=[
        ('num', SimpleImputer(strategy='mean'), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)])

    # logistic regression pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(max_iter=1000))])

    model.fit(X_train, y_train)

    # prints weights / coefficients for each variable
    feature_names = model.named_steps['preprocessor'].get_feature_names_out()
    logreg = model.named_steps['classifier']
    coefs_df = pd.DataFrame({'feature': feature_names, 'coefficient': logreg.coef_[0]})
    coefs_df['abs_coef'] = coefs_df['coefficient'].abs()
    coefs_df = coefs_df.sort_values('abs_coef', ascending=False)
    coefs_df[['feature', 'coefficient']].to_csv(coefficients_file_name, index=False)

    # predict probabilities 
    test_df['predicted_prob_top5'] = model.predict_proba(X_test)[:, 1]
        # optional below: predicted class using 0.5 threshold
    test_df['predicted_top5'] = (test_df['predicted_prob_top5'] >= 0.5).astype(int)

    # rank athletes by probability
    ranked_df = test_df.sort_values(by='predicted_prob_top5', ascending=False)
    ranked_df['rank'] = range(1, len(ranked_df) + 1)
    ranked_df.to_csv(output_file_name, index=False)