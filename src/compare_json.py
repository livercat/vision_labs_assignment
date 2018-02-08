import json
from typing import Dict, Any, Union


def load_json(obj: Any) -> Dict[str, Any]:
    if isinstance(obj, str):
        try:
            return json.loads(obj)
        except json.decoder.JSONDecodeError as e:
            print(f'Not a json object: "{obj}"')
            raise e
    return obj


def compare_json(obj1: Union[str, Dict[str, Any]], obj2: Union[str, Dict[str, Any]]) -> bool:
    # Strict comparison, will return False for obj1={'a': [1, 2]} and obj2={'a': [2, 1]}
    return load_json(obj1) == load_json(obj2)


def compare_json_unordered(obj1: Union[str, Dict[str, Any]], obj2: Union[str, Dict[str, Any]]) -> bool:
    # If you don't care about arrays order, and only need to compare containment.
    # https://stackoverflow.com/a/25851972/488470
    return ordered(load_json(obj1)) == ordered(load_json(obj2))


def ordered(obj: Any):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    return obj


if __name__ == '__main__':
    a = {'a': [{'b': [1, 2, 3]}, {'a': [1, 2]}]}
    b = {'a': [{'b': [1, 2, 3]}, {'a': [1, 2]}]}
    print(f'Identical objects, ordered comparison: {compare_json(a, b)}')
    print(f'Identical objects, unordered comparison: {compare_json_unordered(a, b)}\n')

    a = {'a': [{'b': [1, 2, 3]}, {'a': [1, 2]}]}
    b = {'a': [{'b': [1, 3, 2]}, {'a': [2, 1]}]}
    print(f'Shuffled arrays, ordered comparison: {compare_json(a, b)}')
    print(f'Shuffled arrays, unordered comparison: {compare_json_unordered(a, b)}\n')

    a = {'a': [{'b': [1, 2, 3]}, {'a': [1, 2]}]}
    b = {'a': [{'b': [1, 3, 2]}, {'a': [2, 1, 3]}]}
    print(f'Different objects, ordered comparison: {compare_json(a, b)}')
    print(f'Different objects, unordered comparison: {compare_json_unordered(a, b)}\n')

    a = '{"a": [{"b": [1, 2, 3]}, {"a": [1, 2]}]}'
    b = '{"a": [{"b": [1, 2, 3]}, {"a": [1, 2]}]}'
    print(f"Identical strings, ordered comparison: {compare_json(a, b)}")
    print(f"Identical strings, unordered comparison: {compare_json_unordered(a, b)}\n")

    a = '{"a": [{"b": [1, 2, 3]}, {"a": [1, 2]}]}'
    b = '{"a": [{"b": [1, 3, 2]}, {"a": [2, 1]}]}'
    print(f"Shuffled strings, ordered comparison: {compare_json(a, b)}")
    print(f"Shuffled strings, unordered comparison: {compare_json_unordered(a, b)}\n")

    a = '{"a": [{"b": [1, 2, 3]}, {"a": [1, 2]}]}'
    b = '{"a": [{"b": [1, 3, 2]}, {"a": [2, 1, 3]}]}'
    print(f"Different strings, ordered comparison: {compare_json(a, b)}")
    print(f"Different strings, unordered comparison: {compare_json_unordered(a, b)}\n")
