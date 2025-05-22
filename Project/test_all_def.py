#test_all_def.py
import pickle

class CustomClassExample:
    def __init__(self):
        self.data = "example"
        self.counter = 0
        self.metadata = {"created": "now"}

    def __getstate__(self):
        return self.__dict__

    def __eq__(self, other):
        # 确保两个对象的所有属性都相同
        return self.__class__ == other.__class__ and self.__dict__ == other.__dict__

    def check_all_defs(self, other):
        """检查两个对象的所有定义是否一致"""
        for attr in self.__dict__.keys():
            if not hasattr(other, attr) or getattr(other, attr) != getattr(self, attr):
                return False, attr
        return True, None


def output_test_case():
    """
    提供一组用于测试的数据集。
    返回值是一个 list，包含多种类型嵌套的数据结构。
    """
    return [
        'a',
        123,
        True,
        None,
        ["nested", ["inner_list"]],
        {"outer": {"inner": "value"}},
        (1, 2, 3),
        frozenset([1, 2, 3]),
        [{"key": "value"}, [1, 2, 3]],
        CustomClassExample(),
        ["混合类型", 42, {"a": [1, 2]}, ("tuple_in_list",)],
        b"byte_string",
        bytearray(b"bytearray_example"),
        complex(1, 2),
        set([1, 2, 3]),
        Exception("test exception"),
    ]


def run_tests(test_cases, protocol_v):
    results = []
    for i, case in enumerate(test_cases):
        test_id = i + 1
        try:
            serialized = pickle.dumps(case, protocol=protocol_v)
            deserialized = pickle.loads(serialized)

            # 对于自定义类实例，使用特定的检查方法
            if isinstance(case, CustomClassExample):
                success, missing_attr = case.check_all_defs(deserialized)
                msg = "" if success else f"Attribute {missing_attr} failed to be correctly restored"
            else:
                # 使用深度比较来确保结构和值完全一致
                success = (deserialized == case) if not isinstance(case, CustomClassExample) else (deserialized.data == case.data)
                msg = "Value mismatch after deserialization" if not success else ""

            results.append((test_id, success, msg))
        except Exception as e:
            results.append((test_id, False, str(e)))
    return results


if __name__ == "__main__":
    test_cases = output_test_case()
    print(f"Total test cases: {len(test_cases)}")
    results = run_tests(test_cases, protocol_v=pickle.HIGHEST_PROTOCOL)

    print("\nTest Results:")
    passed_count = 0
    for tid, status, msg in results:
        if status:
            passed_count += 1
        print(f"Test {tid}: {'Passed' if status else 'Failed'} - {msg}")

    print(f"\nSummary: {passed_count}/{len(results)} tests passed.")