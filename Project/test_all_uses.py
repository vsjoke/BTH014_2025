# test_all_uses.py
import pickle
import hashlib
from collections import defaultdict


class CustomClass:
    """用于测试对象属性被不同方式使用的类"""

    def __init__(self):
        self.primary = 42  # 基础属性定义
        self.secondary = None  # 延迟初始化属性
        self._init_complex_attr()  # 方法调用初始化

    def _init_complex_attr(self):
        """测试方法调用触发的属性使用"""
        self.complex_attr = defaultdict(list)
        self.complex_attr["usage1"].append("defined")

    def __reduce__(self):
        return (self.__class__, ())


def output_test_case() -> list:
    """生成覆盖变量不同使用场景的测试数据集"""
    obj = CustomClass()
    obj.secondary = [obj.primary]  # 测试属性值的二次使用

    return [
        # 基础使用场景
        ("direct_use", 42),
        ("reassigned_use", [obj.primary, obj.secondary]),

        # 容器嵌套使用
        {"container_use": {
            "nested": [obj.complex_attr, {"key": obj.primary}],
            "copied": obj.complex_attr.copy()
        }},

        # 修改后使用
        (lambda: setattr(obj, 'dynamic_attr', 3.14))(),  # 动态属性
        (obj.complex_attr["usage1"].append("used"), obj)  # 修改后使用

    ]


def validate_uses(test_case, protocol_v):
    """验证对象使用路径是否被完整保留"""
    try:
        # 序列化/反序列化过程
        serialized = pickle.dumps(test_case, protocol=protocol_v)
        deserialized = pickle.loads(serialized)

        # 使用场景验证逻辑
        if isinstance(test_case, CustomClass):
            # 验证属性初始化路径
            assert hasattr(deserialized, 'complex_attr'), "属性初始化路径丢失"
            assert deserialized.complex_attr["usage1"] == ["defined", "used"], "修改后使用路径丢失"

        # 更多使用场景验证...
        return True
    except Exception as e:
        print(f"Use-case violation: {str(e)}")
        return False


def run_uses_tests(protocol_v=3):
    """执行uses覆盖测试"""
    test_cases = output_test_case()
    results = []

    for idx, case in enumerate(test_cases):
        valid = validate_uses(case, protocol_v)
        # 计算哈希确保稳定性
        case_hash = hashlib.sha256(pickle.dumps(case, protocol_v)).hexdigest()
        results.append((f"Case_{idx + 1}", valid, case_hash))

    return results


if __name__ == "__main__":
    # 执行测试并输出结果
    results = run_uses_tests()
    print("\nUSES覆盖测试结果：")
    for name, status, hash_val in results:
        print(f"{name}: {'通过' if status else '失败'} | 哈希值：{hash_val[:8]}...")

    # 集成到主测试框架
    print("\n测试数据集示例：")
    print(output_test_case()[:2])