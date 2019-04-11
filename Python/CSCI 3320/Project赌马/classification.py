import pandas as pd
import numpy as np
import time
import naive_bayes
from sklearn import linear_model
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn import svm

def main():
    #All features:
    # Char: horse_index (horse_id, horse_name), jockey_index (jockey), trainer_index(trainer)
    # Behaviour: recent_ave_rank(recent_6_runs), jockey_ave_rank, trainer_ave_rank
    # Race: actual_weight, declared_horse_weight, draw, win_odds, race_distance, (race_id, horse_number)
    # Result: finishing_position, length_behind_winner, finish_time
    #         running_position_1, running_position_2, running_position_3, running_position_4, running_position_5, running_position_6,
    training_df = pd.read_csv("training.csv")
    training_df['length_behind_winner'] = training_df['length_behind_winner'].apply(
        lambda frac: convert_to_float_length_behind(frac))
    training_df['finish_time'] = training_df['finish_time'].apply(lambda frac: convert_to_float_time(frac))
    training_df = training_df.fillna(0)

    testing_df = pd.read_csv("testing.csv")
    temp_df_jockey_index = training_df[['jockey_index','jockey_ave_rank']].drop_duplicates(subset = 'jockey_index', keep='last')
    temp_df_trainer_index = training_df[['trainer_index', 'trainer_ave_rank']].drop_duplicates(subset='trainer_index', keep='last')
    testing_df = testing_df.merge(temp_df_jockey_index, left_on = 'jockey_index', right_on = 'jockey_index',how = 'left')
    testing_df = testing_df.merge(temp_df_trainer_index, left_on='trainer_index', right_on='trainer_index', how='left')
    testing_df['jockey_ave_rank'].fillna(7,inplace = True)
    testing_df['trainer_ave_rank'].fillna(7, inplace=True)

    lr_model(training_df, testing_df)
    nb_model(training_df, testing_df)
    svm_model(training_df, testing_df)
    rf_model(training_df, testing_df)

def lr_model(training_df, testing_df):
    print('lr_model:')
    X_train = training_df[['horse_index','jockey_index','trainer_index','draw','actual_weight','race_distance','win_odds','declared_horse_weight']].values
    y_train = training_df[['finishing_position']].values
    X_test = testing_df[['horse_index','jockey_index','trainer_index','draw','actual_weight','race_distance','win_odds','declared_horse_weight']].values

    start_time = time.time()
    lr_model = linear_model.LogisticRegression()
    lr_model.fit(X_train, y_train[:,0])
    y_pred = lr_model.predict(X_test)
    print("Running time: ", (time.time() - start_time))
    result = testing_df[['race_id', 'horse_index']].values
    result = np.append(result, y_pred[:,None], axis=1)
    result_df = pd.DataFrame(data=result,columns=['race_id','horse_index','finishing_position'])
    result_df['recent_ave_rank'] = testing_df['recent_ave_rank']
    result_df = finishPositionTranslate(result_df)
    outputCSV(result_df,None,'model_result/lr_model_result.csv')
    result_df = label_All(result_df,mode='finishing_position')
    result_df['horse_id'] = testing_df['horse_id']
    outputCSV(result_df, None, 'predictions/lr_predictions.csv', mode=2)
    true_df = label_All(testing_df,mode='finishing_position')
    #print(result_df,'\n\n',true_df)
    evaluation(true_df, result_df)

def nb_model(training_df, testing_df):
    print('nb_model:')
    X_train = training_df[['horse_index','jockey_index','trainer_index']].values
    y_train = training_df[['finishing_position']].values
    X_test = testing_df[['horse_index','jockey_index','trainer_index']].values

    #modelSelection(X_train, y_train)
    start_time = time.time()
    nb_model = naive_bayes.NaiveBayes()
    nb_model.fit(X_train, y_train[:,0])
    y_pred = nb_model.predict(X_test)
    print("Running time: ", (time.time() - start_time))
    result = testing_df[['race_id', 'horse_index']].values
    result = np.append(result, y_pred[:,None], axis=1)
    result_df = pd.DataFrame(data=result,columns=['race_id','horse_index','finishing_position'])
    result_df['recent_ave_rank'] = testing_df['recent_ave_rank']
    result_df = finishPositionTranslate(result_df)
    outputCSV(result_df, None, 'model_result/nb_model_result.csv')
    result_df = label_All(result_df,mode='finishing_position')
    result_df['horse_id'] = testing_df['horse_id']
    outputCSV(result_df, None, 'predictions/nb_predictions.csv', mode=2)
    true_df = label_All(testing_df,mode='finishing_position')
    #print(result_df,'\n\n',true_df)
    evaluation(true_df, result_df)

