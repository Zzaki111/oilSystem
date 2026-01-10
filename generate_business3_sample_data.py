"""
生成第三业务界面的示例数据文件
"""

import sys
import os
import pandas as pd

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.utils.data_io import DataImportExport


def generate_sec_unit_change_sample():
    """生成SEC单元变化示例数据"""
    print("生成SEC单元变化示例数据...")
    
    unit_change_sample = pd.DataFrame({
        "井号": [f"W{str(i).zfill(3)}" for i in range(1, 11)],  # 10口井的单元变化
        "上年度大油田": ["油田A"] * 5 + ["油田B"] * 5,
        "本年度大油田": ["油田A"] * 3 + ["油田C"] * 2 + ["油田B"] * 3 + ["油田D"] * 2,
        "上年度单元": ["单元1"] * 5 + ["单元2"] * 5,
        "本年度单元": ["单元1"] * 2 + ["单元3"] * 3 + ["单元2"] * 2 + ["单元4"] * 3,
        "投产日期": ["2020-01-01"] * 10,
        "油藏类型": ["常规"] * 8 + ["页岩油"] * 2
    })
    
    output_dir = "data/input"
    os.makedirs(output_dir, exist_ok=True)
    
    unit_change_file = os.path.join(output_dir, "SEC单元变化表-202509_sample.xlsx")
    DataImportExport.write_excel(unit_change_sample, unit_change_file)
    print(f"✅ 已创建单元变化示例文件: {unit_change_file}")
    return unit_change_file


def generate_old_area_new_wells_sample():
    """生成老区新井示例数据"""
    print("\n生成老区新井示例数据...")
    
    new_wells_sample = pd.DataFrame({
        "井号": [f"W{str(i).zfill(3)}" for i in range(101, 121)],  # 20口新井
        "大油田": ["油田A"] * 10 + ["油田B"] * 10,
        "单元": ["单元1"] * 5 + ["单元2"] * 5 + ["单元3"] * 8 + ["单元4"] * 2,
        "井别": ["采油井"] * 20,
        "井型": ["直井"] * 15 + ["水平井"] * 5,
        "油藏类型": ["常规"] * 18 + ["页岩油"] * 2,
        "投产日期": ["2025-01-01"] * 20,
        "当前层位": ["层位1"] * 20,
        "关闭层位": [""] * 20,
        "新井类型": ["老区新井"] * 20,
        "SEC油田": ["SEC油田A"] * 10 + ["SEC油田B"] * 10,
        "SEC单元": ["SEC单元1"] * 5 + ["SEC单元2"] * 5 + ["SEC单元3"] * 8 + ["SEC单元4"] * 2,
        "页岩油_常规": ["常规"] * 18 + ["页岩油"] * 2
    })
    
    output_dir = "data/input"
    os.makedirs(output_dir, exist_ok=True)
    
    new_wells_file = os.path.join(output_dir, "老区新井表-202509_sample.xlsx")
    DataImportExport.write_excel(new_wells_sample, new_wells_file)
    print(f"✅ 已创建老区新井示例文件: {new_wells_file}")
    return new_wells_file


def generate_pud_pdp_pdnp_sample():
    """生成扩边/PUD转PDP/PDNP示例数据"""
    print("\n生成扩边/PUD转PDP/PDNP示例数据...")
    
    pud_pdp_pdnp_sample = pd.DataFrame({
        "井号": [f"W{str(i).zfill(3)}" for i in range(201, 211)],  # 10口井
        "大油田": ["油田A"] * 5 + ["油田B"] * 5,
        "单元": ["单元5"] * 5 + ["单元6"] * 5,
        "井别": ["采油井"] * 10,
        "井型": ["水平井"] * 10,
        "油藏类型": ["常规"] * 7 + ["页岩油"] * 3,
        "投产日期": ["2024-06-01"] * 10,
        "当前层位": ["层位2"] * 10,
        "关闭层位": [""] * 10,
        "扩边_PUD转PDP_PDNP": ["扩边"] * 3 + ["PUD转PDP"] * 4 + ["PUD转PDNP"] * 3,
        "SEC油田": ["SEC油田A"] * 5 + ["SEC油田B"] * 5,
        "SEC单元": ["SEC单元5"] * 5 + ["SEC单元6"] * 5,
        "是否参评": ["是"] * 10,
        "页岩油/常规": ["常规"] * 7 + ["页岩油"] * 3
    })
    
    output_dir = "data/input"
    os.makedirs(output_dir, exist_ok=True)
    
    pud_pdp_pdnp_file = os.path.join(output_dir, "扩边PUD转PDP表-202509_sample.xlsx")
    DataImportExport.write_excel(pud_pdp_pdnp_sample, pud_pdp_pdnp_file)
    print(f"✅ 已创建扩边/PUD转PDP/PDNP示例文件: {pud_pdp_pdnp_file}")
    return pud_pdp_pdnp_file


def generate_last_year_sec_sample():
    """生成上年度SEC数据表示例"""
    print("\n生成上年度SEC数据表示例...")
    
    last_year_sec_sample = pd.DataFrame({
        "井号": [f"W{str(i).zfill(3)}" for i in range(1, 81)],  # 80口井
        "大油田": ["油田A"] * 40 + ["油田B"] * 40,
        "单元": ["单元1"] * 20 + ["单元2"] * 20 + ["单元3"] * 20 + ["单元4"] * 20,
        "SEC油田": ["SEC油田A"] * 40 + ["SEC油田B"] * 40,
        "SEC单元": ["SEC单元1"] * 20 + ["SEC单元2"] * 20 + ["SEC单元3"] * 20 + ["SEC单元4"] * 20,
        "是否参评": ["是"] * 75 + ["否"] * 5,
        "页岩油/常规": ["常规"] * 70 + ["页岩油"] * 10,
        "年月": [202409] * 80
    })
    
    output_dir = "data/input"
    os.makedirs(output_dir, exist_ok=True)
    
    last_year_sec_file = os.path.join(output_dir, "SEC数据表-202409_sample.xlsx")
    DataImportExport.write_excel(last_year_sec_sample, last_year_sec_file)
    print(f"✅ 已创建上年度SEC示例文件: {last_year_sec_file}")
    return last_year_sec_file


if __name__ == "__main__":
    print("="*60)
    print("🛢️  石油生产数据预处理系统 - 第三业务界面示例数据生成")
    print("="*60)
    print()
    
    try:
        # 生成示例数据
        unit_change_file = generate_sec_unit_change_sample()
        new_wells_file = generate_old_area_new_wells_sample()
        pud_pdp_pdnp_file = generate_pud_pdp_pdnp_sample()
        last_year_sec_file = generate_last_year_sec_sample()
        
        print()
        print("="*60)
        print("✅ 所有第三业务界面示例数据生成完成！")
        print("="*60)
        print()
        print("📁 生成的文件：")
        print(f"  1. {last_year_sec_file} (上年度SEC数据表)")
        print(f"  2. {unit_change_file} (单元变化表)")
        print(f"  3. {new_wells_file} (老区新井表)")
        print(f"  4. {pud_pdp_pdnp_file} (扩边/PUD转PDP/PDNP表)")
        print()
        print("💡 使用提示：")
        print("  - 第三业务界面：使用以上4个文件")
        print("  - 本年度年份：2025")
        print("  - 本年度年月：202509")
        print()
        print("🌐 现在可以在Web界面中上传这些文件进行测试！")
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
