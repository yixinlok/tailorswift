import os
import shutil

from src.pattern_generation.get_sewing_pattern import generate_pattern_from_yaml

DATA_PATH = "./data/from-image"
OUTPUT_PATH = 'output_patterns'

if __name__ == '__main__':
    if os.path.exists(OUTPUT_PATH):
        shutil.rmtree(OUTPUT_PATH)
    os.makedirs(OUTPUT_PATH)

    all_files = []
    for category in os.listdir(DATA_PATH):
        category_path = os.path.join(DATA_PATH, category)
        if os.path.isdir(category_path):
            all_files.append(os.path.join(category_path, f'{category}.yaml'))
    generate_pattern_from_yaml(all_files, OUTPUT_PATH)
