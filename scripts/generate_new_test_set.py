import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

categories = pd.read_csv("../resources/angusSepsisCategorization.csv")
subjects = categories["subject_id"]

train, test = train_test_split(subjects, test_size=.1, random_state=1, stratify=categories["angus"])

trainDF = pd.DataFrame({"subject_id":train})
trainDF["test"] = pd.Series(0, index=trainDF.index)

testDF = pd.DataFrame({"subject_id":test})
testDF["test"] = pd.Series(1, index=testDF.index)

testSetDf = pd.concat([trainDF, testDF]);
testSetDf.set_index("subject_id").to_csv("../resources/testset2.csv")