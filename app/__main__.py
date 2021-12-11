from src.data.make_dataset import generate_raw
from src.features.build_features import preprocess_data
from src.models.train_model import evaluate_models
from src.models.predict_model import predict

if __name__ == "__main__":
    #generate_raw()
    preprocess_data()
    evaluate_models()
    predict("Tbh this movie was horrible, I was very disappointed. Just trash","linearsvc")