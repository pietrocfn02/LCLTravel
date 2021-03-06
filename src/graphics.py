import json
import re
from enum import Enum, unique
from typing import List

import graphviz as gv
import PySimpleGUI as sg

from src.algorithms import Distance, Player, lcl_travel


@unique
class Vehicle(Enum):
    PANDA = 10000
    TRICICLO = 1
    VESPA = 2
    CENTO_VENTI_CINQUE = 3
    SOTTOMARINO = 4
    QUATTRO_PORTE = 5
    MINIVAN = 9
    AUTOBUS = 20


APP_TITLE = 'LCLTravel'

VEHICLES_AVAILABLE = {
    'Panda 4x4': Vehicle.PANDA,
    'Vespa': Vehicle.VESPA,
    '125cc': Vehicle.CENTO_VENTI_CINQUE,
    'Sottomarino Russo': Vehicle.SOTTOMARINO,
    'Auto 4 porte': Vehicle.QUATTRO_PORTE,
    'Minivan': Vehicle.MINIVAN,
    'Autobus': Vehicle.AUTOBUS
}

REGEX_VALIDATION_NUMBERS = re.compile(r'\D')

VEHICLES = ['Panda 4x4 - 10000 posti', 'Vespa - 2 posti', '125cc - 3 posti (senza casco)', 'Sottomarino Russo - 4 posti', 'Auto 4 porte - 5 posti',
            'Minivan - 9 posti', 'Autobus - 20 posti']
CITIES = []
with open('locations.txt', 'r') as o:
    for line in o:
        CITIES.append(line.strip())

START_CITY: str = CITIES[0]
PEOPLE: int = 1
VEHICLE: Vehicle = VEHICLES[2]
MAXIMUM_KM: int = 10

PLAYERS: List[Player] = []


def validate_input(num_people: str, num_km: str):
    message = ''
    if REGEX_VALIDATION_NUMBERS.search(num_people) != None or len(num_people) > 2:
        message += 'Invalid number of people'
    if REGEX_VALIDATION_NUMBERS.search(num_km) != None or len(num_km) > 10:
        if message != '':
            message += '\n'
        message += 'Invalid input for the maximum km'
    if message != '':
        raise ValueError(message)


