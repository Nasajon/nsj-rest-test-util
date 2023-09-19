import re


class AssertUtil:

    @staticmethod
    def assert_status_code(response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Expected status {expected_status_code}, but received {response.status_code}. Return Text: {response.text}."

    @staticmethod
    def assert_is_instance(content, expected_type): 
        assert isinstance(content, expected_type), f"Object is not of type {expected_type}"

    @staticmethod
    def assert_is_dict(content):
        AssertUtil.assert_is_instance(content, dict)

    @staticmethod
    def assert_is_list(content):
        AssertUtil.assert_is_instance(content, list)

    @staticmethod
    def assert_same_type(a, b):
        assert type(a) is type(b), f"Objects are of type {type(a)} and {type(b)}, respectively"

    @staticmethod
    def assert_empty(collection, message = None):
        if not message:
            message = "List is not empty"
        assert len(collection) == 0, message

    @staticmethod
    def assert_dict_has_key(key, content: dict, dict_name: str = ""):
        AssertUtil.assert_is_instance(content, dict)
        assert key in content, f"Key '{key}' is not in dictionary {dict_name}"

    @staticmethod
    def assert_is_equal(a, b, message = None):
        if not message:
            message = f"{a} != {b}"
        assert a == b, message 

    @staticmethod
    def assert_is_not_equal(a, b, message = None):
        if not message:
            message = f"{a} == {b}"
        assert a != b, message 

    @staticmethod
    def assert_greater_than(a, b, message = None):
        if not message:
            message = f"{a} <= {b}"
        assert a > b, message

    @staticmethod
    def assert_less_than(a, b, message = None):
        if not message:
            message = f"{a} >= {b}"
        assert a < b, message
    
    @staticmethod
    def assert_greater_than_or_equal_to(a, b, message = None):
        if not message:
            message = f"{a} < {b}"
        assert a >= b, message

    @staticmethod
    def assert_less_than_or_equal_to(a, b, message = None):
        if not message:
            message = f"{a} > {b}"
        assert a <= b, message

    @staticmethod
    def assert_regex(content, regex):
        assert re.search(regex, content)

    @staticmethod
    def assert_statement(statement, message):
        assert statement, message
