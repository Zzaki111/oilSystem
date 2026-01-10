"""
数据模型定义
定义A2数据表、SEC数据表、评估数据表的数据结构
"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class A2Record:
    """A2数据表记录"""
    井号: str
    大油田: str
    单元: str
    井别: str
    井型: str
    油藏类型: str
    当前层位: str
    关闭层位: str
    年月: int  # 6位数字，如202309
    投产日期: str
    生产天数: float
    月产液量: float
    月产油量: float
    月产水量: float
    月产气量: float
    核实月产液量: float = 0.0
    核实月产油量: float = 0.0
    核实月产水量: float = 0.0
    核实月产气量: float = 0.0


@dataclass
class SECRecord:
    """SEC数据表记录"""
    井号: str
    大油田: str
    单元: str
    井别: str
    井型: str
    油藏类型: str
    当前层位: str
    关闭层位: str
    年月: int
    投产日期: str
    生产天数: float
    月产液量: float
    月产油量: float
    月产水量: float
    月产气量: float
    核实月产液量: float = 0.0
    核实月产油量: float = 0.0
    核实月产水量: float = 0.0
    核实月产气量: float = 0.0
    # SEC特有字段
    SEC油田: str = ""
    SEC单元: str = ""
    是否参评: str = "是"
    页岩油_常规: str = "常规"
    扩边_PUD转PDP_PDNP: str = ""


@dataclass
class EvaluationRecord:
    """评估数据表记录"""
    油田公司: str
    油气田: str
    评估单元: str
    生产时间年: int
    生产时间月: int
    油产量: float = 0.0
    气产量: float = 0.0
    水产量: float = 0.0
    轻烃产量: float = 0.0
    油井开井数: int = 0


@dataclass
class WellUnitAttribute:
    """油井单元属性记录"""
    井号: str
    年月: int
    是否参评: str
    A2油田: str
    A2单元: str
    SEC油田: str = ""
    SEC单元: str = ""


@dataclass
class UnitChangeRecord:
    """单元变化记录"""
    井号: str
    上年度大油田: str
    本年度大油田: str
    上年度单元: str
    本年度单元: str
    大油田变化: str = ""
    单元变化: str = ""
    投产日期: str = ""
    油藏类型: str = ""


@dataclass
class NewWellRecord:
    """新井记录"""
    井号: str
    大油田: str
    单元: str
    井别: str
    井型: str
    油藏类型: str
    投产日期: str
    当前层位: str
    关闭层位: str
    新井类型: str = "老区新井"  # 老区新井、扩边井、PUD转PDP、PUD转PDNP
    SEC油田: str = ""
    SEC单元: str = ""
    页岩油_常规: str = "常规"


# 字段名称常量
class A2Fields:
    """A2数据表字段名称"""
    井号 = "井号"
    大油田 = "大油田"
    单元 = "单元"
    井别 = "井别"
    井型 = "井型"
    油藏类型 = "油藏类型"
    当前层位 = "当前层位"
    关闭层位 = "关闭层位"
    年月 = "年月"
    投产日期 = "投产日期"
    生产天数 = "生产天数(d)"
    月产液量 = "月产液量(t)"
    月产油量 = "月产油量(t)"
    月产水量 = "月产水量(m3)"
    月产气量 = "月产气量(10^4m3)"
    核实月产液量 = "核实月产液量(t)"
    核实月产油量 = "核实月产油量(t)"
    核实月产水量 = "核实月产水量(m3)"
    核实月产气量 = "核实月产气量(10^4m3)"


class SECFields:
    """SEC数据表字段名称"""
    井号 = "井号"
    大油田 = "大油田"
    单元 = "单元"
    井别 = "井别"
    井型 = "井型"
    油藏类型 = "油藏类型"
    当前层位 = "当前层位"
    关闭层位 = "关闭层位"
    年月 = "年月"
    投产日期 = "投产日期"
    生产天数 = "生产天数(d)"
    月产液量 = "月产液量(t)"
    月产油量 = "月产油量(t)"
    月产水量 = "月产水量(m3)"
    月产气量 = "月产气量(10^4m3)"
    核实月产液量 = "核实月产液量(t)"
    核实月产油量 = "核实月产油量(t)"
    核实月产水量 = "核实月产水量(m3)"
    核实月产气量 = "核实月产气量(10^4m3)"
    SEC油田 = "SEC油田"
    SEC单元 = "SEC单元"
    是否参评 = "是否参评"
    页岩油_常规 = "页岩油/常规"
    扩边_PUD转PDP_PDNP = "扩边/PUD转PDP/PDNP"


class EvaluationFields:
    """评估数据表字段名称"""
    油田公司 = "油田公司"
    油气田 = "油气田"
    评估单元 = "评估单元"
    生产时间年 = "生产时间年"
    生产时间月 = "生产时间月"
    油产量 = "油"
    气产量 = "气"
    水产量 = "水"
    轻烃产量 = "轻烃"
    油井开井数 = "油井开井数"
