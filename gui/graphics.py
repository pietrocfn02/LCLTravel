from enum import Enum, unique
import re
from time import sleep
import PySimpleGUI as sg


@unique
class Vehicle(Enum):
    PANDA = 10000
    QUATTRO_PORTE = 5
    MINIVAN = 9
    AUTOBUS = 20


vehicle_available = {
    'Panda 4x4': Vehicle.PANDA,
    'Auto 4 porte': Vehicle.QUATTRO_PORTE,
    'Minivan': Vehicle.MINIVAN,
    'Autobus': Vehicle.AUTOBUS
}

REGEX_VALIDATION_NUMBERS = re.compile(r'\D')

sg.theme('DarkBlue')

VEHICLES = ['Panda 4x4 - 10000 posti', 'Auto 4 porte - 5 posti',
            'Minivan - 9 posti', 'Autobus - 20 posti']

layout = [
    [sg.Text('How many people want to travel?')],
    [sg.InputText(tooltip='Number of people that want to travel',
                  size=(2, 1), default_text=4, key='people')],
    [sg.Text('What type ov vehicle do you want to use?')],
    [sg.InputOptionMenu(VEHICLES, key='vehicle', default_value=VEHICLES[1])],
    [sg.Text('Insert the maximum amount of km do you want to travel')],
    [sg.InputText(tooltip='Maximum km to travel', size=(
        10, 1), default_text=150, key='maximum_km')],
    [sg.Button('Continue')]
]

window = sg.Window('LCLTravel', layout, element_justification='c')


def validate_input(num_people: str, num_km: str):
    message = ''
    if REGEX_VALIDATION_NUMBERS.search(num_people) != None or len(num_people) > 2:
        message += 'Invalid number of people'
    if REGEX_VALIDATION_NUMBERS.search(num_km) != None or len(num_km) > 10:
        if message != '':
            message += '\n'
        message += 'Invalid input for the maximum km'
        print('Genoveffa')
    if message != '':
        raise ValueError(message)


# Event loop:
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Continue':
        print('ciao')
        try:
            validate_input(str(values['people']), str(values['maximum_km']))
        except ValueError as error:
            err_layout = [
                [sg.Text(error)],
                [sg.Button('Ok', button_type=sg.BUTTON_TYPE_CLOSES_WIN)]
            ]
            sg.Window('Invalid Input', err_layout,
                      element_justification='c').read()
		# TODO: switch to other input

window.close()