from pythongame.core.ability_effects import register_ability_effect
from pythongame.core.buff_effects import AbstractBuffEffect, register_buff_effect, get_buff_effect
from pythongame.core.common import BuffType, Millis, AbilityType
from pythongame.core.game_data import register_ability_data, AbilityData, UiIconSprite, register_ui_icon_sprite_path, \
    register_buff_text
from pythongame.core.game_state import GameState, WorldEntity, NonPlayerCharacter
from pythongame.core.visual_effects import VisualCircle

BUFF_DURATION = Millis(10000)
BUFF_TYPE = BuffType.BLOOD_LUST
LIFE_STEAL_BONUS_RATIO = 0.5


def _apply_ability(game_state: GameState) -> bool:
    game_state.player_state.gain_buff_effect(get_buff_effect(BUFF_TYPE), BUFF_DURATION)
    return True


class BloodLust(AbstractBuffEffect):

    def __init__(self):
        self.time_since_graphics = 0

    def apply_start_effect(self, game_state: GameState, buffed_entity: WorldEntity, buffed_npc: NonPlayerCharacter):
        game_state.player_state.life_steal_ratio += LIFE_STEAL_BONUS_RATIO

    def apply_middle_effect(self, game_state: GameState, buffed_entity: WorldEntity, buffed_npc: NonPlayerCharacter,
                            time_passed: Millis):
        self.time_since_graphics += time_passed
        if self.time_since_graphics > 250:
            self.time_since_graphics = 0
            game_state.visual_effects.append(VisualCircle((250, 0, 0,), buffed_entity.get_center_position(),
                                                      25, 30, Millis(350), 1, buffed_entity))

    def apply_end_effect(self, game_state: GameState, buffed_entity: WorldEntity, buffed_npc: NonPlayerCharacter):
        game_state.player_state.life_steal_ratio -= LIFE_STEAL_BONUS_RATIO

    def get_buff_type(self):
        return BUFF_TYPE


def register_bloodlust_ability():
    ability_type = AbilityType.BLOOD_LUST
    register_ability_effect(ability_type, _apply_ability)
    ui_icon_sprite = UiIconSprite.ABILITY_BLOODLUST
    description = "Grants +" + str(int(LIFE_STEAL_BONUS_RATIO * 100)) + "% lifesteal"
    register_ability_data(
        ability_type,
        AbilityData("Bloodlust", ui_icon_sprite, 30, Millis(30000), description, None))
    register_ui_icon_sprite_path(ui_icon_sprite, "resources/graphics/icon_bloodlust.png")
    register_buff_effect(BUFF_TYPE, BloodLust)
    register_buff_text(BUFF_TYPE, "Bloodlust")