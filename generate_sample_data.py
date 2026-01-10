"""
生成示例数据文件
包含正确的字段名称（带单位）
"""

import sys
import os
import pandas as pd

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.utils.data_io import DataImportExport


def generate_a2_sample():
    """生成A2示例数据"""
    print("生成A2示例数据...")
    
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
    
    output_dir = "data/input"
    os.makedirs(output_dir, exist_ok=True)
    
    a2_file = os.path.join(output_dir, "a2-202409_sample.xlsx")
    DataImportExport.write_excel(a2_sample, a2_file)
    print(f"✅ 已创建A2示例文件: {a2_file}")
    print(f"   包含字段: {list(a2_sample.columns)}")
    return a2_file


def generate_sec_sample():
    """生成SEC示例数据"""
    print("\n生成SEC示例数据...")
    
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
    
    output_dir = "data/input"
    os.makedirs(output_dir, exist_ok=True)
    
    sec_file = os.path.join(output_dir, "SEC数据表-202409_sample.xlsx")
    DataImportExport.write_excel(sec_sample, sec_file)
    print(f"✅ 已创建SEC示例文件: {sec_file}")
    print(f"   包含字段: {list(sec_sample.columns)}")
    return sec_file


def generate_a2_yearly_samples():
    """生成年度对比用的A2示例数据"""
    print("\n生成年度对比A2示例数据...")
    
    # 上年度A2
    last_year_a2 = pd.DataFrame({
        "井号": [f"W{str(i).zfill(3)}" for i in range(1, 81)],
        "大油田": ["油田A"] * 40 + ["油田B"] * 40,
        "单元": ["单元1"] * 20 + ["单元2"] * 20 + ["单元3"] * 20 + ["单元4"] * 20,
        "井别": ["采油井"] * 80,
        "井型": ["直井"] * 60 + ["水平井"] * 20,
        "油藏类型": ["常规"] * 70 + ["页岩油"] * 10,
        "当前层位": ["层位1"] * 80,
        "关闭层位": [""] * 80,
        "年月": [202409] * 80,
        "投产日期": ["2020-01-01"] * 80,
        "生产天数(d)": [30] * 80,
        "月产液量(t)": [200 + i*5 for i in range(80)],
        "月产油量(t)": [100 + i*3 for i in range(80)],
        "月产水量(m3)": [100 + i*2 for i in range(80)],
        "月产气量(10^4m3)": [10 + i*0.5 for i in range(80)]
    })
    
    # 本年度A2（包含注销井、新投井、单元变化井）
    this_year_a2 = pd.DataFrame({
        "井号": [f"W{str(i).zfill(3)}" for i in range(6, 101)],  # W006-W100
        "大油田": ["油田A"] * 47 + ["油田B"] * 48,
        "单元": ["单元1"] * 20 + ["单元2"] * 25 + ["单元3"] * 25 + ["单元4"] * 25,
        "井别": ["采油井"] * 95,
        "井型": ["直井"] * 70 + ["水平井"] * 25,
        "油藏类型": ["常规"] * 85 + ["页岩油"] * 10,
        "当前层位": ["层位1"] * 95,
        "关闭层位": [""] * 95,
        "年月": [202509] * 95,
        "投产日期": ["2020-01-01"] * 95,
        "生产天数(d)": [30] * 95,
        "月产液量(t)": [200 + i*5 for i in range(95)],
        "月产油量(t)": [100 + i*3 for i in range(95)],
        "月产水量(m3)": [100 + i*2 for i in range(95)],
        "月产气量(10^4m3)": [10 + i*0.5 for i in range(95)]
    })
    
    output_dir = "data/input"
    os.makedirs(output_dir, exist_ok=True)
    
    last_year_file = os.path.join(output_dir, "a2-202409_上年度.xlsx")
    this_year_file = os.path.join(output_dir, "a2-202509_本年度.xlsx")
    
    DataImportExport.write_excel(last_year_a2, last_year_file)
    DataImportExport.write_excel(this_year_a2, this_year_file)
    
    print(f"✅ 已创建上年度A2文件: {last_year_file}")
    print(f"✅ 已创建本年度A2文件: {this_year_file}")
    print(f"   注销井数: 5个 (W001-W005)")
    print(f"   新投井数: 20个 (W081-W100)")
    
    return last_year_file, this_year_file


if __name__ == "__main__":
    print("="*60)
    print("🛢️  石油生产数据预处理系统 - 示例数据生成")
    print("="*60)
    print()
    
    try:
        # 生成示例数据
        a2_file = generate_a2_sample()
        sec_file = generate_sec_sample()
        last_year_file, this_year_file = generate_a2_yearly_samples()
        
        print()
        print("="*60)
        print("✅ 所有示例数据生成完成！")
        print("="*60)
        print()
        print("📁 生成的文件：")
        print(f"  1. {a2_file}")
        print(f"  2. {sec_file}")
        print(f"  3. {last_year_file}")
        print(f"  4. {this_year_file}")
        print()
        print("💡 使用提示：")
        print("  - 第一业务界面：使用文件1和文件2")
        print("  - 第二业务界面：使用文件3和文件4")
        print()
        print("🌐 现在可以在Web界面中上传这些文件进行测试！")
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
