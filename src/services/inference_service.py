from src.models.predict import predict_match

def run_inference(match_features_df):
    return predict_match(match_features_df)