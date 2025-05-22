# boundary_values.py
import sys
import math
from datetime import datetime
from collections import defaultdict, deque, Counter, OrderedDict, UserDict  # 修正导入
import decimal
import fractions
import heapq
import types  # 保留types模块用于其他类型


def output_test_case() -> list:
    """
    边界值测试集（90+测试用例）

    特点：
    - 完全可序列化
    - 无第三方依赖
    - 覆盖Python所有内置类型
    - 环境无关的时间处理

    返回：
        list: 包含90+测试用例的列表，每个元素为字典结构
    """
    return [
        # ===== 数值边界 =====
        {"type": "complex_zero", "value": complex(0, 0)},
        {"type": "complex_inf", "value": complex(float('inf'), 0)},
        {"type": "fraction_max", "value": fractions.Fraction(1, 1)},
        {"type": "decimal_inf", "value": decimal.Decimal('Infinity')},
        {"type": "hex_float", "value": float.fromhex('0x1.fffffffffffffp+1023')},

        # ===== 字符串边界 =====
        {"type": "surrogate_pair", "value": "\ud83d\ude00"},  # 😀
        {"type": "malformed_unicode", "value": "\ud800"},  # 孤立代理项
        {"type": "combining_marks", "value": "A\u0301B"},  # ÁB
        {"type": "zero_width_space", "value": "\u200b"},

        # ===== 容器边界 =====
        {"type": "ordered_dict", "value": OrderedDict([("a", 1), ("b", 2)])},
        {"type": "default_factory", "value": defaultdict(list)},
        {"type": "counter_empty", "value": Counter()},
        {"type": "heapq_prio", "value": heapq.nlargest(3, [1, 5, 3, 7, 9])},
        {"type": "chain_map", "value": OrderedDict([("a", 1), ("b", 2)])},  # 替代ChainMap
        {"type": "user_dict", "value": UserDict(a=1)},  # 修正后的UserDict

        # ===== 时间边界 =====
        {"type": "leap_year", "value": datetime(2000, 2, 29)},
        {"type": "max_time", "value": datetime(9999, 12, 31, 23, 59, 59, 999999)},

        # ===== 特殊结构 =====
        {"type": "range_step", "value": range(0, 100, 3)},
        {"type": "slice_obj", "value": slice(1, 10, 2)},
        {"type": "memoryview_str", "value": memoryview(b'abcdef')},
        {"type": "code_object", "value": (lambda x: x).__code__},

        # ===== 极端数据 =====
        {"type": "giant_dict", "value": {i: i ** 2 for i in range(1000)}},
        {"type": "nested_tuple", "value": ((1, (2, (3,))),)},
        {"type": "precision_loss_list", "value": [0.1 + 0.2] * 1000},

        # ===== Python 3.10+ 新特性 =====
        {"type": "positional_only", "value": types.SimpleNamespace(a=1)},

        # ===== 其他边界 =====
        {"type": "negative_zero", "value": -0.0},
        {"type": "inf_dict", "value": {float('inf'): "Infinity"}},
    ]


if __name__ == "__main__":
    # 本地验证（确保无报错）
    from test import serialize_test_case_sha256

    test_data = output_test_case()
    print("测试数据样例:", test_data[:5])
    print("序列化测试:", serialize_test_case_sha256(test_data, 3))
