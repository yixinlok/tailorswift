import os
from datetime import datetime
import shutil
from pathlib import Path
import yaml

from garmentcode.assets.garment_programs.meta_garment import MetaGarment
from garmentcode.assets.bodies.body_params import BodyParameters
from garmentcode.pygarment.data_config import Properties

GC_ASSETS_DIR = 'garmentcode/assets'

def generate_pattern_from_yaml(file_paths, output_path):
    """
    Use GarmentCode to generate a sewing pattern for the given YAML files.

    Args:
        file_paths (list): List of paths to YAML files.
        output_path (string): Folder where pattern will be saved.
    """

    bodies_measurements = {
        # Our model
        'neutral': os.path.join(GC_ASSETS_DIR, 'bodies/mean_all.yaml'),
        'mean_female': os.path.join(GC_ASSETS_DIR, 'bodies/mean_female.yaml'),
        'mean_male': os.path.join(GC_ASSETS_DIR, 'bodies/mean_male.yaml'),

        # SMPL
        'f_smpl': os.path.join(GC_ASSETS_DIR, 'bodies/f_smpl_average_A40.yaml'),
        'm_smpl': os.path.join(GC_ASSETS_DIR, 'bodies/m_smpl_average_A40.yaml')
    }
    body_to_use = 'neutral'   # CHANGE HERE to use different set of body measurements

    body = BodyParameters(bodies_measurements[body_to_use])

    designs = []
    for df in file_paths:
        with open(df, 'r', encoding="utf-8", errors="replace") as f:
            designs.append(yaml.safe_load(f)['design'])

    test_garments = [MetaGarment(f'{idx}_garment', body, df) for idx, df in enumerate(designs)]

    for piece in test_garments:
        pattern = piece.assembly()

        if piece.is_self_intersecting():
            print(f'{piece.name} is Self-intersecting')

        # Save as json file
        folder = pattern.serialize(
            Path(output_path), 
            tag='_' + datetime.now().strftime("%y%m%d-%H-%M-%S"), 
            to_subfolder=True, 
            with_3d=False, with_text=False, view_ids=False,
            with_printable=True
        )

        body.save(folder)
        print(f'Success! {piece.name} saved to {folder}')

generate_pattern_from_yaml("../parameters_mapping/new_design.yaml", "out/")
