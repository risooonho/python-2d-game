from typing import Optional, Callable

from pythongame.core.common import HeroId, Millis, AbstractScene, SceneTransition
from pythongame.player_file import SaveFileHandler
from pythongame.scene_creating_world.scene_creating_world import InitFlags


class CommandlineFlags:
    def __init__(self, map_file_name: Optional[str], picked_hero: Optional[HeroId],
                 hero_start_level: int, start_money: int):
        self.map_file_name = map_file_name
        self.chosen_hero_id = picked_hero
        self.hero_start_level = hero_start_level
        self.start_money = start_money

    def __repr__(self):
        return "(" + str(self.map_file_name) + ", " + str(self.chosen_hero_id) + ", " + \
               str(self.hero_start_level) + ", " + str(self.start_money) + ")"


class StartingProgramScene(AbstractScene):
    def __init__(self,
                 main_menu_scene: Callable[[InitFlags], AbstractScene],
                 creating_world_scene: Callable[[InitFlags], AbstractScene],
                 picking_hero_scene: Callable[[InitFlags], AbstractScene],
                 cmd_flags: CommandlineFlags, save_file_handler: SaveFileHandler):

        self.main_menu_scene = main_menu_scene
        self.creating_world_scene = creating_world_scene
        self.picking_hero_scene = picking_hero_scene
        self.cmd_flags = cmd_flags
        self.save_file_handler = save_file_handler

    def run_one_frame(self, _time_passed: Millis) -> Optional[SceneTransition]:

        map_file_name = self.cmd_flags.map_file_name or "map1.json"
        map_file_path = "resources/maps/" + map_file_name

        start_immediately_and_skip_hero_selection = (
                self.cmd_flags.chosen_hero_id is not None
                or self.cmd_flags.hero_start_level is not None
                or self.cmd_flags.start_money is not None)
        if start_immediately_and_skip_hero_selection:
            if self.cmd_flags.chosen_hero_id:
                picked_hero = HeroId[self.cmd_flags.chosen_hero_id]
            else:
                picked_hero = HeroId.MAGE
            hero_start_level = int(self.cmd_flags.hero_start_level) if self.cmd_flags.hero_start_level else 1
            start_money = int(self.cmd_flags.start_money) if self.cmd_flags.start_money else 0

            flags = InitFlags(
                map_file_path=map_file_path,
                picked_hero=picked_hero,
                saved_player_state=None,
                hero_start_level=hero_start_level,
                start_money=start_money,
                character_file=None)
            return SceneTransition(self.creating_world_scene(flags))

        else:
            flags = InitFlags(
                map_file_path=map_file_path,
                picked_hero=None,
                saved_player_state=None,
                hero_start_level=1,
                start_money=0,
                character_file=None)
            return SceneTransition(self.main_menu_scene(flags))
