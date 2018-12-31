import pandas as pd
import os
import argparse


def get_args():
    parser = argparse.ArgumentParser(description='Write tops in markdown file')
    parser.add_argument('json', type=str, help='Relative data path (.json)')
    parser.add_argument('nb', type=str, help='Size of the top')
    parser.add_argument('--year', action='store_true', help='Comparison on the latest year instead of month')
    return parser.parse_args()


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
    return latest_date, previous_latest_date, compute_diff_on_2_dates(data, previous_latest_date, latest_date)


def compute_diff_on_the_year(data):
    latest_date = data['date'].unique()[-1]
    previous_latest_date = data['date'].unique()[-13]
    return latest_date, previous_latest_date, compute_diff_on_2_dates(data, previous_latest_date, latest_date)


def compute_diff_on_2_dates(data, date1, date2):
    if 'game' in data:
        game_key_cols = ['title', 'url', 'game']
    else:
        game_key_cols = ['title', 'url']
    latest_date_df = data[data['date'] == date2]
    previous_latest_date_df = data[data['date'] == date1][game_key_cols + ['replies', 'views']]
    merged_data = pd.merge(latest_date_df, previous_latest_date_df, on=game_key_cols, how='left')
    merged_data.fillna(0, inplace=True)
    merged_data['diff_replies'] = merged_data['replies_x'] - merged_data['replies_y']
    merged_data['diff_views'] = merged_data['views_x'] - merged_data['views_y']
    return merged_data[game_key_cols + ['diff_replies', 'diff_views']]


def write_top_diff(opened_file, diff_2_latest_dates, n, stat_type):
    has_game_col = 'game' in diff_2_latest_dates
    for index, row in diff_2_latest_dates.nlargest(n, 'diff_' + stat_type).iterrows():
        if row['diff_' + stat_type] == 0:
            print('NO MORE THREAD WITH {0} !'.format(stat_type.upper()))
            return
        if has_game_col:
            try:
                opened_file.write('\n|{3}|[{0}]({1})|{2}|'.format(row['title'], row['url'],
                                                                  int(row['diff_' + stat_type]), row['game']))
            except UnicodeEncodeError:
                print('UnicodeEncodeError when printing')
                print(row)
        else:
            try:
                opened_file.write('\n|[{0}]({1})|{2}|'.format(row['title'], row['url'], int(row['diff_' + stat_type])))
            except UnicodeEncodeError:
                print('UnicodeEncodeError when printing')
                print(row)


def format_pretty_date(date):
    return pd.to_datetime(str(date)).strftime('%d %b %Y')


def get_stats_year(latest_date):
    timestamp = pd.to_datetime(str(latest_date))
    if timestamp.month == 1:
        # Stats are for the previous year
        timestamp = timestamp - pd.DateOffset(years=1)
    return timestamp.strftime('%Y')


def get_stats_year_and_month(latest_date):
    timestamp = pd.to_datetime(str(latest_date))
    if timestamp.day < 15:
        # Stats are for the previous month
        timestamp = timestamp - pd.DateOffset(months=1)
    return timestamp.strftime('%Y_%m')


def main(args):
    relative_json_path = args.json
    top_number = int(args.nb)
    is_year = args.year
    json_path = os.path.join(get_data_dir(), relative_json_path)
    print(f'Read the file {json_path}')
    data = pd.read_json(json_path, encoding='utf-8')
    format_data(data)
    print('Compute the tops')
    if is_year:
        latest_date, previous_latest_date, diff_2_latest_dates = compute_diff_on_the_year(data)
    else:
        latest_date, previous_latest_date, diff_2_latest_dates = compute_diff_on_2_latest_dates(data)
    res_directory = os.path.join(get_data_dir(), '..', 'Results', relative_json_path.split('_')[0])
    if is_year:
        file_path = os.path.join(res_directory, get_stats_year(latest_date) + '_year.md')
    else:
        file_path = os.path.join(res_directory, get_stats_year_and_month(latest_date) + '.md')
    print(f'Write the file {file_path}')
    with open(file_path, 'w') as file:
        file.write('## TOP VIEWS*')
        if 'game' in data:
            file.write('\n\n|Game|AAR name and link|Nb|')
            file.write('\n| --- | --- | --- |')
        else:
            file.write('\n\n|AAR name and link|Nb|')
            file.write('\n| --- | --- |')
        write_top_diff(file, diff_2_latest_dates, top_number, 'views')
        file.write('\n\n## TOP REPLIES*')
        if 'game' in data:
            file.write('\n\n|Game|AAR name and link|Nb|')
            file.write('\n| --- | --- | --- |')
        else:
            file.write('\n\n|AAR name and link|Nb|')
            file.write('\n| --- | --- |')
        write_top_diff(file, diff_2_latest_dates, top_number, 'replies')
        file.write('\n\n**Statistics between {0} and {1}*'.format(format_pretty_date(previous_latest_date),
                                                                  format_pretty_date(latest_date)))
    print(f'{file_path} written')


if __name__ == "__main__":
    # execute only if run as a script
    args = get_args()
    main(args)
