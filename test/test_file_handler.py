import pytest
import core.file_handler as fh

def test_setup_config_file():
	fh.setup_config_file(2, [[1, 2], [3, 4]], 1, ['Genoveffa', 'Vercingetorige'])
	good_output = """n = 2;
dist = [|
1,2|
3,4|
];
start_city = 1;
city_names = [Genoveffa,Vercingetorige];"""
	with open(fh.FILE_CONFIG_NAME, 'r') as o:
		output = o.read()
	assert output == good_output
