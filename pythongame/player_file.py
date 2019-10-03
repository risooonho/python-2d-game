import json
from typing import Dict, List


class SavedPlayerState:
    def __init__(self, hero_id: str, level: int, exp: int, consumables_in_slots: Dict[str, List[str]],
                 items: List[str], money: int, enabled_portals: Dict[str, str]):
        self.hero_id = hero_id
        self.level = level
        self.exp = exp
        self.consumables_in_slots = consumables_in_slots
        self.items = items
        self.money = money
        self.enabled_portals = enabled_portals


class PlayerStateJson:
    @staticmethod
    def serialize(player_state: SavedPlayerState):
        return {
            "hero": player_state.hero_id,
            "level": player_state.level,
            "exp": player_state.exp,
            "consumables": player_state.consumables_in_slots,
            "items": player_state.items,
            "money": player_state.money,
            "enabled_portals": player_state.enabled_portals
        }

    @staticmethod
    def deserialize(data) -> SavedPlayerState:
        return SavedPlayerState(
            data["hero"],
            data["level"],
            data["exp"],
            data["consumables"],
            data["items"],
            data["money"],
            data["enabled_portals"]
        )


def load_player_state_from_json_file(file_path: str) -> SavedPlayerState:
    with open(file_path) as file:
        json_data = json.loads(file.read())
        return PlayerStateJson.deserialize(json_data)


def save_player_state_to_json_file(player_state: SavedPlayerState, file_path: str):
    json_data = PlayerStateJson.serialize(player_state)
    with open(file_path, 'w') as file:
        file.write(json.dumps(json_data, indent=2))