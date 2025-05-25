import os
import shutil
import yaml
import numpy as np

DATA_PATH = "data/raw"
OUTPUT_PATH = "data/processed/preprocess_yaml"
SCHEMA = "src/preprocessing/schema.yaml"
DEBUG_LOG = True

def normalize(value, range_vals):
    """
    Normalize the value to a range [0, 1].

    Args:
        value (float): The value to normalize.
        range_vals (tuple): The range to normalize within, e.g., (min, max).

    Returns:
        float: The normalized value.
    """
    min_val, max_val = range_vals
    if max_val - min_val == 0:
        return 0.0
    return (value - min_val) / (max_val - min_val)

def process_categorical(value, range_vals):
    """
    One-hot encode the categorical value based on its range.

    Args:
        value (str): The categorical value.
        range_vals (list): List of possible categorical values.

    Returns:
        list: One-hot encoded vector.
    """
    return [1 if value == val else 0 for val in range_vals]

def vectorize_yaml(yaml_path, schema, log_file=None):
    """
    Parses and vectorizes a YAML file into a flat vector for training.

    Args:
        yaml_path (str): Path to the YAML file.
        schema (dict): The schema defining ranges and types.
        log_file (file): Optional path to log file.

    Returns:
        np.array: A flattened vector representing the YAML data.
    """
    with open(yaml_path, 'r') as f:
        yaml_data = yaml.safe_load(f)

    vectorized_data = {}

    def traverse(data, schema, prefix=""):
        for key, schema_value in schema.items():
            # Create the full key for the schema
            full_key = f"{prefix}_{key}" if prefix else key

            if isinstance(schema_value, dict) and "type" in schema_value:
                if key in data:
                    yaml_value = data[key]

                    # Handle different types based on schema
                    if schema_value["type"] == "float" or schema_value["type"] == "int":
                        # Normalize numerical values
                        vectorized_data[full_key] = normalize(yaml_value["v"], schema_value["range"])
                    elif schema_value["type"] == "select" or schema_value["type"] == "select_null":
                        # One-hot encode categorical values
                        vectorized_data[full_key] = process_categorical(yaml_value["v"], schema_value["range"])
                    elif schema_value["type"] == "bool":
                        # Store boolean values as 1 (True) or 0 (False)
                        vectorized_data[full_key] = 1 if yaml_value["v"] else 0

            elif isinstance(schema_value, dict):
                traverse(data.get(key, {}), schema_value, full_key)

    # Start traversal from the root of both YAML data and schema
    traverse(yaml_data, schema)

    # Convert the dictionary into a flattened vector
    flat_vector = []
    for key in vectorized_data.keys():
        value = vectorized_data[key]
        if log_file:
            log_file.write(f"{key}: {value}\n")
        if isinstance(value, list):
            flat_vector.extend(value)
        else:
            flat_vector.append(value)

    return np.array(flat_vector)

if __name__ == '__main__':
    if os.path.exists(OUTPUT_PATH):
        shutil.rmtree(OUTPUT_PATH)
    os.makedirs(OUTPUT_PATH)

    if DEBUG_LOG:
        DEBUG_PATH = os.path.join(OUTPUT_PATH, "logs")
        os.mkdir(DEBUG_PATH)

    # Load the schema file
    with open(SCHEMA, 'r') as f:
        schema = yaml.safe_load(f)

    # Process files in the data/raw folder
    for category in os.listdir(DATA_PATH):
        category_path = os.path.join(DATA_PATH, category)
        if os.path.isdir(category_path):
            yaml_file = os.path.join(category_path, f"{category}.yaml")

            if os.path.exists(yaml_file):
                print(f"Processing {yaml_file}...")
                if DEBUG_LOG:
                    file_path = os.path.join(DEBUG_PATH, f"{category}_debug.log")
                    with open(file_path, "w") as log_file:
                        vector = vectorize_yaml(yaml_file, schema, log_file)
                else:
                    vector = vectorize_yaml(yaml_file, schema)
                output_file = os.path.join(OUTPUT_PATH, f"{category}_vector")
                np.savetxt(output_file, vector, delimiter="\n")
                print(f"Saved processed data to {output_file}")
            else:
                print(f"No YAML file found for {category} in {category_path}.")
