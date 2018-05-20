import csv
import numpy as np
import pandas as pd
import heapq
import time
import matplotlib.pyplot as plt
import re
import Levenshtein
from pandas import DataFrame, Series
from math import*
from functools import cmp_to_key


data = pd.read_csv('directory.csv')

df = pd.DataFrame(data)

#根据经纬度计算距离
def getDistance(lon1, lat1):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    distance = {}
    lon1, lat1 = map(radians, [lon1, lat1])

    for i, row in df.iterrows():

        lon2 = row['Longitude']
        lat2 = row['Latitude']

        # 将十进制度数转化为弧度
        lon2, lat2 = map(radians, [lon2, lat2])

        # haversine公式
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        r = 6371  # 地球平均半径，单位为公里
        key = row['Store Name']
        distance[key] = c * r * 1000

    return distance


# 找topK小的元素用最大堆
class top_K(object):
    def __init__(self, k):
        self.k = k
        self.data = []

    def Push(self, elem):
        # Reverse elem to convert to max-heap
        elem = -elem
        # Using heap algorighem
        if len(self.data) < self.k:
            heapq.heappush(self.data, elem)
        else:
            topk_small = self.data[0]
            if elem > topk_small:
                heapq.heapreplace(self.data, elem)

    def TopK(self):
        return sorted([-x for x in self.data])


def time_k(k, distance):
    start = time.time()

    K_Startbark = top_K(k)
    for key in distance:
        K_Startbark.Push(distance[key])

    end = time.time()
    q_time = end-start
    return q_time, K_Startbark.TopK()

def visual_k(distance):
    k_list = [100*n for n in range(1, 251)]
    t_list = []
    for k in k_list:
        t_list.append(time_k(k, distance)[0])
    plt.figure()
    plt.plot(k_list, t_list)
    plt.show()

def top_k_search(longitude, latitude, k):
    # longitude, latitude = 144.96, -37.81
    # longitude, latitude = 112.5, 67.89

    start = time.time()
    distance = getDistance(longitude, latitude)
    end = time.time()
    text = "计算距离用时：" + str(end - start) + '\n'
    q_time, heap = time_k(k, distance)
    text += "查询到的店铺及对应距离如下：\n"
    heap = sorted(list(set(heap)))
    for dis in heap:
        for key in distance.keys():
            if dis == distance[key]:
                text += (key + " ----------> " + str(dis)+'\n')
    text += ("本次查询耗时：" + str(q_time + end - start))
    return text


def mycmp(x, y):
    if x[1] > y[1]:
        return 1
    elif x[1] < y[1]:
        return -1
    else:
        if x[0][1] > y[0][1]:
            return 1
        elif x[0][1] < y[0][1]:
            return -1
        else:
            return 0

def keyword_match(keyword, distance, k):
    regex = re.compile(keyword, re.I)
    matched = {}
    unmatched = {}
    sub_matched = {}
    start = time.time()
    for key in distance:
        if regex.search(key):
            matched[key] = distance[key]
        else:
            # 子串匹配
            length = len(keyword)
            index = 0
            i = 0
            while i < length:
                index = key.find(keyword[i], index)
                if index == -1:
                    unmatched[(key, distance[key])] = Levenshtein.distance(keyword, key)
                    break
                i += 1
            if i == length:
                sub_matched[key] = distance[key]

    # assert len(distance) == len(matched) + len(sub_matched) + len(unmatched)

    end = time.time()
    matched = zip(matched.keys(), matched.values())
    # 按照距离排序
    matched = sorted(matched, key=lambda s:s[1])
    # 如果能找到完全匹配的结果
    if len(matched) >= k:
        return matched[:k], [], []
    else:
        sub_matched = zip(sub_matched.keys(), sub_matched.values())
        # 按照距离排序
        sub_matched = sorted(sub_matched, key=lambda s: s[1])
        if len(matched) + len(sub_matched) >= k:
            return matched, sub_matched[:k-len(matched)], []
        else:
            unmatched = zip(unmatched.keys(), unmatched.values())
            unmatched = sorted(unmatched, key=cmp_to_key(mycmp))
            return matched, sub_matched, unmatched[:k-len(matched)-len(sub_matched)]


def top_k_keyword_search(longitude, latitude, k, keyword):
    # longitude, latitude = 144.96, -37.81
    # longitude, latitude = 112.5, 67.89
    # keyword = "bour"
    # k = 100

    start = time.time()
    distance = getDistance(longitude, latitude)
    end = time.time()
    text = "计算距离用时：" + str(end - start) + '\n'
    text += "查询到的店铺如下：" + '\n'

    matched, submatched, editmatched = keyword_match(keyword, distance, k)
    if matched:
        text += ("完全匹配个数：" + str(len(matched)) + '\n')
        for res in matched:
            text += (str(res[0]) + "   " + str(res[1]) + '\n')
    if submatched:
        text += ("---------------------------------------------------------\n子串匹配个数：" + str(len(submatched)) + '\n')
        for res in submatched:
            text += (str(res[0]) + "   " + str(res[1]) + '\n')
    if editmatched:
        text += ("---------------------------------------------------------\n编辑距离个数：" + str(len(editmatched)) + '\n')
        for res in editmatched:
            text += (str(res[0]) + "   " + str(res[1]) + '\n')

    return text


def range_r_search(longitude, latitude, radiu):
    # longitude, latitude = 144.96, -37.81
    # radiu = 5000000
    start = time.time()
    distance = getDistance(longitude, latitude)
    end = time.time()
    text = "计算距离用时：" + str(end - start) + '\n'
    text += "查询到的店铺如下：" + '\n'
    distance = zip(distance.keys(), distance.values())
    distance = sorted(distance, key=lambda s:s[1])
    for dis in distance:
        if dis[1] <= radiu:
            text += (str(dis)+"\n")
    return text


def main():
    # text = range_r_search(144.96, -37.81, 5000000)
    # top_k_search(144.96, -37.81, 10)
    # text = top_k_keyword_search(144.96, -37.81, 200, "bour")
    # print("\n\n\n\n\n", text)
    pass

if __name__ == '__main__':
    main()
