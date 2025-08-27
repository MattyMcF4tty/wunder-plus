from typing import TypedDict
from .store import read_cache_file, save_cache_file

class MapSettingLayer(TypedDict):
  showBusinessTerritories: bool
  showNoParkingAreas: bool
  showLowSpeedAreas: bool
  showIncentiveAreas: bool
  showVehiclesPins: bool
  showOperatorsPins: bool
  showPointsOfInterestsPins: bool

class MapSettings(TypedDict):
  style: str
  layers: MapSettingLayer
  showTraffic: bool
  vehiclesClusterMaxZoom: int


def write(data: MapSettings): 
  print('Updating map_settings in cache...')

  cache = read_cache_file()

  cache['map_settings'] = data

  save_cache_file(cache)


def read() -> MapSettings | None:
  print("Reading map_settings cache...")

  cache = read_cache_file()
  cached_map_settings = cache.get("map_settings", {})

  if not cached_map_settings:
    print("Found no map_settings in cache")
    return None
  else: 
    print("Found map_settings in cache")
    return cached_map_settings

