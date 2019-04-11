import pandas as pd
import classification
import numpy as np
import math
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import gradient_boosting
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
        lambda frac: classification.convert_to_float_length_behind(frac))
    training_df['finish_time'] = training_df['finish_time'].apply(lambda frac: classification.convert_to_float_time(frac))
    training_df = training_df.fillna(0)

    testing_df = pd.read_csv("testing.csv")
    testing_df['finish_time'] = testing_df['finish_time'].apply(
        lambda frac: classification.convert_to_float_time(frac))
    testing_df = testing_df.fillna(0)
    temp_df_jockey_index = training_df[['jockey_index','jockey_ave_rank']].drop_duplicates(subset = 'jockey_index', keep='last')
    temp_df_trainer_index = training_df[['trainer_index', 'trainer_ave_rank']].drop_duplicates(subset='trainer_index', keep='last')
    testing_df = testing_df.merge(temp_df_jockey_index, left_on = 'jockey_index', right_on = 'jockey_index',how = 'left')
    testing_df = testing_df.merge(temp_df_trainer_index, left_on='trainer_index', right_on='trainer_index', how='left')
    testing_df['jockey_ave_rank'].fillna(7,inplace = True)
    testing_df['trainer_ave_rank'].fillna(7, inplace=True)

    svr_model(training_df, testing_df,normalized='False')
    svr_model(training_df, testing_df, normalized='True')
    gbrt_model(training_df, testing_df,normalized='False')
    gbrt_model(training_df, testing_df, normalized='True')

def svr_model(training_df, testing_df, normalized='False'):
    X_train = training_df[['recent_ave_rank','jockey_ave_rank','trainer_ave_rank','race_distance',
                           'actual_weight','declared_horse_weight','draw','win_odds']]
    y_train = training_df[['finish_time']]
    X_test = testing_df[['recent_ave_rank','jockey_ave_rank','trainer_ave_rank','race_distance',
                           'actual_weight','declared_horse_weight','draw','win_odds']]
    scaler = StandardScaler()
    train_scalered = scaler.fit_transform(X_train.values)  # select 4 feature
    test_scalered = scaler.transform(X_test.values)

    svr_model = svm.SVR(kernel='rbf', max_iter=10000, C=1,epsilon=0.1)
    if normalized == 'True':
        print('svr_model(Normalized):')
        svr_model.fit(train_scalered, y_train.values[:,0])
        y_pred = svr_model.predict(test_scalered)
    if normalized == 'False':
        print('svr_model:')
        svr_model.fit(X_train, y_train.values[:, 0])
        y_pred = svr_model.predict(X_test)
    result = testing_df[['race_id', 'horse_index']].values
    result = np.append(result, y_pred[:,None], axis=1)
    result_df = pd.DataFrame(data=result,columns=['race_id','horse_index','finish_time'])
    result_df['recent_ave_rank'] = testing_df['recent_ave_rank']
    result_df = finishTimeTranslate(result_df)
    if normalized == 'True':
        classification.outputCSV(result_df, None, 'model_result/svr_model_result_normalized.csv')
    if normalized == 'False':
        classification.outputCSV(result_df, None, 'model_result/svr_model_result.csv')
    result_df = result_df[['race_id', 'horse_index', 'finishing_position','finish_time']]
    true_df =  testing_df[['race_id', 'horse_index', 'finishing_position','finish_time']]
    evaluation(result_df, true_df)

