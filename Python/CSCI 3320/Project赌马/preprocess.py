import pandas as pd
import numpy as np
import os

def get_avg_recent_6_runs(id_rank, range, idx):
    if idx == 0:
        return 7
    elif idx < range:
        avg = sum(id_rank[0:idx])/idx
    else:
        avg = sum(id_rank[idx - range:idx])/range
    return avg

def get_recent_6_runs(id_rank, range, idx):
    if idx < range:
        string = '/'.join(str(x) for x in id_rank[0:idx])
    else:
        string = '/'.join(str(x) for x in id_rank[idx - range:idx])
    return string

def main():
    mypath = 'model_result'
    if not os.path.isdir(mypath):
        os.makedirs(mypath)
    mypath = 'predictions'
    if not os.path.isdir(mypath):
        os.makedirs(mypath)
    # 2.2.1
    # read csv into dataframe
    df = pd.read_csv("data/race-result-horse.csv")
    # drop the rows where the “finishing_position” is not a number
    df = df[pd.to_numeric(df['finishing_position'], errors='coerce').notnull()]
    # 2.2.2
    # Add a column named race_index
    # df['race_index'] = df['race_id'].str.replace('-', '').astype(int)
    # Add a column named recent_6_runs
    # Add a column named recent_ave_rank
    df['finishing_position'] = df['finishing_position'].astype(int)
    df['recent_6_runs'] = ''
    df['recent_ave_rank'] = 7
    for _id in df.horse_id.unique():
        id_df = df.loc[df['horse_id'] == _id]
        row_index = id_df.index
        id_rank = list(id_df.finishing_position)
        for idx, _ in enumerate(id_rank):
            rank_string = get_recent_6_runs(id_rank, 6, idx)
            ave_rank = get_avg_recent_6_runs(id_rank, 6, idx)
            df.set_value(row_index[idx], 'recent_6_runs', rank_string)
            df.set_value(row_index[idx], 'recent_ave_rank', ave_rank)
    # 2.2.3
    # set rank to horse, jockeys, trainers
    horse_unique = np.array(df.horse_id.unique())

    def get_horse_rank(horse):
        return np.where(horse_unique == horse)[0][0]
    df['horse_index'] = df['horse_id'].apply(lambda x: get_horse_rank(x))

    jockey_unique = np.array(df.jockey.unique())

    def get_jockey_rank(jockey):
        return np.where(jockey_unique == jockey)[0][0]
    df['jockey_index'] = df['jockey'].apply(lambda x: get_jockey_rank(x))

    trainer_unique = np.array(df.trainer.unique())

    def get_trainer_rank(trainer):
        return np.where(trainer_unique == trainer)[0][0]
    df['trainer_index'] = df['trainer'].apply(lambda x: get_trainer_rank(x))
    # the number of horses, the number of jockeys, and the number of trainers
    print('horses:', horse_unique.shape[0])
    print('jockeys:', jockey_unique.shape[0])
    print('trainers:', trainer_unique.shape[0])

    # 2.2.4
    # Read the distance information in race-result-race.csv and add a column to the dataframe
    # race_distance for each entry in race-result-horse.csv
    race_df = pd.read_csv("data/race-result-race.csv")
    temp_df = pd.DataFrame()
    temp_df = race_df[['race_id', 'race_distance']]
    temp_df = temp_df.drop_duplicates(subset='race_id', keep='last')
    df = df.merge(temp_df, left_on='race_id', right_on='race_id', how='left')


    # Add columns named jockey_ave_rank
    # split to test data and train data
    test_data = df.loc[df['race_id'] > '2016-327']
    train_data = df.loc[df['race_id'] <= '2016-327']
    # test_data = test_data.drop(['race_date'], axis=1)
    # train_data = train_data.drop(['race_date'], axis=1)
    temp_df = pd.DataFrame()
    temp_df = train_data[['jockey_index', 'finishing_position']]
    temp_df['jockey_ave_rank'] = temp_df.jockey_index.map(temp_df.groupby(['jockey_index']).finishing_position.mean())
    temp_df = temp_df.drop_duplicates(subset='jockey_index', keep='last')
    temp_df = temp_df.drop(['finishing_position'], axis=1)
    train_data = train_data.merge(temp_df, left_on='jockey_index', right_on='jockey_index', how='left')
    train_data['jockey_ave_rank'].fillna(7, inplace=True)
    # Add trainer_ave_rank
    temp_df = pd.DataFrame()
    temp_df = train_data[['trainer_index', 'finishing_position']]
    temp_df['trainer_ave_rank'] = temp_df.trainer_index.map(temp_df.groupby(['trainer_index']).finishing_position.mean())
    temp_df = temp_df.drop_duplicates(subset='trainer_index', keep='last')
    temp_df = temp_df.drop(['finishing_position'], axis=1)
    train_data = train_data.merge(temp_df, left_on='trainer_index', right_on='trainer_index', how='left')
    train_data['trainer_ave_rank'].fillna(7, inplace=True)
    # 2.2.5 save to csv
    train_data.to_csv(path_or_buf='training.csv', index=False)
    test_data.to_csv(path_or_buf='testing.csv', index=False)


if __name__ == '__main__':
    main()