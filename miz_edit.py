import argparse
import shutil
import os
from zipfile import ZipFile

import luadata as ld

parser = argparse.ArgumentParser(description="Edit loadouts in .miz file")
parser.add_argument("miz", type=str, nargs=1, help="path to .miz file")
parser.add_argument("loadout", type=str, nargs=1, help="path to loadout file")

args = parser.parse_args()
miz_path = args.miz
loadout_path = args.loadout

EXTRACT_PATH = "miz_data"
miz_path = "MOBA_PG_V1.3.1.miz"

def unzip_miz(path):
    print(f"Opening miz file {path}... ", end="")
    with ZipFile(path, 'r') as zip_f:
        zip_f.extractall(EXTRACT_PATH)
    print("Done")

def zip_miz(path, loadout_id):
    # create new miz filename
    new_filename = f"{os.path.basename(path).rsplit('.', 1)[0]}_{loadout_id}.miz"
    new_path = os.path.join(os.path.dirname(path), new_filename)
    
    print(f"Saving new miz to {new_path}... ", end="")
    shutil.make_archive(new_path, "zip", EXTRACT_PATH, ".")
    os.replace(f"{new_path}.zip", new_path)  # remove .zip extension
    print("Done")


if __name__ == "__main__":
    
    if os.path.exists(EXTRACT_PATH):
        shutil.rmtree(EXTRACT_PATH)
    
    # unzip mission
    unzip_miz(miz_path)

    # Read in mission data
    print("Reading mission lua data... ", end="")
    mission = ld.read("miz_data/mission")
    print("Done")

    # Get list of restrictions by type
    # restrictions["MiG-21Bis"] = {...}

    # Apply restrictions to all aircraft by type
    # check coalition
    # exclusions
    # check unit type
    
    for coalition in mission["coalition"]:
        for country in mission["coalition"][coalition]["country"]:
            # helicopters
            if "helicopter" in country:
                for group in country["helicopter"]["group"]:
                    for unit in group["units"]:
                        print(unit["type"])
            # planes
            if "plane" in country:
                for group in country["plane"]["group"]:
                    for unit in group["units"]:
                        print(unit["type"])

    print("Writing modified mission lua data... ", end="")
    ld.write("miz_data/mission", mission, indent="\t", prefix="mission= ")
    print("Done")
    
    # zip file
    zip_miz(miz_path, "test-loadout")

    # clean up miz dir
    shutil.rmtree(EXTRACT_PATH)



