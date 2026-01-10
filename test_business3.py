"""
测试第三业务界面功能
"""

import sys
import os
import pandas as pd

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.utils.data_io import DataImportExport
from backend.services.business_service_3 import BusinessService3


def test_business3():
    """测试第三业务界面功能"""
    print("="*60)
    print("🧪 开始测试第三业务界面功能")
    print("="*60)
    
    try:
        # 读取测试数据
        print("\n📚 读取测试数据...")
        
        # 上年度SEC数据表
        last_year_sec = DataImportExport.read_excel("data/input/SEC数据表-202409_sample.xlsx")
        print(f"✅ 上年度SEC数据表: {len(last_year_sec)}行")
        
        # 单元变化表
        unit_change = DataImportExport.read_excel("data/input/SEC单元变化表-202509_sample.xlsx")
        print(f"✅ 单元变化表: {len(unit_change)}行")
        
        # 老区新井表
        old_area_new_wells = DataImportExport.read_excel("data/input/老区新井表-202509_sample.xlsx")
        print(f"✅ 老区新井表: {len(old_area_new_wells)}行")
        
        # 扩边/PUD转PDP/PDNP表
        pud_pdp_pdnp = DataImportExport.read_excel("data/input/扩边PUD转PDP表-202509_sample.xlsx")
        print(f"✅ 扩边/PUD转PDP/PDNP表: {len(pud_pdp_pdnp)}行")
        
        print("\n⚙️  执行第三业务界面处理...")
        
        # 生成本年度SEC数据表
        result_df = BusinessService3.generate_this_year_sec_table(
            last_year_sec=last_year_sec,
            unit_change_df=unit_change,
            old_area_new_wells=old_area_new_wells,
            pud_pdp_pdnp_df=pud_pdp_pdnp,
            this_year=2025,
            this_year_month=202509
        )
        
        print(f"\n✅ 生成完成！")
        print(f"📊 本年度SEC数据表总计: {len(result_df)}行")
        
        # 验证结果
        print(f"\n🔍 验证结果...")
        print(f"   - 包含字段: {list(result_df.columns)}")
        print(f"   - 年月字段: {result_df['年月'].unique()}")
        print(f"   - 井号数量: {len(result_df['井号'].unique())}")
        
        # 保存结果
        output_file = DataImportExport.save_with_timestamp(
            result_df, 
            "data/output", 
            "202509_本年度SEC数据表_测试结果"
        )
        print(f"\n💾 结果已保存至: {output_file}")
        
        print("\n" + "="*60)
        print("🎉 第三业务界面功能测试成功！")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_business3()
    if success:
        print("\n✅ 测试通过！")
    else:
        print("\n❌ 测试失败！")
        sys.exit(1)