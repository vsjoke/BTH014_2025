#test.py
import hashlib
import pickle
import equivalence_partitioning
import test_all_if
import boundary_values
import fuzzing
import test_all_uses
import test_all_def


# 返回test_case对应的哈希值，protocol_v:pickle.dumps协议版本，test_case:list
def serialize_test_case_sha256(test_case, protocol_v):
    """
    计算测试用例列表中每个元素的SHA256哈希值并使用pickle进行序列化。

    :param test_case: 要处理的测试用例列表，例如 [a, b, c, ...]
    :param protocol_v: pickle序列化使用的协议版本
    :return: 包含每个元素SHA256哈希的列表
    :raises ValueError: 如果输入类型不符合要求或协议版本无效
    """
    # 验证test_case是否为列表
    if not isinstance(test_case, list):
        raise ValueError("test_case必须是一个列表，例如 [a, b, c, ...]")

    # 验证protocol_v是否为整数
    if not isinstance(protocol_v, int):
        raise ValueError("protocol_v必须是一个整数，表示pickle的协议版本")

    # 获取pickle支持的最高协议版本
    highest_protocol = pickle.HIGHEST_PROTOCOL
    if protocol_v < 0 or protocol_v > highest_protocol:
        raise ValueError(f"protocol_v必须在0到{highest_protocol}之间")

    res = []
    for index, item in enumerate(test_case):
        try:
            # 序列化每个测试用例元素
            test_case_bytes = pickle.dumps(item, protocol=protocol_v)
            # 计算SHA256哈希
            sha256_hash = hashlib.sha256(test_case_bytes).hexdigest()
            res.append(sha256_hash)
        except Exception as e:  # 捕获所有异常
            print(f"Warning: 无法序列化测试用例中的元素 at index {index}, 类型: {type(item)}, 错误: {str(e)}")
            res.append(None)  # 用None表示序列化失败
    return res


def get_hash(a):
    return hashlib.sha256(pickle.dumps(a, protocol=3)).hexdigest()


if __name__ == '__main__':
    # test_case = ["a",["sss","w"],"saww"]
    test_case_sha256_f = []
    p_v = 3
    test_case = equivalence_partitioning.output_test_case()
    test_case_sha256 = serialize_test_case_sha256(test_case, p_v)
    test_case_sha256_f.append(get_hash(test_case_sha256))
    print(f"equivalence_partitioning:{test_case_sha256}")
    print(f"***整体哈希值{get_hash(test_case_sha256)}")
    test_case = test_all_if.output_test_case()
    test_case_sha256 = serialize_test_case_sha256(test_case, p_v)
    test_case_sha256_f.append(get_hash(test_case_sha256))
    print(f"test_all_if:{test_case_sha256}")
    print(f"***整体哈希值{get_hash(test_case_sha256)}")
    test_case = boundary_values.output_test_case()
    test_case_sha256 = serialize_test_case_sha256(test_case, p_v)
    test_case_sha256_f.append(get_hash(test_case_sha256))
    print(f"boundary_values:{test_case_sha256}")
    print(f"***整体哈希值{get_hash(test_case_sha256)}")
    test_case = fuzzing.output_test_case()
    test_case_sha256 = serialize_test_case_sha256(test_case, p_v)
    test_case_sha256_f.append(get_hash(test_case_sha256))
    print(f"fuzzing:{test_case_sha256}")
    print(f"***整体哈希值{get_hash(test_case_sha256)}")
    test_case = test_all_uses.output_test_case()
    test_case_sha256 = serialize_test_case_sha256(test_case, p_v)
    test_case_sha256_f.append(get_hash(test_case_sha256))
    print(f"test_all_uses:{test_case_sha256}")
    print(f"***整体哈希值{get_hash(test_case_sha256)}")
    test_case = test_all_def.output_test_case()
    test_case_sha256 = serialize_test_case_sha256(test_case, p_v)
    test_case_sha256_f.append(get_hash(test_case_sha256))
    print(f"test_all_def:{test_case_sha256}")
    print(f"***整体哈希值{get_hash(test_case_sha256)}")
    print(f"final hash value:{get_hash(test_case_sha256_f)}")  # 输出合成哈希值