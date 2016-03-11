from flask import Flask
from flask import request, jsonify
from os import walk
import json

app = Flask(__name__)

# global value define and initial
global data
data = []

global filepath
filepath = 'wifiLoc/dat1'

global k_value
k_value = 10

global data_num
data_num = 200

global class_num
class_num = 10


def get_data_by_name(filename):
    f = open(filename)
    for i in range(data_num):
        line = f.readline()
        s_line = line.split()
        result = [(int)(s_line[1]), (int)(s_line[3]),
                  (int)(s_line[5]), (int)(s_line[7])]
        data[(int)(filename[29])].append(result)


def init():
    for i in range(class_num):
        data.append([i])

    content = walk(filepath)
    for i in content:
        for j in i:
            for k in j:
                if k[-3:] == 'txt':
                    get_data_by_name(filepath + '/' + k)


def eu_distance(vec1, vec2):
    d = 0
    for a, b in zip(vec1, vec2):
        d += (a - b)**2
    return d ** 0.5


def cal_distance_by_eu(RSSI):
    result = []
    for i in data:
        for k in range(data_num):
            distance = eu_distance(RSSI, i[k + 1])
            tmpResult = [i[0], distance]
            result.append(tmpResult)

    result.sort(key=lambda x: x[1])

    count = []
    for i in range(class_num):
        count.append((int)(0))

    for i in range(k_value):
        tmp = result[i]
        ttmp = tmp[0]
        count[(int)(ttmp)] += 1

    max_num = 0
    tmpMax = count[0]
    for i in range(class_num):
        if tmpMax < count[i]:
            tmpMax = count[i]
            max_num = i
    print count
    print max_num

    return max_num


@app.route('/', methods=['POST'])
def get_location():
    if request.method == 'POST':
        strJson = request.get_json()
        tmpRSSI = [(int)(strJson['Asury']), (int)(strJson['Asury2']),
                   (int)(strJson['Asury3']), (int)(strJson['Passion'])]
        print tmpRSSI
        re = {'result': cal_distance_by_eu(tmpRSSI)}
        return json.dumps(re)

if __name__ == '__main__':
    init()
    print data
    app.run()