def gbrt_model(training_df, testing_df, normalized='False'):
    X_train = training_df[['recent_ave_rank','jockey_ave_rank','trainer_ave_rank','race_distance',
                           'actual_weight','declared_horse_weight','draw','win_odds']]
    y_train = training_df[['finish_time']]
    X_test = testing_df[['recent_ave_rank','jockey_ave_rank','trainer_ave_rank','race_distance',
                           'actual_weight','declared_horse_weight','draw','win_odds']]
    scaler = StandardScaler()
    train_scalered = scaler.fit_transform(X_train.values)  # select 4 feature
    test_scalered = scaler.transform(X_test.values)

    gbrt_model = gradient_boosting.GradientBoostingRegressor(loss='quantile',learning_rate=0.1,n_estimators=200,max_depth=3)
    if normalized == 'True':
        print('gbrt_model(Normalized):')
        gbrt_model.fit(train_scalered, y_train.values[:,0])
        y_pred = gbrt_model.predict(test_scalered)
    if normalized == 'False':
        print('gbrt_model:')
        gbrt_model.fit(X_train, y_train.values[:, 0])
        y_pred = gbrt_model.predict(X_test)
    result = testing_df[['race_id', 'horse_index']].values
    result = np.append(result, y_pred[:,None], axis=1)
    result_df = pd.DataFrame(data=result,columns=['race_id','horse_index','finish_time'])
    result_df['recent_ave_rank'] = testing_df['recent_ave_rank']
    result_df = finishTimeTranslate(result_df)
    if normalized == 'True':
        classification.outputCSV(result_df, None, 'model_result/gbrt_model_result_normalized.csv')
    if normalized == 'False':
        classification.outputCSV(result_df, None, 'model_result/gbrt_model_result.csv')
    result_df = result_df[['race_id', 'horse_index', 'finishing_position','finish_time']]
    true_df =  testing_df[['race_id', 'horse_index', 'finishing_position','finish_time']]
    #print(result_df,'\n\n',true_df)
    evaluation(result_df, true_df)

def evaluation(result_df, true_df):
    temp_df = pd.DataFrame()
    temp_df[['finishing_position_result']] = result_df[['finishing_position']]
    temp_df[['finishing_position_true']] = true_df[['finishing_position']]
    temp_df['Top_1_Hit'] = temp_df.apply(lambda row: label_Predict(row, mode='Win'), axis=1)
    temp_df['Top_3_Hit'] = temp_df.apply(lambda row: label_Predict(row, mode='Top3'), axis=1)
    temp_df['Average_Rank'] = temp_df.apply(lambda row: label_Predict(row, mode='Average_Rank'), axis=1)
    temp_df = temp_df[temp_df["finishing_position_result"] == 1]
    print("Top1 hit: ", np.mean(temp_df['Top_1_Hit'].values), "Top3 hit: ", np.mean(temp_df['Top_3_Hit'].values))

    temp_df_time = pd.DataFrame()
    temp_df_time[['finishing_time_result']] = result_df[['finish_time']]
    temp_df_time[['finishing_time_true']] = true_df[['finish_time']]
    temp_df_time['MSE'] = temp_df_time.apply(lambda row: label_Predict(row, mode='MSE'), axis=1)
    print("Average_Rank: ", np.mean(temp_df['Average_Rank'].values), "MSE: ", math.sqrt(np.mean(temp_df_time['MSE'].values)))
    print("(", math.sqrt(np.mean(temp_df_time['MSE'].values)), ",", np.mean(temp_df['Top_1_Hit'].values), ",", np.mean(temp_df['Top_3_Hit'].values), ",",np.mean(temp_df['Average_Rank'].values),")\n")

def label_Predict(row, mode):
    if mode == 'Win':
        if row['finishing_position_result'] == 1 and row['finishing_position_true'] == 1:
            return 1
        else:
            return 0;
    if mode == 'Top3':
        if row['finishing_position_result'] == 1 and row['finishing_position_true'] >= 1 and row['finishing_position_true'] <= 3:
            return 1
        else:
            return 0;
    if mode == 'Average_Rank':
        if row['finishing_position_result'] == 1:
            return row['finishing_position_true'];
        else:
            return 0;
    if mode == 'MSE':
        return math.pow(row['finishing_time_result'] - row['finishing_time_true'], 2)

def finishTimeTranslate(result_df): #Function: reorder finish position to be a sequence
    result_df_new = pd.DataFrame()
    result_df['index'] = [x for x in range(0, result_df.values.shape[0])]
    raceID = result_df[['race_id']].drop_duplicates(subset='race_id',keep='last')
    for i in range(0, raceID.values.shape[0]):
        result_df_sub = result_df[result_df['race_id'].isin(raceID.values[i])]
        result_df_sub = result_df_sub.sort_values(['finish_time','recent_ave_rank'], ascending=[True,True])
        result_df_sub['finishing_position'] = [x for x in range(1, result_df_sub.values.shape[0] + 1)]
        frames = [result_df_new, result_df_sub]
        result_df_new = pd.concat(frames)
    result_df_new = result_df_new.sort_values(['index'], ascending=[True])
    return result_df_new[['race_id','horse_index','finishing_position','finish_time']]

if __name__ == '__main__':
    main()