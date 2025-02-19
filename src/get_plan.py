import requests
from urllib.parse import quote
import time
from requests.adapters import HTTPAdapter
import urllib3
from db import Session,MajorTable,AdmissionRecordTable
import pandas as pd
import copy



class GetDanZhaoServer(object):
    def __init__(self):
        self.headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Cookie': 'BIGipServerpool_xgk_student=1736708780.893.0000; LOGIN_USER_TYPE=student; C2AT=eyJraWQiOiJ2MmJ2amhjZlNjUzFISzhGQWJocnJRIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJhYyI6IjA1NTExMjE3Iiwic2V4IjoiMiIsImlzcyI6ImMyIiwib3JnaW5zaWRzIjpbIjItMi1lMjU4Zjg4MGZkZWE0YjZlYTU3MDFhNjY3NWQwZjIxOSJdLCJvaWQiOlsiZTI1OGY4ODBmZGVhNGI2ZWE1NzAxYTY2NzVkMGYyMTkiXSwidWlkIjoiNDk3N2E3OTQ0OGFhNDhhYzg5OThjZGJiY2VhZDcwMmUiLCJjZXIiOiI0MzA1MjMyMDA3MDkyMDE1MlgiLCJjZXJ0eXBlIjoib3RoZXIiLCJwaG9uZSI6IjE1NTczOTEzOTk1IiwibmFtZSI6IumCk-WmmSIsInVuIjoi6YKT5aaZIiwid25vIjoiMDU1MTEyMTciLCJleHAiOjE3NDEyNDY3MjYsImFpZCI6IlcxZXNZN3phU2s2d2NHcWZ2SEw1bHciLCJybyI6WyJkZWZhdWx0Il0sImlhdCI6MTczOTk1MDcyNiwiY2lkIjpbIjItMiJdfQ.cDeQXxeEl-iC7anSSEkZN0gjgJYIMvsoHhBxdNBuI0qoA5xMwHxAl7p2NnA53u4QjesyoI60zpHoZEE76VTBTdDGd_eRhszkePubmO5oMSKQGkilyHuhVpHYN1LdB4fM3pbM9ktpxR7SOVavTyi8gYxeC8JUYnLxJ04LIG0OrZs; C2RT=4977a79448aa48ac8998cdbbcead702e.48092c28bf64df603732541ac7bae470; USER_GXQY_ALL=z56oBf7CaDpka4kpJXEElix2FTdOwyaPZuktxrpwVk2BN1yKG09CTi6XpJWtGBrtuYcaCSns+ghnzjb4MwBOE4vnEiM5Qs2u2/c/rfpxn0SQ+ANr7GqCa1fnS2uwvTP+7WFurGfuNH+ZsRouppUllDcGJ7MXR2UxGTlzZrUu+DZaUUX8cnB+VLlpdCyNxF63',
        'Host': 'ks.hneao.cn',
        'Referer': 'https://ks.hneao.cn',
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
        self.session = None
        
    def query(self,url,headers,params):
        # 生成13位时间戳
        timestamp = int(time.time() * 1000)
        params['_'] = timestamp
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
                print(f"请求成功！")
                rsp_json = response.json()  # 解析JSON响应
        
            else:
                print(f"请求失败，状态码：{response.status_code}")
                print("响应内容：", response.text)
                rsp_json = None
        
        except Exception as e:
            print(f"发生错误：{str(e)}")
            rsp_json = None
        finally:
            return rsp_json

    def get_jhrs(self,zyzdm:str|int,yxdh:str|int)->dict|None:
        # 目标URL
        url = "https://ks.hneao.cn/gaokao/v1/volunteer/yxjhk/zypage"
        # 构造请求参数
        params = {
            'pageSize':100,
            'pageNo':1,
            'zyzdm':zyzdm,
            'yxdh':yxdh,
            'lqpc':'g',
            "jhkl":'g',
            "jhlb":'g2',
            "jhxz":0,
            "tbrcdm":10,
            "zylxdm":3,
            "kskmyq":"不限",
        }
        headers = copy.deepcopy(self.headers)
        headers['Referer'] = 'https://ks.hneao.cn/student/volunteer/volunteerSystem/zyzZyList?data=%7B%22sf985%22:null,%22zyzmc%22:%22%E9%AB%98%E8%81%8C%E5%8D%95%E6%8B%9B%E4%B8%8D%E5%88%86%E7%BB%84%22,%22zysl%22:%2214%22,%22tbrcdm%22:%2210%22,%22djsdm%22:null,%22pcdm%22:%22g%22,%22zydz%22:null,%22yxmc%22:%22%E9%95%BF%E6%B2%99%E8%88%AA%E7%A9%BA%E8%81%8C%E4%B8%9A%E6%8A%80%E6%9C%AF%E5%AD%A6%E9%99%A2%22,%22jhrs%22:%220%22,%22yxdm%22:%2212055%22,%22jhlbdm%22:%22g2%22,%22zyzbh%22:%22002%22,%22sfysc%22:false,%22zyzdm%22:%229102000000%22,%22sfyjtjzycgk%22:null,%22sfsyl%22:null,%22kldm%22:%22g%22,%22jhxzdm%22:%220%22,%22yxdh%22:%224328%22,%22sfgb%22:null,%22sf211%22:null,%22kskmyq%22:%22%E4%B8%8D%E9%99%90%22,%22ssdm%22:null,%22tbrcmc%22:%22%E9%AB%98%E8%81%8C%E5%8D%95%E6%8B%9B%E6%89%B9%22,%22pcmc%22:%22%E9%AB%98%E8%81%8C%E5%8D%95%E6%8B%9B%E6%89%B9%22,%22klmc%22:%22%E9%AB%98%E8%81%8C%E5%8D%95%E6%8B%9B%E7%B1%BB%22,%22jhlbmc%22:%22%E4%B8%AD%E8%81%8C%E5%92%8C%E5%BE%80%E5%B1%8A%E6%99%AE%E9%AB%98%E5%8F%8A%E5%90%8C%E7%AD%89%E5%AD%A6%E5%8A%9B%E8%80%83%E7%94%9F%22,%22zylxdm%22:%223%22,%22flmc%22:%22%E9%AB%98%E8%81%8C%E5%8D%95%E6%8B%9B%E6%89%B9%22%7D'
        print(f'院校代号:{yxdh},专业组代码{zyzdm}开始查询专业招生计划')
        return self.query(url,headers,params)

    
    def get_zyzdm(self,yxdh:str|int)->dict|None:
        # 目标URL
        url = "https://ks.hneao.cn/gaokao/v1/volunteer/yxjhk/zyzpage"
                # 构造请求参数
        params = {
            'pageSize':100,
            'pageNo':1,
            'tbrcdm':10,
            'pcdm':'g',
            'kldm':'g',
            "jhxzdm":0,
            "jhlbdm":'g2',
            "zylxdm":3,
            "lqpc":'g',
            "jhkl":'g',
            "jhxz":0,
            "jhlb":'g2',
            'yxdh':yxdh
        }
        headers = copy.deepcopy(self.headers)
        headers['Referer'] = 'https://ks.hneao.cn/student/volunteer/volunteerSystem/yxjhcx'
        print(f'院校代号:{yxdh}开始查询专业组')
        return self.query(url,headers,params)
    
    def save_majors(self,data_list):
        if self.session is None:
            self.create_session()

        try:
            self.session.bulk_insert_mappings(MajorTable, data_list)
            self.session.commit()
            print(f"成功插入")
            return True
        except Exception as e:
            self.session.rollback()
            print(f"插入数据时发生错误: {str(e)}")
            return False
    def create_session(self):
        self.session = Session()

    def close_session(self):
        if self.session is not None:
            self.session.close()
            self.session = None
    def get_distinct_yxdh_raw(self):
        try:
            if self.session is None:
                self.create_session()

            # 执行DISTINCT查询
            distinct_yxdm = self.session.query(AdmissionRecordTable.yxdh.distinct()).all()
        
            # 将结果转换为简单列表 [注意：查询结果返回的是元组列表]
            return [item[0] for item in distinct_yxdm if item[0] is not None]

        except Exception as e:
            print(f"SQL执行错误: {str(e)}")
            return []