def main():
    sg.theme('DarkBlue')

    start_layout = [
        [sg.Text('How many people want to travel?')],
        [sg.InputText(tooltip='Number of people that want to travel',
                      size=(2, 1), default_text=4, key='people')],
        [sg.Text('What type ov vehicle do you want to use?')],
        [sg.InputOptionMenu(VEHICLES, key='vehicle',
                            default_value=VEHICLES[2])],
        [sg.Text('Where do you want to start the tour?')],
        [sg.InputOptionMenu(CITIES, key='start_city',
                            default_value=CITIES[0])],
        [sg.Text('Insert the maximum amount of km do you want to travel')],
        [sg.InputText(tooltip='Maximum km to travel', size=(
            10, 1), default_text=150, key='maximum_km')],
        [sg.Button('Continue')]
    ]

    input_layout = [
        [sg.Text('Insert traveler name:')],
        [sg.InputText(tooltip='Name of the traveler', size=(
            40, 3), default_text='Name', key='name')],
        [sg.Text('Insert how much you\'re willing to pay:')],
        [sg.InputText(tooltip='Maximum ammount willing to pay', size=(
            5, 1), default_text=100, key='maximum_willing_cost')],
        [sg.Text('How many cities do you prefer to visit?')],
        [sg.InputText(tooltip='Number of preferred cities', size=(
            2, 1), default_text=1, key='number_of_cities')],
        [sg.Button('Insert cities')]
    ]

    window = sg.Window(APP_TITLE, start_layout, element_justification='c')

    # Event loop:
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Continue':
            try:
                validate_input(str(values['people']),
                               str(values['maximum_km']))
            except ValueError as error:
                sg.Popup(error, keep_on_top=True)

            PEOPLE = values['people']
            # TODO: trim at `-` and use VEHICLES_AVAILABLE
            VEHICLE = VEHICLES_AVAILABLE[values['vehicle'].partition(' -')[0]]
            START_CITY = values['start_city']
            MAXIMUM_KM = values['maximum_km']

            other_window = sg.Window(
                APP_TITLE, layout=input_layout, element_justification='c')
            window.close()
            window = other_window
        if event == 'Insert cities':
            # Validation
            if re.search(r'[^a-zA-Z\s]', str(values['name'])) != None:
                sg.Popup('Invalid name inserted!', keep_on_top=True)
                continue
            if REGEX_VALIDATION_NUMBERS.search(str(values['number_of_cities'])) != None:
                sg.Popup('Invalid number of cities inserted!', keep_on_top=True)
                continue
            if REGEX_VALIDATION_NUMBERS.search(str(values['maximum_willing_cost'])) != None:
                sg.Popup('Invalid maximum cost inserted!',
                         keep_on_top=True)
                continue
            # Cities insertion layout
            cities_layout = [
                [sg.Text(
                    'Select a city to visit and give it a numeric value representing your preference:')],
            ]
            for i in range(int(values['number_of_cities'])):
                cities_layout.append([sg.InputOptionMenu(CITIES, default_value=CITIES[CITIES.index(START_CITY)], key=f'city_{i}'), sg.InputText(
                    tooltip='Value represinting the preference of this city', size=(6, 1), default_text=1, key=f'pref_city_{i}')])
            cities_layout.append([sg.Button('Submit preferences')])
            # Cities insertion window
            cities_window = sg.Window(
                APP_TITLE, layout=cities_layout, element_justification='c')
            # Cities event loop
            while True:
                cities_event, cities_values = cities_window.read()
                if cities_event == 'Submit preferences':
                    # Validation
                    valid = True
                    for i in range(int(values['number_of_cities'])):
                        if REGEX_VALIDATION_NUMBERS.search(cities_values[f'pref_city_{i}']) != None:
                            valid = False
                    if valid == False:
                        sg.Popup('Invalid input in the city preferences!',
                                 keep_on_top=True)
                        continue
                    # Setting up of the `utility` dictionary
                    preferences: dict = {}
                    for city in CITIES:
                        preferences[city] = 0
                    index = 0

                    for i in range(int(values['number_of_cities'])):
                        preferences[cities_values[f'city_{index}']] = int(
                            cities_values[f'pref_city_{index}'])
                        index += 1

                    player = Player(str(values['name']), preferences, int(
                        values['maximum_willing_cost']))
                    # Add the new `Player` instance in the `PLAYERS` list
                    PLAYERS.append(player)
                    # Check to terminate the insertion of new `Player`
                    if len(PLAYERS) == int(PEOPLE):
                        # Closing all the windows and open the output one
                        cities_window.close()
                        window.close()
                        # Getting by file the list of loations and the list of distances
                        distances: List[Distance] = []
                        with open('distances.json', 'r') as o:
                            data = json.load(o)
                        for city_from, city_to in data.items():
                            for c_t in city_to:
                                distances.append(
                                    Distance(str(city_from), str(c_t), int(data[city_from][c_t])))
                        # Starting all the logic and obtaining the outcome
                        output = lcl_travel(PLAYERS, CITIES, START_CITY,
                                            distances, min(len(PLAYERS), int(VEHICLE.value)), int(MAXIMUM_KM))
                        # Handlign the `NoneType` of `output`
                        if output == None:
                            output_layout = [
                                [sg.Text('Impossible to determine the trip')]]
                        else:
                            # Starting to create the output layout
                            output_layout = [
                                [sg.Text(
                                    'The travelers who\'ll partecipate to the tour are:')],
                            ]
                            # Showing all players partecipating to the tour
                            for agent in output.X:
                                output_layout.append([sg.Text(
                                    f'{agent.name}, who\'ll pay {output.f[agent] + output.p[agent]}???, divided in {output.f[agent]}??? as "fixed costs" and {output.p[agent]}??? as "proportional costs"')])
                            # Populating the output
                            output_layout.append(
                                [sg.Text(f'The social-welfare reached is equal to {output.w}')])
                            output_layout.append([sg.Text(f'The tour will start and end at {START_CITY}')])
                            output_layout.append([sg.Text(f'The textual representation of the tour is: {output.t.tour_itin}')])
                            # Creating an oriented graph to represent the tour
                            graph = gv.Digraph()
                            itinerary = output.t.tour_itin
                            for city in itinerary:
                                graph.node(city, label=city)
                            for i in range(len(itinerary) - 1):
                                graph.edge(
                                    itinerary[i], itinerary[i+1], label=str(data[itinerary[i]][itinerary[i+1]]))

                            graph.render('output_tour_itinerary', format='png')
                            output_layout.append(
                                [sg.Image('output_tour_itinerary.png')])
                        # Switching windows
                        window.close()
                        window = sg.Window(
                            APP_TITLE, layout=output_layout, element_justification='c')
                    break
            cities_window.close()

    window.close()