def svm_model(training_df, testing_df):
    print('svm_model:')
    X_train = training_df[['recent_ave_rank','jockey_ave_rank','trainer_ave_rank']].values
    y_train = training_df[['finishing_position']].values
    X_test = testing_df[['recent_ave_rank','jockey_ave_rank','trainer_ave_rank']].values

    start_time = time.time()
    svm_model = svm.SVC(kernel='rbf', max_iter=1000)
    svm_model.fit(X_train, y_train[:,0])
    y_pred = svm_model.predict(X_test)
    print("Running time: ", (time.time() - start_time))
    result = testing_df[['race_id', 'horse_index']].values
    result = np.append(result, y_pred[:,None], axis=1)
    result_df = pd.DataFrame(data=result,columns=['race_id','horse_index','finishing_position'])
    result_df['recent_ave_rank'] = testing_df['recent_ave_rank']
    result_df = finishPositionTranslate(result_df)
    outputCSV(result_df, None, 'model_result/svm_model_result.csv')
    result_df = label_All(result_df,mode='finishing_position')
    result_df['horse_id'] = testing_df['horse_id']
    outputCSV(result_df, None, 'predictions/svm_predictions.csv',mode=2)
    true_df = label_All(testing_df,mode='finishing_position')
    # print(result_df,'\n\n',true_df)
    evaluation(true_df, result_df)

def rf_model(training_df, testing_df):
    print('rf_model:')
    X_train = training_df[['horse_index','jockey_index','trainer_index','draw','actual_weight','win_odds','declared_horse_weight']].values
    y_train = training_df[['finishing_position']].values
    X_test = testing_df[['horse_index','jockey_index','trainer_index','draw','actual_weight','win_odds','declared_horse_weight']].values

    start_time = time.time()
    rf_model = RandomForestClassifier(max_depth=10, random_state=0)
    rf_model.fit(X_train, y_train[:,0])
    y_pred = rf_model.predict(X_test)
    print("Running time: ", (time.time() - start_time))
    result = testing_df[['race_id', 'horse_index']].values
    result = np.append(result, y_pred[:,None], axis=1)
    result_df = pd.DataFrame(data=result,columns=['race_id','horse_index','finishing_position'])
    result_df['recent_ave_rank'] = testing_df['recent_ave_rank']
    result_df = finishPositionTranslate(result_df)
    outputCSV(result_df, None, 'model_result/rf_model_result.csv')
    result_df = label_All(result_df,mode='finishing_position')
    result_df['horse_id'] = testing_df['horse_id']
    outputCSV(result_df, None, 'predictions/rf_predictions.csv', mode=2)
    true_df = label_All(testing_df,mode='finishing_position')
    # print(result_df,'\n\n',true_df)
    evaluation(true_df, result_df)

def outputCSV(result_df, true_df, filename, mode=1):
    if mode == 1:
        result_df = result_df[['race_id','horse_index','finishing_position']]
    if mode == 2:
        result_df = result_df[['race_id', 'horse_id', 'HorseWin','HorseRankTop3', 'HorseRankTop50Percent']]
    result_df.to_csv(filename)

def evaluation(true_df,result_df):
    p_score = precision_score(np.asfarray(true_df[['HorseWin']].values,float), np.asfarray(result_df[['HorseWin']].values,float))
    r_score = recall_score(np.asfarray(true_df[['HorseWin']].values,float), np.asfarray(result_df[['HorseWin']].values,float))
    print("Winner: p_score:", p_score, 'r_score:', r_score)
    p_score = precision_score(np.asfarray(true_df[['HorseRankTop3']].values, float), np.asfarray(result_df[['HorseRankTop3']].values, float))
    r_score = recall_score(np.asfarray(true_df[['HorseRankTop3']].values, float), np.asfarray(result_df[['HorseRankTop3']].values, float))
    print("Top3: p_score:", p_score, 'r_score:', r_score)
    p_score = precision_score(np.asfarray(true_df[['HorseRankTop50Percent']].values, float), np.asfarray(result_df[['HorseRankTop50Percent']].values, float))
    r_score = recall_score(np.asfarray(true_df[['HorseRankTop50Percent']].values, float),np.asfarray(result_df[['HorseRankTop50Percent']].values, float))
    print("Top50P: p_score:", p_score, 'r_score:', r_score,"\n")