if __name__ == "__main__":
    danzhao_server = GetDanZhaoServer()
    yxdh_list = danzhao_server.get_distinct_yxdh_raw()
    fail_list = []
    for yxdh in yxdh_list:
        zyzdm_rsp = danzhao_server.get_zyzdm(yxdh)
        if zyzdm_rsp is None or zyzdm_rsp['code']!=200:
            fail_list.append({'yxdh':yxdh,'zyzdm':'全部'})
            print(f'院校代号:{yxdh}查询专业组失败')
            continue
        zyzdm_list = zyzdm_rsp['result']['records']
        for zyzdm_item in zyzdm_list:
            zyzdm = zyzdm_item['zyzdm']
            jhrs_rsp = danzhao_server.get_jhrs(zyzdm,yxdh)
            if jhrs_rsp is None or jhrs_rsp['code']!=200:
                fail_list.append({'yxdh':yxdh,'zyzdm':zyzdm})
                print(f'院校代号:{yxdh},专业组代码{zyzdm}查询专业招生计划失败')
                continue
            jhrs_list = jhrs_rsp['result']['records']
            print(f'院校代号:{yxdh},专业组代码{zyzdm},招生计划开始保存到数据库')
            insert_result = danzhao_server.save_majors(jhrs_list)
            if not insert_result:
                fail_list.append({'yxdh':yxdh,'zyzdm':zyzdm})
                print(f'院校代号:{yxdh},专业组代码{zyzdm}保存到数据库失败')
            time.sleep(1)
    
    danzhao_server.close_session()
