import pandas as pd
import classification

def main():
    pd.options.mode.chained_assignment = None
    for i in range(0, 8):
        model(i)

def model(num):
    result_file = ['lr_model_result','nb_model_result','svm_model_result','rf_model_result', 'svr_model_result', 'svr_model_result_normalized', 'gbrt_model_result', 'gbrt_model_result_normalized']
    l = []
    l.append('model_result/')
    l.append(result_file[num])
    l.append(".csv")
    result_df = pd.read_csv(''.join(l))

    testing_df = pd.read_csv("testing.csv")
    result_df = classification.label_All(result_df,mode='finishing_position')
    true_df = classification.label_All(testing_df,mode='finishing_position')

    bet_df = pd.DataFrame()
    bet_df[['race_id','horse_index','HorseWin']] = true_df[['race_id','horse_index','HorseWin']]
    bet_df[['choice']] = result_df[['HorseWin']]
    bet_df[['win_odds']] = testing_df[['win_odds']]
    bet_df = bet_df[bet_df.choice != '0']
    bet_df['gain'] = bet_df.apply(lambda row: label(row, mode='Bet'), axis=1)

    list = bet_df['gain'].values
    print(result_file[num], 'Final money we get for all race:', sum(list))
    return 0

def label (row,mode='None'):
    if mode == 'Bet':
       if row['HorseWin'] == '1' :
          return row['win_odds']
       return -1
    return -233

if __name__ == '__main__':
    main()