def modelSelection(X_train, y_train):
    nb_model_Ber = BernoulliNB()
    nb_model_Mut = MultinomialNB()
    nb_model_Gau = GaussianNB()
    lr_model = linear_model.LogisticRegression()
    svm_model = svm.SVC(kernel='linear', max_iter=10)
    kfold = KFold(n_splits=10)
    results = cross_val_score(nb_model_Ber, X_train, y_train.ravel(), cv=kfold, scoring='accuracy')
    print('BernoulliNB:', np.mean(results))
    results = cross_val_score(nb_model_Mut,X_train, y_train.ravel(), cv=kfold,scoring='accuracy')
    print('MultinomialNB:',np.mean(results))
    results = cross_val_score(nb_model_Gau, X_train, y_train.ravel(), cv=kfold, scoring='accuracy')
    print('GaussianNB:', np.mean(results))
    results = cross_val_score(lr_model, X_train, y_train.ravel(), cv=kfold, scoring='accuracy')
    print('LogisticRegression:', np.mean(results))
    results = cross_val_score(svm_model, X_train, y_train.ravel(), cv=kfold, scoring='accuracy')
    print('SVC:', np.mean(results))

def finishPositionTranslate(result_df): #Function: reorder finish position to be a sequence
    result_df_new = pd.DataFrame()
    result_df['index'] = [x for x in range(0, result_df.values.shape[0])]
    raceID = result_df[['race_id']].drop_duplicates(subset='race_id',keep='last')
    for i in range(0, raceID.values.shape[0]):
        result_df_sub = result_df[result_df['race_id'].isin(raceID.values[i])]
        result_df_sub = result_df_sub.sort_values(['finishing_position','recent_ave_rank'], ascending=[True,True])
        #print(result_df_sub)
        result_df_sub['finishing_position'] = [x for x in range(1, result_df_sub.values.shape[0] + 1)]
        frames = [result_df_new, result_df_sub]
        result_df_new = pd.concat(frames)
    result_df_new = result_df_new.sort_values(['index'], ascending=[True])
    return result_df_new[['race_id','horse_index','finishing_position']]

def label_All(result_df, mode, casual='True'): #Function: add Winner, Top3, Top50 to a dataFrame with (race_id, finishing_position)
    if mode == 'finishing_position':
        if casual == 'True':
            result_df['HorseWin'] = result_df.apply(lambda row: label_Winner(row,mode='Winner'), axis=1)
            result_df['HorseRankTop3'] = result_df.apply(lambda row: label_Winner(row,mode='Top3'), axis=1)
            result_df['HorseRankTop50Percent'] = result_df.apply(lambda row: label_Winner(row,mode='Top50',casual='True'), axis=1)
            return result_df[['race_id','horse_index','HorseWin','HorseRankTop3','HorseRankTop50Percent']]
        else:
            result_df_new = pd.DataFrame()
            raceID = result_df[['race_id']].drop_duplicates(subset='race_id',keep='last')
            for i in range(0, raceID.values.shape[0]):
                result_df_sub = result_df[result_df['race_id'].isin(raceID.values[i])]
                result_df_sub['race_capacity'] = result_df_sub.values.shape[0]
                frames = [result_df_new, result_df_sub]
                result_df_new = pd.concat(frames)
            result_df_new['HorseWin'] = result_df_new.apply(lambda row: label_Winner(row,mode='Winner'), axis=1)
            result_df_new['HorseRankTop3'] = result_df_new.apply(lambda row: label_Winner(row,mode='Top3'), axis=1)
            result_df_new['HorseRankTop50Percent'] = result_df_new.apply(lambda row: label_Winner(row,mode='Top50',casual='False'), axis=1)
            return result_df_new[['race_id','horse_index','HorseWin','HorseRankTop3','HorseRankTop50Percent']]
    return result_df

def label_Winner (row,mode,casual='True'):
    if mode == 'Winner':
       if row['finishing_position'] == 1 :
          return '1'
       return '0'
    if mode == 'Top3':
        if row['finishing_position'] <= 3:
            return '1'
        return '0'
    if mode == 'Top50':
        if casual == 'True':
            if row['finishing_position'] <= 6:
                return '1'
            return '0'
        else:
            if row['finishing_position'] <= row['race_capacity'] / 2:
                return '1'
            return '0'
    return -1;

def convert_to_float_time(frac_str):
    if frac_str.isdigit():
        return float(frac_str)
    else:
        min, sec, subsec = frac_str.split('.')
        whole = float(min) * 60 + float(sec) + float(subsec) / 100
        return whole

def convert_to_float_length_behind(frac_str):
    if frac_str.isdigit():
        return float(frac_str)
    else:
        if not frac_str.replace('-', '').replace('/', '').isdigit():
            return 0;
        else:
            if frac_str.find('-') == -1:
                num, denom = frac_str.split('/')
                whole = (float(num) / float(denom))
                return whole
            else:
                int, frac = frac_str.split('-')
                num, denom = frac.split('/')
                whole = float(int) + (float(num) / float(denom))
                return whole

if __name__ == '__main__':
    main()