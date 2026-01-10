"""
测试第四业务界面功能
"""

import sys
import os
import pandas as pd

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.utils.data_io import DataImportExport
from backend.services.business_service_4 import BusinessService4


def generate_test_data():
    """生成测试数据"""
    print("生成第四业务界面测试数据...")
    
    # 创建测试数据目录
    os.makedirs("data/input", exist_ok=True)
    
    # 1. 上年度常规油评估数据表
    last_year_eval_df = pd.DataFrame({
        '油气田': ['油田A', '油田B', '油田A'],
        '评估单元': ['单元1', '单元2', '单元1'],
        '生产时间年': [2024, 2024, 2024],
        '生产时间月': [1, 2, 3],
        '油产量': [1000, 1200, 900],
        '液产量': [2000, 2400, 1800],
        '油井开井数': [10, 12, 9]
    })
    
    # 2. 年度油井SEC单元变化表
    sec_unit_change_df = pd.DataFrame({
        '井号': ['W001', 'W002', 'W003'],
        '上年度SEC油田': ['SEC油田A', 'SEC油田B', 'SEC油田A'],
        '本年度SEC油田': ['SEC油田A', 'SEC油田C', 'SEC油田A'],  # W002变化了油田
        '上年度SEC单元': ['SEC单元1', 'SEC单元2', 'SEC单元1'],
        '本年度SEC单元': ['SEC单元1', 'SEC单元3', 'SEC单元1'],  # W002变化了单元
        '页岩油/常规': ['常规', '常规', '常规']
    })
    
    # 3. 油井历史生产数据
    historical_prod_data_df = pd.DataFrame({
        '井号': ['W001', 'W002', 'W003'],
        '年月': [202401, 202401, 202401],
        '月产油量(t)': [100, 120, 90],
        '月产液量(t)': [200, 240, 180]
    })
    
    # 4. 扩边/PUD转PDP/PDNP数据表
    pud_pdp_pdnp_df = pd.DataFrame({
        '井号': ['W010', 'W011'],
        '大油田': ['油田A', '油田B'],
        '单元': ['单元1', '单元2'],
        'SEC油田': ['SEC油田A', 'SEC油田B'],
        'SEC单元': ['SEC单元1', 'SEC单元2'],
        '页岩油/常规': ['常规', '页岩油']  # 一个常规，一个页岩油
    })
    
    # 5. 老区新井数据表
    old_area_new_wells_df = pd.DataFrame({
        '井号': ['W020', 'W021'],
        '大油田': ['油田A', '油田B'],
        '单元': ['单元1', '单元2'],
        'SEC油田': ['SEC油田A', 'SEC油田B'],
        'SEC单元': ['SEC单元1', 'SEC单元2'],
        '页岩油_常规': ['常规', '常规']
    })
    
    # 6. 上年度SEC数据表
    last_year_sec_df = pd.DataFrame({
        '井号': ['W001', 'W002', 'W003'],
        '大油田': ['油田A', '油田B', '油田A'],
        '单元': ['单元1', '单元2', '单元1'],
        'SEC油田': ['SEC油田A', 'SEC油田B', 'SEC油田A'],
        'SEC单元': ['SEC单元1', 'SEC单元2', 'SEC单元1'],
        '是否参评': ['是', '是', '否'],
        '页岩油/常规': ['常规', '常规', '常规'],
        '年月': [202409, 202409, 202409]
    })
    
    # 7. 本年度SEC数据表
    current_year_sec_df = pd.DataFrame({
        '井号': ['W001', 'W002', 'W003'],
        '大油田': ['油田A', '油田B', '油田A'],
        '单元': ['单元1', '单元3', '单元1'],  # W002单元变化
        'SEC油田': ['SEC油田A', 'SEC油田C', 'SEC油田A'],  # W002油田变化
        'SEC单元': ['SEC单元1', 'SEC单元3', 'SEC单元1'],
        '是否参评': ['是', '是', '否'],
        '页岩油/常规': ['常规', '常规', '常规'],
        '年月': [202509, 202509, 202509]
    })
    
    # 8. A2数据表（12个月数据）
    a2_data_list = []
    for month in range(10, 22):  # 202410 到 202509
        year = 2024 if month <= 12 else 2025
        actual_month = month if month <= 12 else month - 12
        year_month = year * 100 + actual_month
        
        for well in ['W001', 'W002', 'W003', 'W010', 'W011', 'W020', 'W21']:
            a2_data_list.append({
                '井号': well,
                '大油田': '油田A' if well.startswith('W00') or well.startswith('W010') else '油田B',
                '单元': '单元1' if well.startswith('W001') or well.startswith('W010') else '单元2',
                '年月': year_month,
                '月产油量(t)': 100 + (hash(well) % 50),
                '月产液量(t)': 200 + (hash(well) % 100)
            })
    
    a2_data_df = pd.DataFrame(a2_data_list)
    
    # 9. 上年度页岩油评估数据表
    last_year_shale_eval_df = pd.DataFrame({
        '油气田': ['W011', 'W012'],  # 以井号作为油气田
        '评估单元': ['W011', 'W012'],  # 以井号作为评估单元
        '生产时间年': [2024, 2024],
        '生产时间月': [1, 2],
        '油产量': [800, 850],
        '液产量': [1600, 1700],
        '油井开井数': [1, 1]
    })
    
    # 保存测试数据
    DataImportExport.write_excel(last_year_eval_df, "data/input/上年度常规油评估数据表_测试.xlsx")
    DataImportExport.write_excel(sec_unit_change_df, "data/input/年度油井SEC单元变化表_测试.xlsx")
    DataImportExport.write_excel(historical_prod_data_df, "data/input/油井历史生产数据_测试.xlsx")
    DataImportExport.write_excel(pud_pdp_pdnp_df, "data/input/扩边PUD转PDP表_测试.xlsx")
    DataImportExport.write_excel(old_area_new_wells_df, "data/input/老区新井数据表_测试.xlsx")
    DataImportExport.write_excel(last_year_sec_df, "data/input/上年度SEC数据表_测试.xlsx")
    DataImportExport.write_excel(current_year_sec_df, "data/input/本年度SEC数据表_测试.xlsx")
    DataImportExport.write_excel(a2_data_df, "data/input/A2数据表12个月_测试.xlsx")
    DataImportExport.write_excel(last_year_shale_eval_df, "data/input/上年度页岩油评估数据表_测试.xlsx")
    
    print("测试数据生成完成！")
    return {
        'last_year_eval': last_year_eval_df,
        'sec_unit_change': sec_unit_change_df,
        'historical_prod': historical_prod_data_df,
        'pud_pdp_pdnp': pud_pdp_pdnp_df,
        'old_area_new_wells': old_area_new_wells_df,
        'last_year_sec': last_year_sec_df,
        'current_year_sec': current_year_sec_df,
        'a2_data': a2_data_df,
        'last_year_shale_eval': last_year_shale_eval_df
    }


