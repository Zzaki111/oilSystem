"""
使用示例脚本
演示如何使用各个业务服务
"""

import sys
import os
import pandas as pd

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.utils.data_io import DataImportExport
from backend.services.business_service_1 import BusinessService1
from backend.services.business_service_2 import BusinessService2
from backend.services.business_service_3 import BusinessService3
from backend.services.business_service_4 import BusinessService4


def example_business_1():
    """第一业务界面示例"""
    print("\n" + "="*50)
    print("第一业务界面：对比A2表与SEC表")
    print("="*50)
    
    # 创建示例数据
    a2_data = {
        "井号": ["W001", "W002", "W003", "W004"],
        "大油田": ["油田A", "油田A", "油田B", "油田B"],
        "单元": ["单元1", "单元1", "单元2", "单元2"],
        "年月": [202409, 202409, 202409, 202409],
        "月产油量(t)": [100, 150, 120, 90]
    }
    
    sec_data = {
        "井号": ["W001", "W002", "W003"],
        "SEC油田": ["SEC油田A", "SEC油田A", "SEC油田B"],
        "SEC单元": ["SEC单元1", "SEC单元1", "SEC单元2"]
    }
    
    a2_df = pd.DataFrame(a2_data)
    sec_df = pd.DataFrame(sec_data)
    
    # 执行对比
    result_df = BusinessService1.compare_a2_sec_tables(a2_df, sec_df, 202409)
    print("\n油井单元属性表：")
    print(result_df)
    
    # 构建树形结构
    tree = BusinessService1.build_tree_structure(sec_df)
    print("\n树形结构：")
    print(tree)


def example_business_2():
    """第二业务界面示例"""
    print("\n" + "="*50)
    print("第二业务界面：对比本年度与上年度A2表")
    print("="*50)
    
    # 上年度A2数据
    last_year_data = {
        "井号": ["W001", "W002", "W003"],
        "大油田": ["油田A", "油田A", "油田B"],
        "单元": ["单元1", "单元1", "单元2"],
        "年月": [202409, 202409, 202409]
    }
    
    # 本年度A2数据
    this_year_data = {
        "井号": ["W001", "W002", "W004", "W005"],
        "大油田": ["油田A", "油田B", "油田B", "油田A"],
        "单元": ["单元1", "单元2", "单元2", "单元1"],
        "年月": [202509, 202509, 202509, 202509]
    }
    
    last_year_df = pd.DataFrame(last_year_data)
    this_year_df = pd.DataFrame(this_year_data)
    
    # 执行对比
    result = BusinessService2.compare_a2_tables(last_year_df, this_year_df)
    
    print("\n注销井：")
    print(result['cancelled_wells'])
    
    print("\n新投井：")
    print(result['new_wells'])
    
    print("\n单元变化井：")
    print(result['unit_changed_wells'])


def example_business_3():
    """第三业务界面示例"""
    print("\n" + "="*50)
    print("第三业务界面：生成本年度SEC数据表")
    print("="*50)
    
    # 上年度SEC数据
    last_year_sec = pd.DataFrame({
        "井号": ["W001", "W002"],
        "SEC油田": ["SEC油田A", "SEC油田A"],
        "SEC单元": ["SEC单元1", "SEC单元1"],
        "是否参评": ["是", "是"]
    })
    
    # 单元变化数据
    unit_change = pd.DataFrame({
        "井号": ["W002"],
        "本年度大油田": ["油田B"],
        "本年度单元": ["单元2"]
    })
    
    # 老区新井
    old_area_wells = pd.DataFrame({
        "井号": ["W005"],
        "大油田": ["油田A"],
        "单元": ["单元1"],
        "新井类型": ["老区新井"]
    })
    
    # 生成本年度SEC表
    result_df = BusinessService3.generate_this_year_sec_table(
        last_year_sec,
        unit_change,
        old_area_wells,
        pd.DataFrame(),
        2025,
        202509
    )
    
    print("\n本年度SEC数据表：")
    print(result_df)


def create_sample_data():
    """创建示例数据文件"""
    print("\n" + "="*50)
    print("创建示例数据文件")
    print("="*50)
    
    output_dir = "data/input"
    os.makedirs(output_dir, exist_ok=True)
    
    # A2数据示例
    a2_sample = pd.DataFrame({
        "井号": [f"W{str(i).zfill(3)}" for i in range(1, 101)],
        "大油田": ["油田A"] * 50 + ["油田B"] * 50,
        "单元": ["单元1"] * 25 + ["单元2"] * 25 + ["单元3"] * 25 + ["单元4"] * 25,
        "井别": ["采油井"] * 100,
        "井型": ["直井"] * 80 + ["水平井"] * 20,
        "油藏类型": ["常规"] * 90 + ["页岩油"] * 10,
        "当前层位": ["层位1"] * 100,
        "关闭层位": [""] * 100,
        "年月": [202409] * 100,
        "投产日期": ["2020-01-01"] * 100,
        "生产天数(d)": [30] * 100,
        "月产液量(t)": [200 + i*5 for i in range(100)],
        "月产油量(t)": [100 + i*3 for i in range(100)],
        "月产水量(m3)": [100 + i*2 for i in range(100)],
        "月产气量(10^4m3)": [10 + i*0.5 for i in range(100)]
    })
    
    a2_file = os.path.join(output_dir, "a2-202409_sample.xlsx")
    DataImportExport.write_excel(a2_sample, a2_file)
    print(f"已创建A2示例文件: {a2_file}")
    
    # SEC数据示例
    sec_sample = pd.DataFrame({
        "井号": [f"W{str(i).zfill(3)}" for i in range(1, 91)],
        "大油田": ["油田A"] * 45 + ["油田B"] * 45,
        "单元": ["单元1"] * 22 + ["单元2"] * 23 + ["单元3"] * 22 + ["单元4"] * 23,
        "SEC油田": ["SEC油田A"] * 45 + ["SEC油田B"] * 45,
        "SEC单元": ["SEC单元1"] * 45 + ["SEC单元2"] * 45,
        "是否参评": ["是"] * 90,
        "页岩油/常规": ["常规"] * 80 + ["页岩油"] * 10,
        "年月": [202409] * 90
    })
    
    sec_file = os.path.join(output_dir, "SEC数据表-202409_sample.xlsx")
    DataImportExport.write_excel(sec_sample, sec_file)
    print(f"已创建SEC示例文件: {sec_file}")
    
    print("\n示例数据文件创建完成！")


if __name__ == "__main__":
    print("石油生产数据预处理系统 - 使用示例")
    print("=" * 60)
    
    # 创建示例数据
    create_sample_data()
    
    # 运行示例
    example_business_1()
    example_business_2()
    example_business_3()
    
    print("\n" + "="*60)
    print("示例运行完成！")
    print("请参考以上示例代码，根据实际需求调用相应的服务。")
    print("="*60)
