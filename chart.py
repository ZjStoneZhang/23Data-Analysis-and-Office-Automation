import os
import re
import json
from pyecharts.charts import Bar, Timeline, Grid
from pyecharts.options import *
import pyecharts.options as opts
from pyecharts.globals import ThemeType
import csv
import pandas as pd


def makecharts(t, wsite):

    # 用t时间点后的90个数据作图
    if wsite == 1:
        path = './data/WB'
        w_type = '微博'
    elif wsite == 2:
        path = './data/BD'
        w_type = '百度'
    elif wsite == 3:
        path = './data/ZH'
        w_type = '知乎'

    t_reform = t[0] + '月' + t[1] + '日' + t[2] + '时' + w_type + '热搜'

    data_dict = dict()
    files = os.listdir(path)

    k = 0
    name = []
    check = 0

    for file in files:
        if check == 0:
            if file[0:6] == t[0] + t[1] + t[2]:
                check = 1
            else:
                continue
        position = path + '\\' + file
        name.append(file[0:7])
        f = open(position, 'r', encoding='utf-8')
        data = f.readlines()

        f.close()

        data.pop(0)
        number = k
        k += 1

        for line in data:
            title = line.split(',')[1]
            rank = int(line.split(',')[2])
            try:
                data_dict[number].append([title, rank])
            except KeyError:
                data_dict[number] = [[title, rank]]
        if k >= 90:
            break

    timeline = Timeline(init_opts=InitOpts(width='1440px', height='1020px', theme=ThemeType.LIGHT))

    k = 0
    # 组装数据到 Bar 对象中，并添加到 timeline 中
    for number in data_dict.keys():
        t = name[k]
        data_dict[number].sort(key=lambda element: element[1], reverse=True)
        n_data = data_dict[number]
        x_data = []
        y_data = []
        for hot in n_data:
            x_data.append(hot[0])
            y_data.append(hot[1])
        # 创建柱状图
        bar = Bar()
        x_data.reverse()
        y_data.reverse()
        # 添加 x y 轴数据
        bar.add_xaxis(x_data)
        bar.add_yaxis("热度", y_data, label_opts=LabelOpts(position='right'),
                      bar_width='60%'
                      )
        # 反转 x y 轴
        bar.reversal_axis()
        # 设置每时间点的图表的标题
        bar.set_global_opts(
            title_opts=TitleOpts(title=t[0:2] + '月' + t[2:4] + '日' + t[4:6] + '时' + t[6:7] + '0分' + w_type + '热度', pos_left='20%')
        )
        k += 1
        # 将 bar 对象添加到 timeline 中
        grid = (
            Grid()
            .add(bar, grid_opts=opts.GridOpts(pos_left="45%"))
        )
        timeline.add(grid, number)

    # 设置自动播放参数
    timeline.add_schema(
        play_interval=1000,  # 自动播放的时间间隔，单位毫秒
        is_timeline_show=True,  # 是否显示自动播放的时候，显示时间线（默认 True）
        is_auto_play=False,  # 是否在自动播放（默认 False）
        is_loop_play=False  # 是否循环自动播放（默认 True）
    )

    # 通过时间线绘图
    timeline.render('./charts/' + t_reform + '.html')

    path = './charts/' + t_reform + '.html'
    timeline.render(path)
    return path
