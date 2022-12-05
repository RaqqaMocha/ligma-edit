import argparse
import shutil
import os
from zipfile import ZipFile

import luadata as ld


EXTRACT_PATH = "miz_data"
PLAYER_UNITS = ["plane", "helicopter"]

def is_selected(selector, unit):
    selectors = selector.split(" ")
    
    unit_type = None
    unit_names = []
    
    # parse selector statements
    for sel in selectors: 
        # unit type selector
        if sel.startswith("."):
            unit_type = sel[1:] # only allow one unit type (for now)
            continue
        
        # unit name selector
        if sel.startswith("#"):
            unit_names.append(sel[1:])
            continue
    
    # check unit type
    if unit["type"] != unit_type:
        print("Wrong unit type")
        return False

    # check unit name
    if not all([s in unit["name"] for s in unit_names]):
        print("Wrong unit name")
        return False

    # unit passes all checks and is selected
    return True
            
            
def unzip_miz(path):
    print(f"Opening miz file {path}... ", end="")
    with ZipFile(path, "r") as zip_f:
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


def main(miz_path, loadout_path):
    loadout_id = os.path.basename(loadout_path).split(".")[0]
    if os.path.exists(EXTRACT_PATH):
        shutil.rmtree(EXTRACT_PATH)

    # unzip mission
    unzip_miz(miz_path)

    # Read in mission data
    print("Reading mission lua data... ", end="")
    mission = ld.read("miz_data/mission", encoding="utf-8")
    print("Done")

    print(f"Reading {loadout_id} loadout lua data... ", end="")
    loadout = ld.read(loadout_path, encoding="utf-8")
    print("Done")

    for coalition in mission["coalition"]:
        for country_idx, country in enumerate(mission["coalition"][coalition]["country"]):
            for player_unit in PLAYER_UNITS:      
                if player_unit in country:
                    for group_idx, group in enumerate(country[player_unit]["group"]):
                        for unit_idx, unit in enumerate(group["units"]):
                            if unit["type"] in loadout:
                                if "restricted" in loadout[unit["type"]]:
                                    mission["coalition"][coalition]["country"][country_idx][player_unit]["group"][group_idx]["units"][unit_idx]["payload"]["restricted"] = loadout[unit["type"]]["restricted"]
                                    print(f"Restrictions applied to {unit['type']}")
                                if "Radio" in loadout[unit["type"]]:
                                    mission["coalition"][coalition]["country"][country_idx][player_unit]["group"][group_idx]["units"][unit_idx]["Radio"]= loadout[unit["type"]]["Radio"]
                                    print(f"Radio preset applied to {unit['type']}")

    print("Writing modified mission lua data... ", end="")
    ld.write("miz_data/mission", mission, indent="\t", prefix="mission= ")
    print("Done")

    # zip file
    zip_miz(miz_path, loadout_id)

    # clean up miz dir
    shutil.rmtree(EXTRACT_PATH)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Edit loadouts in .miz file")
    parser.add_argument("miz", type=str, help="path to .miz file")
    parser.add_argument("loadout", type=str, help="path to loadout file")

    args = parser.parse_args()
    miz_path = args.miz
    loadout_path = args.loadout

    main(miz_path, loadout_path)
