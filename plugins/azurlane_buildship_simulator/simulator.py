import random

from .constants import *

__all__ = ['mass_ship_build_light', 
           'mass_ship_build_heavy', 
           'mass_ship_build_aircraft']

DEFAULT_TIMES: int = 10


def mass_ship_build(build_list: dict,
                    *probabilities: int,
                    times:int=DEFAULT_TIMES) -> str:
    '''probabilities is a tuple(list) of four (last one is always 100) integers, 
    corresponding to the official game'''
    resList: list = []

    for _ in range(times):
        randomed: int = random.randint(1, 100)
        if 1 <= randomed <= probabilities[0]:
            resList.append(
                '*SSS* ' + random.choice(build_list.get('super_rare')))
        elif probabilities[0] < randomed <= probabilities[1]:
            resList.append(
                '*S* ' + random.choice(build_list.get('elite')))
        elif probabilities[1] < randomed <= probabilities[2]:
            resList.append(
                random.choice(build_list.get('rare')))
        else:
            resList.append(
                random.choice(build_list.get('normal')))
    return '\n'.join(resList)

def mass_ship_build_light(times:int=DEFAULT_TIMES) -> str:
    return mass_ship_build(LIGHTSHIP_LIST,
                           LIGHTSHIP_SUPERRARE_CUML_PROB,
                           LIGHTSHIP_ELITE_CUML_PROB,
                           LIGHTSHIP_RARE_CUML_PROB,
                           **({'times': times} if times else {}))

def mass_ship_build_heavy(times:int=DEFAULT_TIMES) -> str:
    return mass_ship_build(HEAVYSHIP_LIST,
                           HEAVYSHIP_SUPERRARE_CUML_PROB,
                           HEAVYSHIP_ELITE_CUML_PROB,
                           HEAVYSHIP_RARE_CUML_PROB,
                           **({'times': times} if times else {}))

def mass_ship_build_aircraft(times:int=DEFAULT_TIMES) -> str:
    return mass_ship_build(AIRCRAFT_LIST,
                           AIRCRAFT_SUPERRARE_CUML_PROB,
                           AIRCRAFT_ELITE_CUML_PROB,
                           AIRCRAFT_RARE_CUML_PROB,
                           **({'times': times} if times else {}))
