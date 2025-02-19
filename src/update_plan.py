from db import Session,MajorPlanTable

def update_jhrs_from_bz(skip_zero=True, show_progress=True):
    import re
    from tqdm import tqdm  # 需要先安装：pip install tqdm
    
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
                    match = re.search(r'计划.*?(\d+)', record.bz)
                    if match:
                        new_jhrs = int(match.group(1))
                        
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