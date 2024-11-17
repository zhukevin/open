# This is a sample Python script.
import csv
import os

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd


# def split_underlying_symbols(file_path, columns, nrows):
#     # Use a breakpoint in the code line below to debug your script.
#     cf = pd.read_csv(file_path, header=0, usecols=columns, chunksize=nrows)
#     for df in cf:
#         print(df.shape)
#         symbol_set = set(df['tic'])
#         print(symbol_set)
#         for symbol in symbol_set:
#             df_per_symbol = df[df['tic'] == symbol]
#             if os.path.isfile('/Volumes/data/underlying/{}.csv'.format(symbol)):
#                 df_per_symbol.to_csv('/Volumes/data/underlying/{}.csv'.format(symbol), index=False,
#                                      columns=df.columns, mode='a', header=False)
#             else:
#                 df_per_symbol.to_csv('/Volumes/data/underlying/{}.csv'.format(symbol), index=False,
#                                      columns=df.columns)


# Press ⌘F8 to toggle the breakpoint.

def statTrend(file_path, columns, threshold, i_time):
    df = pd.read_csv(file_path, header=None)
    print('threshold: ' + str(threshold * 100) + "%")
    # print('i_time: ' + i_time)
    df.columns = columns
    # print(df.shape)
    # print(df[0:3])
    # print(df['open'][1])
    n = len(df)
    over_threshold_amount, same_trend_amount, v_trend_amount = 0, 0, 0
    pre_date = df['date'][0]
    is_over_threshold = False
    # print(str(datetime(date_cur) - start_date))
    open_trend = 0
    same_trend_changes = 0
    v_trend_changes = 0
    over_threshold_changes = 0
    set_all = set()
    set_1 = set()
    set_2 = set()
    date_amount = 1
    for i in range(1, n - 1):
        date_cur = df['date'][i]
        if date_cur != pre_date:
            p0 = df['close'][i - 1]
            p1 = df['open'][i]
            if date_cur == '03/18/1999' or date_cur == '06/30/1999' or date_cur == '07/16/1999':
                continue
            if abs(p1 - p0) / p0 < 0.0025 and threshold == 0.0:
                    is_over_threshold = True
                    over_threshold_amount += 1
                    set_all.add(date_cur)
            if (p1 > p0 and threshold > 0) or (p1 < p0 and threshold < 0):
                if (abs(p1 - p0) / p0 >= abs(threshold) and (abs(p1 - p0) / p0 < abs(threshold) + 0.0025 or abs(threshold) >= 0.02)):
                    # print('reach threshold')
                    is_over_threshold = True
                    over_threshold_amount += 1
                    set_all.add(date_cur)
            pre_date = date_cur
        if is_over_threshold and df['time'][i] == i_time:
            # print(df['time'][i] )
            p2 = df['close'][i]
            over_threshold_changes += (p2 - p1) / p1
            if (p2 >= p1 and p1 >= p0) or (p2 <= p1 and p1 <= p0):
                same_trend_amount += 1
                same_trend_changes += (p2 - p1) / p1
                set_1.add(date_cur)
            if (p2 > p1 and p1 < p0) or (p2 < p1 and p1 > p0):
                v_trend_amount += 1
                v_trend_changes += (p2 - p1) / p1
                set_2.add(date_cur)
            is_over_threshold = False
    if same_trend_amount != 0:
        same_trend_changes_avg = round(same_trend_changes / same_trend_amount * 100, 3)
    else:
        same_trend_changes_avg = 0
    if v_trend_amount != 0:
        v_trend_changes_avg = round(v_trend_changes / v_trend_amount * 100, 3)
    else:
        v_trend_changes_avg = 0
    if over_threshold_amount != 0:
        changes_avg = round(over_threshold_changes / over_threshold_amount * 100, 3)
    else:
        changes_avg = 0
    # print('over_threshold_amount: ' + str(over_threshold_amount))
    # print('same_trend_amount_amount: ' + str(same_trend_amount))
    # print('same_trend_changes_avg: ' + str(same_trend_changes_avg))
    # print('v_trend_amount: ' + str(v_trend_amount))
    # print('v_trend_changes_avg: ' + str(v_trend_changes_avg))
    # print('over_threshold_changes_avg: ' + str(over_threshold_changes_avg))
    # print('len(set_all):' + str(len(set_all)))
    # print('len(set_1):' + str(len(set_1)))
    # print('len(set_2):' + str(len(set_2)))
    for date_all in set_all:
        if date_all not in set_1 and date_all not in set_2:
            print(date_all)
    return ((str(round(threshold * 100, 2)) + "%," + i_time + ',' + str(over_threshold_amount) + ","
             + str(same_trend_amount) + "," + str(same_trend_changes_avg) + "%,"
             + str(v_trend_amount)) + "," + str(v_trend_changes_avg) + "%,"
            + str(changes_avg) + "%")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # columns = ['tic','datadate','cshtrd','prccd','prchd','prcld','prcod']
    # split_underlying_symbols("/Volumes/data/underlying2.csv",columns, 10000)
    # print("test finished")
    res_columns_str = ("threshold,i_time,over_threshold_amount,same_trend_amount_amount,same_trend_changes_avg,"
                       "v_trend_amount,v_trend_changes_avg, changes_avg")

    column_list = res_columns_str.split(",")


    columns = ['date', 'time', 'open', 'high', 'low', 'close', 'volume']
    qqq_file_path = '/Volumes/data/data/QQQ_19990310_20091231/QQQ_19990310_20091231.csv'
    spy_file_path = '/Volumes/data/data/SPY_19980102_20091231/SPY_19980102_20091231.txt'
    threshold_start = -200
    threshold_end = 201
    i_time = '11:30'
    with open('output_SPY.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(column_list)
    for i in range(threshold_start, threshold_end, 25):
        threshold = round(i / 10000, 4)
        print(threshold)
        #row_data = statTrend(qqq_file_path, columns, threshold, i_time)
        row_data = statTrend(spy_file_path, columns, threshold, i_time)

        with open('output_SPY.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row_data.split(','))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
