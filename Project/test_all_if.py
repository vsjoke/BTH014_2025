#test_all_if.py
import numpy as np


class CustomClass:
    def __init__(self, x):
        self.x = x


def output_test_case():
    # 基本数据类型 + 边界值
    basic_objects = [
        None,  # None
        True, False,  # 布尔值
        0, 1, -1, 2 ** 31 - 1,  # 整数（包括边界值）
        0.0, 3.14, -1.23,  # 浮点数
        "", "hello",  # 字符串（空和非空）
        b"", b"bytes",  # 字节（空和非空）
    ]

    # 容器类型（列表、字典、集合、元组）
    container_objects = [
        [], [1, "a", None],  # 列表
        {}, {"a": 1, "b": None},  # 字典
        set(), {1, "a", None},  # 集合
        (), (1, "a", None),  # 元组
        frozenset(), frozenset([1, "a", None]),  # 不可变集合
    ]

    # 嵌套结构
    nested_objects = [
        [1, {"a": [2, 3]}],  # 列表嵌套字典
        {"x": (1, 2), "y": [3, 4]},  # 字典嵌套元组和列表
        {1, (2, 3)},  # 集合嵌套元组
    ]

    # 特殊对象和第三方库对象
    special_objects = [
        np.int64(42),  # numpy 整数
        np.array([1, 2, 3]),  # numpy 数组
        CustomClass(10),  # 自定义类实例
        lambda x: x + 1,  # 函数（注：pickle默认不支持，会抛出异常）
    ]

    # 合并所有测试对象
    all_test_objects = (
            basic_objects +
            container_objects +
            nested_objects +
            special_objects
    )
    return all_test_objects