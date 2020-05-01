import random

from .constants import *

__all__ = ['mass_ship_build_light', 
           'mass_ship_build_heavy', 
           'mass_ship_build_aircraft']


def mass_ship_build(build_list: dict,
                    cuml: list,
                    times: int) -> str:
    '''probabilities is a tuple(list) of four (last one is always 100) integers, 
    corresponding to the official game'''
    resList = []

    for _ in range(times):
        randomed: int = random.randint(1, 100)
        if 1 <= randomed <= cuml[0]:
            resList.append(
                '*SSS* ' + random.choice(build_list.get('super_rare')))
        elif cuml[0] < randomed <= cuml[1]:
            resList.append(
                '*S* ' + random.choice(build_list.get('elite')))
        elif cuml[1] < randomed <= cuml[2]:
            resList.append(
                random.choice(build_list.get('rare')))
        else:
            resList.append(
                random.choice(build_list.get('normal')))
    return '\n'.join(resList)

def mass_ship_build_light(times: int) -> str:
    return mass_ship_build(SHIP_LIST['light'], SHIP_CUML_PROB['light'], times)

def mass_ship_build_heavy(times: int) -> str:
    return mass_ship_build(SHIP_LIST['heavy'], SHIP_CUML_PROB['heavy'], times)

def mass_ship_build_aircraft(times: int) -> str:
    return mass_ship_build(SHIP_LIST['aircraft'], SHIP_CUML_PROB['aircraft'], times)
