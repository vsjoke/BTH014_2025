# fuzzing.py
import random
import string
from typing import List, Any


def output_test_case() -> List[Any]:
    """
    生成纯模糊测试数据集（优化版）

    特点：
    - 固定随机种子(42)保证可复现性
    - 扩展数据类型覆盖范围
    - 增加边界条件测试
    - 保持原有代码结构不变
    - 生成12个典型模糊测试用例

    Returns:
        list: 包含12个测试元素的列表，每个元素都是独立生成的测试用例
    """
    random.seed(42)

    def rand_str(length: int = 10) -> str:
        """生成增强型随机字符串（新增特殊字符）"""
        # 在原有基础上增加特殊字符
        chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
        return ''.join(random.choices(chars, k=length))

    def rand_container(depth: int = 1) -> Any:
        """保持原有容器生成逻辑不变"""
        if depth == 0:
            return rand_str()

        container_type = random.choice([
            lambda: [rand_container(depth - 1) for _ in range(random.randint(1, 3))],
            lambda: {rand_str(): rand_container(depth - 1) for _ in range(random.randint(1, 3))},
            lambda: tuple(rand_container(depth - 1) for _ in range(random.randint(1, 3)))
        ])
        return container_type()

    test_cases = []

    # 保持原有循环结构，新增测试用例在原有基础上扩展
    for _ in range(12):  # 增加循环次数到12次
        case_type = random.choice(["basic", "container", "mixed", "empty"])  # 新增empty类型

        if case_type == "basic":
            # 保持原有基础类型，新增None值
            test_cases.append(random.choice([
                random.randint(-1000, 1000),
                random.uniform(-100.0, 100.0),
                rand_str(random.randint(5, 15)),
                random.choice([True, False]),
                None  # 新增None值测试
            ]))

        elif case_type == "container":
            # 保持原有容器生成，增加嵌套深度到3层
            test_cases.append(rand_container(depth=3))

        elif case_type == "mixed":
            # 保持原有混合类型，新增集合类型测试
            test_cases.append(random.choice([
                [rand_str(), random.randint(0, 100), True],
                {"id": rand_str(), "value": random.uniform(0, 1)},
                (rand_str(), random.choice([None, True, False])),
                {rand_str() for _ in range(3)}  # 新增集合类型
            ]))

        elif case_type == "empty":  # 新增空容器测试
            test_cases.append(random.choice([
                [],  # 空列表
                {},  # 空字典
                ()  # 空元组
            ]))

    return test_cases


if __name__ == "__main__":
    sample = output_test_case()[:3]
    print("优化后测试数据样例:")
    for i, item in enumerate(sample, 1):
        print(f"用例{i}: {type(item).__name__}({item})")

# boundary_values.py
def output_test_case():
    """
    使用边界值分析法生成测试数据。
    目标输入范围假设为整数 [1, 100]，可按需调整。

    返回：
        List[List]：每个测试样例作为一个列表，例如：['input_value', '期望行为']
    """
    test_cases = []

    # 边界值
    min_val = 1
    max_val = 100

    # 正常边界值
    test_cases.append([min_val, "Valid lower boundary"])
    test_cases.append([min_val + 1, "Just above lower boundary"])
    test_cases.append([max_val, "Valid upper boundary"])
    test_cases.append([max_val - 1, "Just below upper boundary"])

    # 异常边界值
    test_cases.append([min_val - 1, "Below valid range"])  # 无效值
    test_cases.append([max_val + 1, "Above valid range"])  # 无效值

    # 中间值作为对照
    test_cases.append([(min_val + max_val) // 2, "Typical valid value"])

    return test_cases

if __name__ == "__main__":
    for case in output_test_case():
        print(case)