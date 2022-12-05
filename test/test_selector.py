from ligma_edit import is_selected

# test units
basic_mig = {"type": "MiG-21bis", "name": "RED MiG-21 5"}
road_mig = {"type": "MiG-21bis", "name": "RED_17_ROAD MiG-21 3"}
road_f5 = {"type": "F-5E-3", "name": "BLUE_17_ROAD F-5E 3"}
    
def test_unit_type():
    selector = ".MiG-21bis"
    assert is_selected(selector, basic_mig) == True
    assert is_selected(selector, road_mig) == True
    assert is_selected(selector, road_f5) == False
    
def test_unit_name():
    selector = ".MiG-21bis #ROAD #RED"
    assert is_selected(selector, basic_mig) == False
    assert is_selected(selector, road_mig) == True
    assert is_selected(selector, road_f5) == False
