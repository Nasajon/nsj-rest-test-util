from typing import Tuple, Union

from nsj_rest_test_util.util.assert_util import AssertUtil
from nsj_rest_test_util.util.dump_util import DumpUtil


class ValidateUtil():

    @staticmethod
    def compare_content(a, b, diff_path: str = None) -> Tuple[bool, Union[dict, list, None]]:

        if not type(b) is type(a):
            return True, None

        has_diff = False
        diff = {}

        if isinstance(a, dict):
            diff = ValidateUtil.compare_dict(a, b)
            has_diff = diff != {}

        elif isinstance(a, list):
            diff = ValidateUtil.compare_list(a, b)
            has_diff = len(diff) != 0

        elif a != b:
            has_diff = True

        if has_diff and diff_path:
            DumpUtil.write_json(diff_path, diff)

        return has_diff, diff

    @staticmethod
    def compare_dict(dict_a: dict, dict_b: dict) -> dict:

        diff = {}

        for key, val_a in dict_a.items():

            if key not in dict_b:
                diff[key] = "Missing property"
                continue

            val_b = dict_b[key]

            if not type(val_b) is type(val_a):
                diff[key] = f"Incorrect type: {type(val_a)} != {type(val_b)}"
                continue

            val_diff = {}
            if isinstance(val_a, dict):
                val_diff = ValidateUtil.compare_dict(val_a, val_b)

            elif isinstance(val_a, list):
                val_diff = ValidateUtil.compare_list(val_a, val_b)

            elif val_a != val_b:
                val_diff = f"Different value -> {val_a} != {val_b}"

            if val_diff:
                diff[key] = val_diff

        return diff

    @staticmethod
    def compare_list(list_a: list, list_b: list) -> list:

        if len(list_a) > len(list_b):
            return "Different lenght"

        diff = []

        for i, (val_a, val_b) in enumerate(zip(list_a, list_b)):

            if not type(val_b) is type(val_a):
                diff.append(f"Incorrect type {type(val_a)} != {type(val_b)}")
                continue

            val_diff = {}
            if isinstance(val_a, dict):
                val_diff = ValidateUtil.compare_dict(val_a, val_b)

            elif isinstance(val_a, list):
                val_diff = ValidateUtil.compare_list(val_a, val_b)

            elif val_a != val_b:
                val_diff = f"Different value at {i} -> {val_a} != {val_b}"

            if val_diff:
                val_diff["index"] = i
                diff.append(val_diff)

        return diff

    # -----------------------------------------------------------   
    @staticmethod
    def assert_content(esperado, real, root="json"):
        AssertUtil.assert_same_type(esperado, real)

        failures = []
        if isinstance(real, dict):
            failures = ValidateUtil.assert_dict(esperado, real, trace=root)
        elif isinstance(real, list):
            failures = ValidateUtil.assert_list(esperado, real, trace=root)
        else:
            if real != esperado:
                failures = [f"\n\t{root}:  real [{real}]  != esperado [{esperado}]"]

        AssertUtil.assert_statement(len(failures) == 0, "\n".join([f"{fail}" for fail in failures]))

    @staticmethod
    def assert_dict(esperado: dict, real: dict, trace: str = ""):

        failures = []
        for key, val_a in esperado.items():

            trace_key = f"{trace} -> {key}"

            if key not in real:
                failures.append(f"\n\t{trace_key} is not in dictionary")
                continue

            val_b = real[key]

            if not type(val_a) is type(val_b):
                failures.append(f"\n\t{trace_key}: Incorrect type: {type(val_a)} != {type(val_b)}")
                continue

            key_failures = []

            if isinstance(val_a, dict):
                key_failures = ValidateUtil.assert_dict(val_a, val_b, trace_key)

            elif isinstance(val_b, list):
                key_failures = ValidateUtil.assert_list(val_a, val_b, trace_key)

            else:
                if (val_a != val_b) and (key != 'tenant'):
                    key_failures = [f"\n\t{trace_key}:  {val_a} != {val_b}"]

            if key_failures:
                failures.extend(key_failures)

        return failures

    @staticmethod
    def assert_list(esperado: list, real: list, trace: str = ""):

        if len(esperado) != len(real):
            return [f"\n\t{trace}: Lists do not have same length: Real [{len(real)}] != Esperado [{len(esperado)}]"]

        failures = []

        for i, (val_a, val_b) in enumerate(zip(esperado, real)):

            trace_index = f"{trace}[{i}]"

            index_failures = None

            if isinstance(val_a, dict):
                index_failures = ValidateUtil.assert_dict(val_a, val_b, trace_index)

            elif isinstance(val_b, list):
                index_failures = ValidateUtil.assert_list(val_a, val_b, trace_index)

            else:
                if val_a != val_b:
                    index_failures = [f"\n\t{trace_index}:  {val_a} != {val_b}"]

            if index_failures:
                failures.extend(index_failures)

        return failures
