import csv
import json
import sys
import yaml

def csv_to_json(csv_file, group_columns):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        data = {}
        for row in reader:
            group_data = data
            for col in group_columns[:-1]:
                group_value = row[col]
                if group_value not in group_data:
                    group_data[group_value] = {}
                group_data = group_data[group_value]
            last_group_value = row[group_columns[-1]]
            if last_group_value not in group_data:
                group_data[last_group_value] = []
            group_data[last_group_value].append(row)

    return data

def group_by_columns(csv_file, group_columns):
    json_data = csv_to_json(csv_file, group_columns)
    return json.dumps(json_data, indent=4)

def json_to_yaml(json_data, yaml_file):
    data = json.loads(json_data)

    with open(yaml_file, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

    print(f"YAML file has been saved to {yaml_file}.")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python convertjson.py <csv_file> --groupby <column1,column2,...> --output <output_file>")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'json2yaml':
        if len(sys.argv) != 4:
            print("Usage: python convertjson.py json2yaml <input_file.json> <output_file.yaml>")
            sys.exit(1)

        input_file = sys.argv[2]
        output_file = sys.argv[3]

        with open(input_file, 'r') as file:
            json_data = file.read()

        json_to_yaml(json_data, output_file)
    elif command == 'csv2json':
        if len(sys.argv) < 3:
            print("Usage: python convertjson.py csv2json <csv_file> --groupby <column1,column2,...> --output <output_file>")
            sys.exit(1)

        csv_file = sys.argv[2]

        group_index = sys.argv.index('--groupby') if '--groupby' in sys.argv else -1
        if group_index != -1:
            group_columns = sys.argv[group_index + 1].split(',')
        else:
            group_columns = []

        output_index = sys.argv.index('--output') if '--output' in sys.argv else -1
        if output_index != -1:
            output_file = sys.argv[output_index + 1]
        else:
            output_file = 'output.json'

        json_data = group_by_columns(csv_file, group_columns)

        with open(output_file, 'w') as outfile:
            outfile.write(json_data)

        print(f"JSON data has been saved to {output_file}.")
    else:
        print("Invalid command. Please use 'json2yaml' or 'csv2json'.")