def test_conventional_evaluation():
    """测试常规油评估数据处理"""
    print("="*60)
    print("🧪 开始测试常规油评估数据处理...")
    print("="*60)
    
    try:
        # 生成测试数据
        test_data = generate_test_data()
        
        # 调用业务服务处理常规油评估数据
        result_df = BusinessService4.process_conventional_oil_evaluation(
            last_year_eval_df=test_data['last_year_eval'],
            sec_unit_change_df=test_data['sec_unit_change'],
            historical_prod_data_df=test_data['historical_prod'],
            pud_pdp_pdnp_df=test_data['pud_pdp_pdnp'],
            old_area_new_wells_df=test_data['old_area_new_wells'],
            last_year_sec_df=test_data['last_year_sec'],
            current_year_sec_df=test_data['current_year_sec'],
            a2_data_df=test_data['a2_data']
        )
        
        print(f"✅ 常规油评估数据处理完成！")
        print(f"📊 结果数据表包含 {len(result_df)} 条记录")
        print(f"📋 字段包括: {list(result_df.columns)}")
        
        # 保存结果
        output_file = DataImportExport.save_with_timestamp(
            result_df, 
            "data/output", 
            "测试_常规油评估数据表"
        )
        print(f"💾 结果已保存至: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ 常规油评估数据处理失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_shale_evaluation():
    """测试页岩油评估数据处理"""
    print("\n" + "="*60)
    print("🧪 开始测试页岩油评估数据处理...")
    print("="*60)
    
    try:
        # 生成测试数据
        test_data = generate_test_data()
        
        # 定义评估月份
        evaluation_months = list(range(202410, 202510))  # 202410 到 202509
        evaluation_months.extend([202501, 202502, 202503])  # 添加一些月份
        
        # 调用业务服务处理页岩油评估数据
        result_df = BusinessService4.process_shale_oil_evaluation(
            last_year_shale_eval_df=test_data['last_year_shale_eval'],
            pud_pdp_pdnp_df=test_data['pud_pdp_pdnp'],
            a2_data_df=test_data['a2_data'],
            evaluation_months=evaluation_months[:12]  # 取前12个月
        )
        
        print(f"✅ 页岩油评估数据处理完成！")
        print(f"📊 结果数据表包含 {len(result_df)} 条记录")
        print(f"📋 字段包括: {list(result_df.columns)}")
        
        # 保存结果
        output_file = DataImportExport.save_with_timestamp(
            result_df, 
            "data/output", 
            "测试_页岩油评估数据表"
        )
        print(f"💾 结果已保存至: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ 页岩油评估数据处理失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("🚀 开始测试第四业务界面功能")
    print("="*70)
    
    success_count = 0
    total_tests = 2
    
    # 测试常规油评估
    if test_conventional_evaluation():
        success_count += 1
    
    # 测试页岩油评估
    if test_shale_evaluation():
        success_count += 1
    
    print("\n" + "="*70)
    print(f"✅ 测试完成: {success_count}/{total_tests} 个测试通过")
    
    if success_count == total_tests:
        print("🎉 第四业务界面功能测试全部通过！")
        return True
    else:
        print("⚠️  部分测试未通过，请检查错误信息")
        return False


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)