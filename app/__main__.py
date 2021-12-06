from src.data.make_dataset import generate_raw
from src.features.build_features import do_preprocessing
from src.models.train_model import evaluate_models

if __name__ == "__main__":
    #generate_raw()
    #do_preprocessing()
    evaluate_models()