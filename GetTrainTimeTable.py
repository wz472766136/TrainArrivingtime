import requests
import json
import argparse


def get_train_timetable(TrainNo):
    r = requests.post('http://www.gtbyxx.com/wxg/inter/ky/getTrainZwd', data=json.dumps({'trainNo': TrainNo}))
    return r.json()


def read_train_list(listtxt):
    with open(listtxt, 'r') as f:
        train_list = f.readlines()
    return train_list


def showresult(result, dst_station):
    data = result['data']
    error = result['error']
    success = result['success']
    if success:
        for dataele in data:
            trainNo = dataele['trainNo']
            sfDate = dataele['sfDate']
            stationInfos = dataele['stationInfos']
            for stationInfo in stationInfos:
                if dst_station == stationInfo['station']:
                    tdTime = stationInfo['tdTime']
                    sjTime = stationInfo['sjTime']
                    late = stationInfo['late']
                    print("车次:", trainNo, ",始发日期:", sfDate, ",到", dst_station)
                    if "" == late:
                        print("预计", tdTime, ",实际", sjTime, ",", "正点")
                    else:
                        print("预计", tdTime, ",实际", sjTime, ",", late)
                    break
    else:
        print(error)


def parse_args():
    """Parse input arguments."""

    parser = argparse.ArgumentParser(description='请指定广铁集团管内的车次及车站')
    parser.add_argument('-trainlist', dest='train_list', help='请将车次添加到目录下trainlist.txt文件中',
                        default='trainlist.txt', type=str)
    parser.add_argument('-dst', dest='dst_station', help='默认车站长沙',
                        default="长沙", type=str)
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()
    train_list = args.train_list
    dst_station = args.dst_station
    train_list = read_train_list(train_list)
    for train in train_list:
        result = get_train_timetable(train)
        showresult(result, dst_station)
