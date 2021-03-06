from typing import Dict

from pythongame.core.common import *
from pythongame.core.game_state import GameState, Event
from pythongame.core.item_data import get_item_data_by_type
from pythongame.core.item_inventory import ItemWasActivated


class AbstractItemEffect:

    def apply_start_effect(self, game_state: GameState):
        pass

    def apply_middle_effect(self, game_state: GameState, time_passed: Millis):
        pass

    def apply_end_effect(self, game_state: GameState):
        pass

    def item_handle_event(self, event: Event, game_state: GameState):
        pass


class CompositeItemEffect(AbstractItemEffect):
    def __init__(self, effects: List[AbstractItemEffect]):
        self.effects = effects

    def apply_start_effect(self, game_state: GameState):
        for e in self.effects:
            e.apply_start_effect(game_state)

    def apply_middle_effect(self, game_state: GameState, time_passed: Millis):
        for e in self.effects:
            e.apply_middle_effect(game_state, time_passed)

    def apply_end_effect(self, game_state: GameState):
        for e in self.effects:
            e.apply_end_effect(game_state)

    def item_handle_event(self, event: Event, game_state: GameState):
        for e in self.effects:
            e.item_handle_event(event, game_state)

    def __repr__(self):
        return "CompositeItemEffect(%s)" % self.effects


class StatModifyingItemEffect(AbstractItemEffect):
    def __init__(self, stat_modifiers: List[StatModifier]):
        self.stat_modifiers = stat_modifiers

    def apply_start_effect(self, game_state: GameState):
        for modifier in self.stat_modifiers:
            game_state.modify_hero_stat(modifier.hero_stat, modifier.delta)

    def apply_end_effect(self, game_state: GameState):
        for modifier in self.stat_modifiers:
            game_state.modify_hero_stat(modifier.hero_stat, -modifier.delta)

    def __repr__(self):
        return "StatModifyingItemEffect(%s)" % self.stat_modifiers


class EmptyItemEffect(AbstractItemEffect):
    pass


_custom_item_effects: Dict[ItemType, AbstractItemEffect] = {}


def register_custom_item_effect(item_type: ItemType, effect: AbstractItemEffect):
    _custom_item_effects[item_type] = effect


# Note this is handled differently compared to buffs
# There is only one effect instance per item type - having duplicate items with active effects may not be well supported
def create_item_effect(item_id: ItemId) -> AbstractItemEffect:
    effects = []
    if item_id.item_type in _custom_item_effects:
        effects.append(_custom_item_effects[item_id.item_type])
    if item_id.base_stats:
        effects.append(StatModifyingItemEffect(item_id.base_stats))
    if item_id.suffix_id:
        effects.append(StatModifyingItemEffect(item_id.suffix_stats))
    effect = CompositeItemEffect(effects)
    return effect


def try_add_item_to_inventory(game_state: GameState, item_id: ItemId) -> bool:
    item_effect = create_item_effect(item_id)
    item_type = item_id.item_type
    item_equipment_category = get_item_data_by_type(item_type).item_equipment_category
    result = game_state.player_state.item_inventory.try_add_item(item_id, item_effect, item_equipment_category)
    if result:
        if isinstance(result, ItemWasActivated):
            item_effect.apply_start_effect(game_state)
    return result is not None
