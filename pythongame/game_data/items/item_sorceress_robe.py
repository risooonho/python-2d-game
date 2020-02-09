from pythongame.core.common import ItemType, Sprite, UiIconSprite, HeroStat
from pythongame.core.item_inventory import ItemEquipmentCategory
from pythongame.game_data.items.register_items_util import register_randomized_stat_modifying_item


def register_sorceress_robe_item():
    register_randomized_stat_modifying_item(
        item_type=ItemType.SORCERESS_ROBE,
        item_level=7,
        ui_icon_sprite=UiIconSprite.ITEM_SORCERESS_ROBE,
        sprite=Sprite.ITEM_SORCERESS_ROBE,
        image_file_path="resources/graphics/item_sorceress_robe.png",
        item_equipment_category=ItemEquipmentCategory.CHEST,
        name="Sorceress' Robe",
        stat_modifier_intervals={HeroStat.ARMOR: [1], HeroStat.MAX_MANA: [8, 9, 10],
                                 HeroStat.MAGIC_DAMAGE: [0.13, 0.14, 0.15]}
    )
