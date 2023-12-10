import sys
from tqdm import tqdm
import requests


BASE_URL = "http://localhost:5000"


def make_insert_request(table, key, key_pairs):
    url = f"{BASE_URL}/insert"
    response = requests.post(
        url, json={
            "key": key,
            "values": key_pairs,
            }
    )
    if response.status_code != 200:
        print(response.text)
        raise ValueError("Error in insert request")


def make_read_request(table, key):
    url = f"{BASE_URL}/get"
    response = requests.post(
        url, json={
            "key": key,
            }
    )
    if response.status_code != 200:
        print(response.text)
        raise ValueError("Error in read request")


def make_update_request(table, key, key_pairs):
    url = f"{BASE_URL}/update"
    response = requests.post(
        url, json={
            "key": key,
            "values": key_pairs,
            }
    )
    if response.status_code != 200:
        print(response.text)
        raise ValueError("Error in update request")


def make_delete_request(table, key):
    url = f"{BASE_URL}/delete"
    response = requests.delete(
        url, json={
            "key": key,
            }
    )
    if response.status_code != 200:
        print(response.text)
        raise ValueError("Error in delete request")


def make_requests(request_data):
    for command, table, key, key_pairs in tqdm(request_data):
        if command == "READ":
            make_read_request(table, key)
        elif command == "INSERT":
            make_insert_request(table, key, key_pairs)
        elif command == "UPDATE":
            make_update_request(table, key, key_pairs)
        elif command == "DELETE":
            make_delete_request(table, key)
        else:
            raise ValueError("Unknown command type")


def parse_serialized_string(serialized_string):
    # Find all occurrences of content between 'field' and the next 'field'
    substr = serialized_string
    pairs = {}
    keys = []
    first_one = True
    while substr.find("field") != -1:
        start = substr.index("field")
        # get value
        if not first_one:
            value = substr[0:start]
        start += len("field")
        # get number between 'field' and '='
        field_num = ""
        while substr[start] != "=":
            field_num += substr[start]
            start += 1
        # get value between '=' and next 'field'
        start += 1
        substr = substr[start:]
        key = "field" + field_num
        keys.append(key)

        if len(keys) > 1:
            pairs[keys[-2]] = value

        first_one = False
    value = substr
    pairs[keys[-1]] = value.strip(']')
    return pairs


def parse_line(line):
    command, table, key, *fields = line.split(" ")
    try:
        if command == "READ":
            key_pairs = None
        elif command == "INSERT":
            key_pairs = parse_serialized_string(" ".join(fields))
        else:
            key_pairs = parse_serialized_string(" ".join(fields))
    except Exception as e:
        import pdb; pdb.set_trace()
        raise e
    return command, table, key, key_pairs


def read_ycsb_output(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    # skip first line as it is path
    # then list of properties starts with *** and ends with ***
    # skip properties
    # the read until lines starts with square bracket
    i = 0
    properties_count = 0
    while i < len(lines):
        if lines[i].startswith("***"):
            properties_count += 1
            if properties_count == 2:
                i += 1
                break
        i += 1

    rows = []
    while i < len(lines):
        if lines[i].startswith("["):
            break
        rows.append(
            parse_line(lines[i].strip())
        )
        i += 1
    return rows


if __name__ == "__main__":
    file_path = sys.argv[1]
    commands = read_ycsb_output(file_path)
    make_requests(commands)
