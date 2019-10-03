from pythongame.core.common import ConsumableType, Sprite, UiIconSprite
from pythongame.core.consumable_effects import create_potion_visual_effect_at_player, ConsumableWasConsumed, \
    ConsumableFailedToBeConsumed, register_consumable_effect
from pythongame.core.damage_interactions import player_receive_mana
from pythongame.core.game_data import POTION_ENTITY_SIZE, ConsumableCategory
from pythongame.core.game_data import register_ui_icon_sprite_path, register_entity_sprite_initializer, \
    SpriteInitializer, register_consumable_data, ConsumableData
from pythongame.core.game_state import GameState

MANA_AMOUNT = 50


def _apply_mana(game_state: GameState):
    if not game_state.player_state.mana_resource.is_at_max():
        create_potion_visual_effect_at_player(game_state)
        player_receive_mana(MANA_AMOUNT, game_state)
        return ConsumableWasConsumed()
    else:
        return ConsumableFailedToBeConsumed("Already at full mana!")


def register_lesser_mana_potion():
    consumable_type = ConsumableType.MANA_LESSER
    sprite = Sprite.POTION_MANA_LESSER
    ui_icon_sprite = UiIconSprite.POTION_MANA_LESSER

    register_consumable_effect(consumable_type, _apply_mana)
    image_path = "resources/graphics/icon_potion_lesser_mana.png"
    register_entity_sprite_initializer(sprite, SpriteInitializer(image_path, POTION_ENTITY_SIZE))
    register_ui_icon_sprite_path(ui_icon_sprite, image_path)
    data = ConsumableData(ui_icon_sprite, sprite, "Lesser mana potion", "Restores " + str(MANA_AMOUNT) + " mana",
                          ConsumableCategory.MANA)
    register_consumable_data(consumable_type, data)