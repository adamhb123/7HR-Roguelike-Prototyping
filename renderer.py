import curses
from controller import Controller
from engine import Rect, Tile, Map, Event
from entities import Player


class Renderer:
    tile_render_map = {
        Tile.EMPTY.value: " ",  # EMPTY space
        Tile.FILL.value: "█",  # Filled space (rock)
        Tile.ENEMY.value: "e",  # Enemy
        Tile.KEY.value: "+",  # Key
        Tile.GOLD.value: "$",  # Gold
        Tile.PLAYER.value: "P",
    }
    _infoscr_h = 6

    def __init__(self, controller: Controller, map: Map, player: Player):
        # Note: curses coordinate system is (y,x)
        self.stdscr = curses.initscr()
        self._map = map
        self._player = player
        self._controller = controller
        # Below len(str) used for axes labeling spacing
        self.mapscr = curses.newwin(self._map.h+len(str(self._map.h)), self._map.w+1+len(str(self._map.w)), 0, 0)
        self.infoscr = curses.newwin(self._infoscr_h, self._map.w, self._map.h, 0)
        curses.noecho()
        curses.cbreak()
        self.mapscr.keypad(True)

    def render_loop(self):
        while True:
            self.clear()
            self.render()
            key = self.mapscr.getkey()
            print(key)
            print(type(key))
            event, to_tile, from_position, to_position = self._controller.handle_input(key)
            if event != Event.NULL:
                self._map.move_entity(from_position, to_position)
                self._map.handle_event(event, to_tile, to_position)
                self._map.entities_step()
    def clear(self):
        self.mapscr.clear()
        self.infoscr.clear()

    def shutdown(self):
        curses.nocbreak()
        self.mapscr.keypad(False)
        curses.echo()
        curses.endwin()

    def _get_infoscr_text(self):
        return [
            f"HP: {self._player.health}",
            f"Strength: {self._player.strength}",
            f"Keys: {self._player.keys}",
            f"Gold: {self._player.gold}",
        ]

    def render(self):
        # Render map
        for i, y in enumerate(self._map.state):
          line = "".join(map(lambda c: self.tile_render_map[c], y))
          self.mapscr.addstr(i, 0, line)
        texts = self._get_infoscr_text()
        # Divider
        self.infoscr.addstr(0, 0, "-"*self._map.w)
        for i in range(0, len(texts)):
            self.infoscr.addstr(i+1, 0, texts[i])
        self.mapscr.refresh()
        self.infoscr.refresh()

def test_renderer():
    map = Map(72, 15)
    map.generate_rooms(10000,(2,5),(2,5))
    map._place_entity_randomly(Tile.PLAYER)
    player = Player(100, 10)
    controller = Controller(map, player)
    renderer = Renderer(controller, map, player)
    renderer.render_loop()
    

test_renderer()