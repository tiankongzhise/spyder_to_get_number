import requests
from urllib.parse import quote
import time
from requests.adapters import HTTPAdapter
import os
from db import Session,AdmissionRecordTable
import pandas as pd
import tqdm

def get_data(school_name):
    # 目标URL
    url = "https://ks.hneao.cn/gaokao/v1/zymk/cj/gzdzbmt/pageGzdzbmtjList"

    # 请求头配置
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Cookie': 'BIGipServerpool_xgk_student=1736708780.893.0000; LOGIN_USER_TYPE=student; C2AT=eyJraWQiOiJ2MmJ2amhjZlNjUzFISzhGQWJocnJRIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJhYyI6IjA1NTExMjE3Iiwic2V4IjoiMiIsImlzcyI6ImMyIiwib3JnaW5zaWRzIjpbIjItMi1lMjU4Zjg4MGZkZWE0YjZlYTU3MDFhNjY3NWQwZjIxOSJdLCJvaWQiOlsiZTI1OGY4ODBmZGVhNGI2ZWE1NzAxYTY2NzVkMGYyMTkiXSwidWlkIjoiNDk3N2E3OTQ0OGFhNDhhYzg5OThjZGJiY2VhZDcwMmUiLCJjZXIiOiI0MzA1MjMyMDA3MDkyMDE1MlgiLCJjZXJ0eXBlIjoib3RoZXIiLCJwaG9uZSI6IjE1NTczOTEzOTk1IiwibmFtZSI6IumCk-WmmSIsInVuIjoi6YKT5aaZIiwid25vIjoiMDU1MTEyMTciLCJleHAiOjE3NDEyNDY3MjYsImFpZCI6IlcxZXNZN3phU2s2d2NHcWZ2SEw1bHciLCJybyI6WyJkZWZhdWx0Il0sImlhdCI6MTczOTk1MDcyNiwiY2lkIjpbIjItMiJdfQ.cDeQXxeEl-iC7anSSEkZN0gjgJYIMvsoHhBxdNBuI0qoA5xMwHxAl7p2NnA53u4QjesyoI60zpHoZEE76VTBTdDGd_eRhszkePubmO5oMSKQGkilyHuhVpHYN1LdB4fM3pbM9ktpxR7SOVavTyi8gYxeC8JUYnLxJ04LIG0OrZs; C2RT=4977a79448aa48ac8998cdbbcead702e.48092c28bf64df603732541ac7bae470; USER_GXQY_ALL=z56oBf7CaDpka4kpJXEElix2FTdOwyaPZuktxrpwVk2BN1yKG09CTi6XpJWtGBrtuYcaCSns+ghnzjb4MwBOE4vnEiM5Qs2u2/c/rfpxn0SQ+ANr7GqCa1fnS2uwvTP+7WFurGfuNH+ZsRouppUllDcGJ7MXR2UxGTlzZrUu+DZaUUX8cnB+VLlpdCyNxF63',
        'Host': 'ks.hneao.cn',
        'Referer': 'https://ks.hneao.cn/student/zymk/gzdzbmtj/gzdzbmtj?dataId=gHvdC726SpiqwxMR9As4zg',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'platform': 'student',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
            
    # 生成13位时间戳
    timestamp = int(time.time() * 1000)
    
    # 构造请求参数
    params = {
        'yxdm': school_name,
        'type': 0,
        '_': timestamp
    }
    try:
        # 发送GET请求
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10,
            # verify=False
        )
        
        # 检查响应状态
        if response.status_code == 200:
            print(f"{school_name}请求成功！")
            rsp_json = response.json()  # 解析JSON响应
    
        else:
            print(f"{school_name}请求失败，状态码：{response.status_code}")
            print("响应内容：", response.text)
            rsp_json = None
    
    except Exception as e:
        print(f"{school_name}发生错误：{str(e)}")
        rsp_json = None
    finally:
         return rsp_json
#从学校选择.xlsx的Sheet1中获取学校名称,值在学校名称列。
def get_school_names():
    school_names = []
    try:
        # 读取Excel文件
        df = pd.read_excel('学校选择.xlsx', sheet_name='Sheet1')
        # 获取学校名称列
        school_names = df['学校名称'].tolist()
    except Exception as e:
        print(f"发生错误：{str(e)}")
    finally:
        return school_names

def main():
    session = Session()
    school_list = get_school_names()
    fail_list = []
    err_log = './err'
    #加一个进度条
    for school_name in tqdm.tqdm(school_list, desc="进度条"):
        rsp_json = get_data(school_name)
        result = rsp_json['result']
        try:
            if not result:
                print(f"{school_name}没有数据")
                continue
            session.bulk_insert_mappings(AdmissionRecordTable, result)
            session.commit()
            print(f"{school_name}数据已保存到数据库！")
        except Exception as e:
            print(f"保存数据到数据库时出错：{e}")
            fail_list.append({'school':school_name,"error":str(e)})
            session.rollback()
        # 限速1秒
        time.sleep(1)
    
    if fail_list:
        if not os.path.exists(err_log):
            os.makedirs(err_log)
        err_log_file = os.path.join(err_log, 'err_log.txt')


        with open(err_log_file, 'w', encoding='utf-8') as file:
            for item in fail_list:
                file.write(f"学校名称: {item['school']}\n错误信息: {item['error']}\n\n")
        print(f"保存错误日志到 {err_log}")
    
def debug(school_name):
    session = Session()
    rsp_json = get_data(school_name)
    result = rsp_json['result']
    try:
        session.bulk_insert_mappings(AdmissionRecordTable, result)
        session.commit()
        print(f"{school_name}数据已保存到数据库！")
    except Exception as e:
        print(f"保存数据到数据库时出错：{e}")
        session.rollback()
    print("result:")
    print(result)

if __name__ == "__main__":
    # main()
    debug('怀化师范高等专科学校')
