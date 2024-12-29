import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk, Button, Label, Frame


def get_data(file_path):
    # 读取Excel文件
    xls = pd.ExcelFile(file_path)

    goal_list = []
    # 遍历所有子表，跳过第一个空表
    for sheet_name in xls.sheet_names[1:]:
        # 用于存储每分钟进球的计数，字典形式
        goal_counts = {i: 0 for i in range(1, 93)}  # 初始化字典，键为1到90分钟
        df = pd.read_excel(xls, sheet_name=sheet_name)

        # 确保第二列存在并且是有效的
        if df.shape[1] > 1:
            goals = df.iloc[:, 1].dropna()  # 获取第二列，并去掉空值

            # 只保留非补时进球（非负数）
            # non_extra_time_goals = goals[goals >= 0]
            for goal in goals:
                if 1 <= goal <= 90:  # 确保进球分钟在1到90之间
                    goal_counts[int(goal)] += 1  # 对应分钟计数加1
                elif -89 <= goal <= -46:
                    goal_counts[int(91)] += 1
                elif goal <= -91:
                    goal_counts[int(92)] += 1
        goal_list.append(goal_counts)

    return goal_list


def get_5min_data(file_path):
    # 读取Excel文件
    xls = pd.ExcelFile(file_path)

    # 用于存储每5分钟进球的计数，字典形式
    goal_counts = {
        f"{i}-{i+4}": 0 for i in range(1, 91, 5)
    }  # 初始化字典，键为1-5, 6-10, ..., 86-90分钟

    # 遍历所有子表，跳过第一个空表
    for sheet_name in xls.sheet_names[1:]:
        df = pd.read_excel(xls, sheet_name=sheet_name)

        # 确保第二列存在并且是有效的
        if df.shape[1] > 1:
            goals = df.iloc[:, 1].dropna()  # 获取第二列，并去掉空值

            # 只保留非补时进球（非负数）
            non_extra_time_goals = goals[goals >= 0]
            for goal in non_extra_time_goals:
                if 1 <= goal <= 90:  # 确保进球分钟在1到90之间
                    # 确定进球属于哪个5分钟区间
                    interval = f"{(goal - 1) // 5 * 5 + 1}-{(goal - 1) // 5 * 5 + 5}"
                    goal_counts[interval] += 1  # 对应区间计数加1

    return goal_counts


def goals_by_time(goal_counts):
    # 按时间升序的图
    plt.figure(figsize=(12, 6))
    sns.barplot(x=goal_counts.index, y=goal_counts.values, order=goal_counts.index)
    plt.title("Goals by Time (Regular Time)")
    plt.xlabel("Minute")
    plt.ylabel("Number of Goals")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("goals_by_time.png")
    plt.show()


def goals_by_num(goal_counts):
    # 按进球数降序的图
    goal_counts_sorted = goal_counts.sort_values(ascending=False)

    plt.figure(figsize=(12, 6))
    sns.barplot(x=goal_counts_sorted.values, y=goal_counts_sorted.index)  # 交换 x 和 y
    plt.title("Goals by Count (Regular Time)")
    plt.xlabel("Number of Goals")
    plt.ylabel("Minute")
    plt.tight_layout()
    plt.savefig("goals_by_count.png")
    plt.show()


def plot_goals_by_count(goal_counts):
    # 按字典值降序排列
    sorted_goal_counts = dict(
        sorted(goal_counts.items(), key=lambda item: item[1], reverse=True)
    )

    plt.figure(figsize=(12, 6))

    x = list(sorted_goal_counts.keys())
    y = list(sorted_goal_counts.values())

    plt.xticks(range(len(x)), x)
    plt.plot(y)

    plt.title("Goals by Minute (Sorted by Count)")
    plt.xlabel("Minute")
    plt.ylabel("Number of Goals")
    plt.tight_layout()
    plt.show()


def run(path):
    data = get_data(path)
    for i in range(10, len(data)):
        goal_sum = 0
        for j in data[i]:
            goal_sum += data[i][j]
        print(
            f"{2004+i}-{2005+i}总进球数{goal_sum},45分钟进球数{data[i][45]},占比{data[i][45]/goal_sum},90分钟进球数{data[i][90]},占比{data[i][90]/goal_sum}"
        )


def main():
    # 调用函数，替换为你的Excel文件路径

    path = "D:\\football\\stats\\data\\goal_stats\\L1_goals.xlsx"
    run(path)



# 创建一些示例图形数据
data = {
    '图1': [1, 2, 3, 4],
    '图2': [4, 3, 2, 1],
    '图3': [2, 3, 4, 5],
}

# 当前显示的图形索引
current_index = 0
keys = list(data.keys())

# 定义全局变量
canvas = None
fig = None
title_label = None
previous_label = None
next_label = None

def show_plot(index):
    global canvas, fig  # 声明全局变量
    plt.clf(fig)  # 清除当前图形
    plt.plot(data[keys[index]], marker='o')
    plt.title(keys[index], fontsize=16)
    plt.xlim(0, 3)
    plt.ylim(0, 5)
    plt.grid(True)
    canvas.draw()
    
    # 更新标题标签
    title_label.config(text=f"当前图: {keys[index]}")
    previous_label.config(text=f"上一张: {keys[(index - 1) % len(data)]}")
    next_label.config(text=f"下一张: {keys[(index + 1) % len(data)]}")

def next_plot():
    global current_index
    current_index = (current_index + 1) % len(data)
    show_plot(current_index)

def previous_plot():
    global current_index
    current_index = (current_index - 1) % len(data)
    show_plot(current_index)

def interface():
    global canvas, fig, title_label, previous_label, next_label  # 声明全局变量
    # 设置Tkinter窗口
    root = Tk()
    root.title("图形切换")
    root.geometry("800x600")  # 增大窗口尺寸

    # 创建图形框架
    frame = Frame(root)
    frame.pack(pady=20)

    # 创建Matplotlib图形
    fig = plt.Figure(figsize=(6, 4))
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack()

    # 创建按钮
    btn_previous = Button(root, text="上一张", command=previous_plot, font=("Arial", 12))
    btn_previous.pack(side='left', padx=20)

    btn_next = Button(root, text="下一张", command=next_plot, font=("Arial", 12))
    btn_next.pack(side='right', padx=20)

    # 添加标题标签
    title_label = Label(root, text="", font=("Arial", 14))
    title_label.pack(pady=10)

    previous_label = Label(root, text="", font=("Arial", 12))
    previous_label.pack(pady=5)

    next_label = Label(root, text="", font=("Arial", 12))
    next_label.pack(pady=5)

    # 初始化显示第一张图
    show_plot(current_index)

    root.mainloop()

interface()
