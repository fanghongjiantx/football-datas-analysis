import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import time 
import os
import pandas as pd
from collections import Counter


#提取西甲历年排名,保存html数据,提取其中排名到xlsx文件中
def get_Lastats(time):
    # 目标URL
    url = "https://fbref.com/en/comps/12/"+str(time)+"-"+str(time+1)+"/"+str(time)+"-"+str(time+1)+"-La-Liga-Stats"
    html_loca='D:/football/stats/html/La_Liga/La_Liga_table_'+str(time)+"-"+str(time+1)+'.html'
    xlsx_loca='D:/football/stats/data/La_Liga/'+str(time)+"-"+str(time+1)+'_data.xlsx'
    # 发起请求
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        # 将源码保存到文件
        with open(html_loca, 'w', encoding='utf-8') as file:
            file.write(soup.prettify())

        # 读取HTML文件
        with open(html_loca, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # 解析HTML
        soup = BeautifulSoup(html_content, 'lxml')

        # 定位到特定的表格
        # 假设我们要找的表格具有类名 'target-table'
        table = soup.find('table', class_='stats_table sortable min_width force_mobilize')
            
        # 创建一个新的Excel工作簿
        wb = Workbook()
        ws = wb.active

        # 遍历表格中的每一行
        for i, row in enumerate(table.find_all('tr')):
            # 获取每一行的所有单元格
            cols = row.find_all(['td', 'th'])
            # 提取单元格中的文本，并去除前后空白字符
            cols_text = [col.get_text(strip=True) for col in cols]
            # 将单元格文本写入Excel工作表的当前行
            ws.append(cols_text)
        # 保存Excel工作簿
        wb.save(xlsx_loca)
        print(str(time)+"-"+str(time+1)+"done")
    else:
        print("请求失败，状态码：", response.status_code)

#统计各支球队在西甲踢过多少赛季
def count_Lateams():
    # 文件夹路径 (放置你的xlsx文件)
    folder_path = 'D:/football/stats/data/La_Liga/'

    # 初始化一个字典，用于统计
    element_counter = {}

    # 遍历所有的xlsx文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.xlsx'):
            file_path = os.path.join(folder_path, filename)
            
            # 读取Excel文件
            df = pd.read_excel(file_path)
            
            # 提取第二列从第二行到最后一行的元素 (假设索引从0开始，第二列为列索引1)
            second_column_elements = df.iloc[0:, 1].dropna()  # iloc[1:] 从第二行开始，列索引1为第二列
            
            # 更新计数器
            for element in second_column_elements:
                if element in element_counter:
                    element_counter[element] += 1
                else:
                    element_counter[element] = 1

    # 将统计结果按数量排序
    element_counter = dict(sorted(element_counter.items(), key=lambda item: item[1], reverse=True))
    # 将统计结果保存到文件
    output_df = pd.DataFrame(element_counter.items(), columns=['Element', 'Count'])
    output_df.to_excel('D:/football/stats/data/La_teams_count.xlsx', index=False)

    # 打印统计结果到终端
    for element, count in element_counter.items():
        print(f"{element}: {count}")
    print(len(element_counter))

#寻找某支球队未在西甲的赛季
def find_team_notin_La(team_name):
     # 文件夹路径 (放置你的xlsx文件)
    folder_path = 'D:/football/stats/data/La_Liga/'

    # 遍历所有的xlsx文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.xlsx'):
            exist=0
            file_path = os.path.join(folder_path, filename)
            
            # 读取Excel文件
            df = pd.read_excel(file_path)
            
            # 提取第二列从第二行到最后一行的元素 (假设索引从0开始，第二列为列索引1)
            second_column_elements = df.iloc[0:, 1].dropna()  # iloc[1:] 从第二行开始，列索引1为第二列
            for i in second_column_elements:
                if team_name==i:
                    exist=1
                    break
            if exist==0:
                print(filename)


def run():
    # for t in range(1988,2024):
    #     get_Lastats(t)
    #     time.sleep(20)

    count_Lateams()

    # find_team_notin_La("Manchester City")


run()