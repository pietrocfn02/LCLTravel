import pytest
import src.file_handler as fh


def test_setup_config_file():
    fh.setup_config_file(2, [[1, 2], [3, 4]], 1, ['Genoveffa', 'Vercingetorige'])
    good_output = """n = 4;
dist = [|0,50,180,85|50,0,140,70|180,140,0,90|85,70,90,0|];
start_city = 1;
city_names = ["Cosenza","Catanzaro","Vibo","Crotone"];"""
    with open(fh.FILE_CONFIG_NAME, 'r') as o:
        output = o.read()
    assert output == good_output
