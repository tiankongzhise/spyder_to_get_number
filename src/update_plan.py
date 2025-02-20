from db import Session,MajorPlanTable
import re
from tqdm import tqdm  # 需要先安装：pip install tqdm

def get_new_jhrs_from_bz(bz):
    if '计划' in bz:
        match = re.search(r'计划.*?(\d+)', bz)
        if match:
            print(f'bz找到计划并获取到招生人数')
            return int(match.group(1))
        else:
            print(f'bz找到计划，但是未获取到招生人数')
            return 0
    if '共' in bz:
        match = re.search(r'共.*?(\d+)', bz)
        if match:
            print(f'bz找到共并获取到招生人数')
            return int(match.group(1))
        else:
            print(f'bz找到共，但是未获取到招生人数')
            return 0
    match = re.search(r'(\d+)', bz)
    if match:
        print(f'bz未匹配到关键字，但是获取到招生人数')
        return int(match.group(1))
    else:
        print(f'bz未匹配到关键字，也未获取到招生人数')
        return 0


def update_jhrs_from_bz(skip_zero=True, show_progress=True):

    
    with Session() as session:
        try:
            # 获取总记录数
            total = session.query(MajorPlanTable).filter(MajorPlanTable.jhrs == 0).count()
            records = session.query(MajorPlanTable).filter(MajorPlanTable.jhrs == 0)
            
            updated_count = 0
            skipped_zero = 0
            format_errors = 0
            
            # 使用进度条
            iterator = tqdm(records, total=total) if show_progress else records
            for record in iterator:
                try:
                        new_jhrs = get_new_jhrs_from_bz(record.bz)
                        
                        print(f'更新计划人数：{new_jhrs}')
                        
                        # 跳过0值处理
                        if skip_zero and new_jhrs == 0:
                            skipped_zero += 1
                            continue
                            
                        record.jhrs = new_jhrs
                        updated_count += 1
                except ValueError:
                    format_errors += 1

            session.commit()
            print(f"\n更新完成：{updated_count}条成功 | {skipped_zero}条跳过零值 | {format_errors}条格式错误")
            
        except Exception as e:
            session.rollback()
            print(f"\n更新失败: {str(e)}")
if __name__ == "__main__":
    update_jhrs_from_bz(skip_zero=True, show_progress=True)