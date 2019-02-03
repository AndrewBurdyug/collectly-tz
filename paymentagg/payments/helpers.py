"""Here are some helper functions."""
import re
import json  # TODO: use ujson

_camel_case_re = re.compile(r'([A-Z])')


def camel_case_to_snake_case(s):
    """Convert camelCase to snake_case.

    :param str s: input string

    """
    return _camel_case_re.sub(r'_\1', s).lower()


def dehydrate_json_data(raw_json_string, input_file=None):
    """Reformat original json field names to expected and return dict.

    :param raw_json_string: input json string
    :param file input_file: input file with json data
    :returns: input json data
    :rtype: dict

    """
    if input_file:
        json_data = json.load(input_file)
    else:
        json_data = json.loads(raw_json_string)
    if isinstance(json_data, dict):
        json_data = [json_data]

    data = {'form-TOTAL_FORMS': len(json_data),
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000'}
    for i, item in enumerate(json_data):
        for key, value in item.items():
            key = camel_case_to_snake_case(key)
            if key == 'patient_id':  # INFO: handle foreign keys
                key = 'patient'
            data['form-{i}-{key}'.format(i=i, key=key)] = value
    return data
