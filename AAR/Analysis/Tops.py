import pandas as pd
import os
import sys


def get_data_dir():
    if 'Data' in os.listdir('.'):
        return './Data'
    return '../Data'


def format_data(data):
    if data['replies'].dtype == 'O':
        data['replies'] = pd.to_numeric(data['replies'].apply(lambda s: s.replace(',', '').replace('.', '')))
    if data['views'].dtype == 'O':
        data['views'] = pd.to_numeric(data['views'].apply(lambda s: s.replace(',', '').replace('.', '')))


def compute_diff_on_2_latest_dates(data):
    latest_date = data['date'].unique()[-1]
    previous_latest_date = data['date'].unique()[-2]
    latest_date_df = data[data['date'] == latest_date]
    previous_latest_date_df = data[data['date'] == previous_latest_date][['replies', 'title', 'views', 'url']]
    merged_data = pd.merge(latest_date_df, previous_latest_date_df, on=['title', 'url'], how='left')
    merged_data.fillna(0, inplace=True)
    merged_data['diff_replies'] = merged_data['replies_x'] - merged_data['replies_y']
    merged_data['diff_views'] = merged_data['views_x'] - merged_data['views_y']
    return latest_date, previous_latest_date, merged_data[['title', 'url', 'diff_replies', 'diff_views']]


def print_top_diff(diff_2_latest_dates, n, type):
    for index, row in diff_2_latest_dates.nlargest(n, 'diff_' + type).iterrows():
        if row['diff_' + type] == 0:
            print('NO MORE THREAD WITH {0} !'.format(type.upper()))
            return
        print(u'{0} {1} {2}'.format(row['url'], row['title'], int(row['diff_' + type])))


def format_pretty_date(date):
    return pd.to_datetime(str(date)).strftime('%d/%m/%Y')


def main(args):
    json_path = os.path.join(get_data_dir(), args[1])
    print('Read the file {0}'.format(json_path))
    data = pd.read_json(json_path)
    format_data(data)
    latest_date, previous_latest_date, diff_2_latest_dates = compute_diff_on_2_latest_dates(data)
    print('TOP VIEWS between {0} and {1}:'.format(format_pretty_date(previous_latest_date),
                                                    format_pretty_date(latest_date)))
    print_top_diff(diff_2_latest_dates, int(args[2]), 'views')
    print('\n\nTOP REPLIES between {0} and {1}:'.format(format_pretty_date(previous_latest_date),
                                                    format_pretty_date(latest_date)))
    print_top_diff(diff_2_latest_dates, int(args[2]), 'replies')


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv)
