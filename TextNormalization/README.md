# Project Details
    Team ID: 34
    Teams Members:
        Nikhil Bandi - 170050099
        Chagam Dileep Kumar Reddy - 170050080
        Ramswaroop - 203050117

    Project Topic: Text Normalisation

    Project Description:
        Detection and Normalization of non-standard words such as abbreviations, numbers or currency expressions, measure phrases, addresses or dates.Require text to be converted from written expressions into appropriate "spoken" forms.

        Input : sequence of tokens
        Output : spoken form of the tokens

        Example:
            12:47 is converted to "twelve forty-seven"
            “6 ft” is converted to "six feet"
            10 Nov 2008  is converted to “the tenth of november two thousand eight”

    



# Requirements
    python modules : sklearn , xgboost , pandas , numpy , singleton_decorator

    pip install xgboost
    pip install singleton_decorator

## submission
    xgb_model_320000 : XGBoost model trained on 1/3 rd dataset
    XGboost.py : Run to view a example of normalisation
    change sentences with proper '###' as delimiter (Task is to normalise sequence of tokens ,we chose "###" as delimiter for tokens)

## How to Run
    python XGboost.py
    (Loads model and prints out put of 3 sample token sequnces)
    if needed to train
    download dataset file en_train.csv from https://drive.google.com/file/d/1NraMFJHpAoF1wCm2v6fOjd1SvyKvWnH8/view?usp=sharing and put the csv file in code folder
    (uncomment train_model()  to train a new model)

