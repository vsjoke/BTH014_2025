# equivalence_partitioning.py
import sys


class CustomClass:
    """
    自定义类用于测试对象序列化
    包含多种数据类型属性用于边界测试
    """

    def __init__(self, a, b):
        self.a = a  # 测试多种类型的属性
        self.b = b  # 包含边界值的属性

    def __reduce__(self):
        """确保对象可被正确序列化"""
        return (self.__class__, (self.a, self.b))


def output_test_case(recursive_tuple=None):
    """
    生成等价划分测试数据集

    返回:
        list: 包含多种数据类型的测试用例列表，
        覆盖基本类型/复杂类型/特殊值等价类（已移除边界值）
    """

    # 自引用数据结构构造
    cyclic_list = []
    cyclic_list.append(cyclic_list)

    self_referential_dict = {}
    self_referential_dict['self'] = self_referential_dict

    # 新增递归类型测试
    recursive_list = []
    recursive_list.append(recursive_list)  # 二级自引用列表
    recursive_tuple = ((), recursive_tuple)  # 元组内嵌套递归
    recursive_dict = {"level1": {"level2": {}}}  # 三级嵌套字典
    recursive_dict["level1"]["level2"]["self"] = recursive_dict  # 最深层自引用

    # 长文本生成 
    long_text = ("This is a 1024 chars string." + "x" * 1000)[:1024]

    return [
        # 基本数据类型
        42, -456, 0,
        3.14, -2.71, 0.0,
        True, False, None,

        # 容器类型（保持原有结构）
        [], [1, 2, 3],
        [1, [2, [3]]],
        [True, False, None],
        cyclic_list,

        # 新增递归类型测试
        recursive_list,  # 二级自引用列表
        recursive_tuple,  # 元组递归
        recursive_dict,  # 三层嵌套自引用字典
        {"self": {"deep": {"self": None}}},  # 动态深度自引用
        [[[[]]]],  # 多维空列表
        (((),),),  # 元组递归嵌套
        {"a": {"b": {"c": {"self": None}}}},  # 字典路径递归

        (), (1, 2), (1, (2, 3)),
        {}, {"a": 1},
        {1, 2, 3},

        # 等价类
        [None] * 5,  # 全None列表
        [1] * 10,  # 同值列表
        [1, 2, 3, 4, 5],  # 顺序列表
        [5, 4, 3, 2, 1],  # 逆序列表
        ["", "a", "ab", "abc"],  # 递增长度字符串
        [{"k": i} for i in range(3)],  # 嵌套字典列表
        [CustomClass(1, "a"), CustomClass(2, "b")],  # 对象列表
        [True, False] * 5,  # 交替布尔列表
        [1.1, 2.2, 3.3, 4.4],  # 浮点序列
        [b'bytes', b'more_bytes'],  # 字节列表
        [r'\n', r'\t', r'\r'],  # 转义字符列表
        [0, 1, 0, 1, 0],  # 二进制模式
        [None, "text", 123, 45.67],  # 混合类型

        (), (1, 2), (1, (2, 3)),  # 元组类型
        {}, {"a": 1},  # 简单字典
        {"a": [1, 2], "b": {"c": 3}},  # 嵌套字典
        {1, 2, 3},  # 集合类型

        # 自定义对象
        CustomClass([1, 2], {"a": "b"}),
        CustomClass(None, float('nan')),

        # 大数据结构
        10 ** 100,
        list(range(10000)),
        {i: str(i) for i in range(1000)}
    ]


# 以下代码用于本地测试数据生成
if __name__ == "__main__":
    from pprint import pprint

    test_set = output_test_case()
    print("生成的测试用例数量:", len(test_set))
    print("\n前15个测试样例预览:")
    pprint(test_set[:15])
