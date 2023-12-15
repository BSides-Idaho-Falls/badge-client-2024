import framebuf
import uasyncio as asyncio

from library import atomics


class QueueItem:

    def __init__(self, item_type: str, data: dict = None, ms_between_frames: float = None):
        self.item_type: str = item_type
        self.data: dict = data
        self.ms_between_frames: float = ms_between_frames


class Display:

    def __init__(self, oled):
        self.oled = oled
        self.queue: list = []
        self.GRID_WIDTH = 8
        self.GRID_HEIGHT = 8
        self.queue_frozen = False
        self.cached_render = None

    def queue_item(self, queue_item: QueueItem):
        # if self.queue_frozen:
        #     return
        self.queue.append(queue_item)

    def clear_queue(self, item_type=None):
        if not item_type:
            self.queue = []
            return
        self.queue_frozen = True
        queue = []
        for item in self.queue:
            if item_type != item.item_type:
                queue.append(item)
        self.queue = queue
        self.queue_frozen = False

    async def run(self):
        if len(self.queue) < 1:
            await asyncio.sleep_ms(300)
            return
        queue_item: QueueItem = self.queue.pop(0)
        if queue_item.item_type == "animation":
            await self.display_animation(queue_item)
        elif queue_item.item_type == "clear":
            await self.clear_screen()
        elif queue_item.item_type == "image":
            await self.display_image(queue_item)
        elif queue_item.item_type == "text":
            await self.display_text(queue_item)
        elif queue_item.item_type == "render_house":
            await self.render_house(queue_item)
        await asyncio.sleep_ms(20)

    async def clear_screen(self):
        self.oled.fill(0)
        self.oled.show()

    def _show_frame(self, frame):
        frame_buffer = framebuf.FrameBuffer(frame, 128, 64, framebuf.MONO_HMSB)
        self.oled.fill(0)
        self.oled.blit(frame_buffer, 0, 0, 0)
        self.oled.show()

    async def display_image(self, queue_item: QueueItem):
        frame = queue_item.data["frame"]
        self._show_frame(frame)
        if "delay" in queue_item.data:
            await asyncio.sleep_ms(queue_item.data["delay"])

    async def display_text(self, queue_item: QueueItem):
        i = 0
        message = queue_item.data["message"]
        self.oled.fill(0)
        for item in message:
            self.oled.text(item, 0, i)
            i += 12
        self.oled.show()
        if "delay" in queue_item.data:
            await asyncio.sleep_ms(queue_item.data["delay"])

    async def display_animation(self, queue_item: QueueItem):
        atomics.FREEZE_BUTTONS = True
        sequence = queue_item.data["sequence"]
        frames = queue_item.data["frames"]
        delay = queue_item.ms_between_frames

        for index in sequence:
            frame = frames[index]
            self._show_frame(frame)
            await asyncio.sleep_ms(delay)
        if "delay" in queue_item.data:
            await asyncio.sleep_ms(queue_item.data["delay"])
        atomics.FREEZE_BUTTONS = False

    def _local_grid_start_coords(self, x, y):
        x_shift = 63
        return (x * 8) + x_shift, ((7 - y) * 8)

    def _local_grid_fill_coords(self, x, y):
        x1, y1 = self._local_grid_start_coords(x, y)
        self.oled.fill_rect(x1, y1, self.GRID_WIDTH, self.GRID_HEIGHT, framebuf.MONO_HMSB)

    def _local_grid_icon_coords(self, x, y, icon):
        x1, y1 = self._local_grid_start_coords(x, y)
        if icon == "X":
            self.oled.line(x1, y1, x1 + 8, y1 + 8, 1)
            self.oled.line(x1, y1 + 8, x1 + 8, y1, 1)
        elif icon == "+":
            self.oled.line(x1 + 4, y1, x1 + 4, y1 + 7, 1)
            self.oled.line(x1, y1 + 4, x1 + 7, y1 + 4, 1)

            self.oled.line(x1 + 3, y1, x1 + 3, y1 + 7, 1)
            self.oled.line(x1, y1 + 3, x1 + 7, y1 + 3, 1)
        elif icon == "*":
            self.oled.line(x1, y1, x1 + 7, y1 + 7, 1)
            self.oled.line(x1, y1 + 7, x1 + 7, y1, 1)

            self.oled.line(x1 + 4, y1, x1 + 4, y1 + 7, 1)
            self.oled.line(x1, y1 + 4, x1 + 7, y1 + 4, 1)
        elif icon in ["left", "right", "up", "down"]:
            self.draw_arrow(x1 + 2, y1 + 2, icon)

    def draw_arrow(self, x, y, direction):
        directions = {
            "left": [
                [x + 2, y],
                [x + 1, y + 1],
                [x, y + 2],
                [x + 1, y + 2],
                [x + 2, y + 2],
                [x + 3, y + 2],
                [x + 4, y + 2],
                [x + 1, y + 3],
                [x + 2, y + 4],
            ],
            "right": [
                [x + 2, y],
                [x + 3, y + 1],
                [x, y + 2],
                [x + 1, y + 2],
                [x + 2, y + 2],
                [x + 3, y + 2],
                [x + 4, y + 2],
                [x + 3, y + 3],
                [x + 2, y + 4]
            ],
            "up": [
                [x + 2, y],
                [x + 2, y + 1],
                [x + 2, y + 2],
                [x + 2, y + 3],
                [x + 2, y + 4],
                [x, y + 2],
                [x + 4, y + 2],
                [x + 1, y + 1],
                [x + 3, y + 1]
            ],
            "down": [
                [x + 2, y],
                [x + 2, y + 1],
                [x + 2, y + 2],
                [x + 2, y + 3],
                [x + 2, y + 4],
                [x, y + 2],
                [x + 4, y + 2],
                [x + 1, y + 3],
                [x + 3, y + 3]
            ]
        }
        if direction not in directions:
            return
        coord_set = directions[direction]
        for coord in coord_set:
            self.oled.pixel(coord[0], coord[1], 1)

    async def render_house(self, queue_item: QueueItem = None):
        if not queue_item.data:
            queue_item = self.cached_render
        if not queue_item:
            print("Uh oh, something went wrong rendering.")
            return

        self.cached_render = queue_item
        self.oled.fill(0)

        self.oled.rect(63, 0, 64, 64, 1)

        construction: list = queue_item.data["construction"]
        for item in construction:
            passable = item["passable"]
            loc = item["local_location"]
            abs_loc = item["absolute_location"]
            if abs_loc[0] == 0 and abs_loc[1] == 15:
                self._local_grid_icon_coords(loc[0], loc[1], "*")
                continue
            if not passable:
                if item["material_type"] == "player":
                    self._local_grid_icon_coords(loc[0], loc[1], atomics.GAME_STATE.move_direction)
                else:
                    self._local_grid_fill_coords(loc[0], loc[1])

        player_location = queue_item.data["player_location"]
        x, y = player_location[0], player_location[1]
        x_str = f"0{x}" if x < 10 else str(x)
        y_str = f"0{y}" if y < 10 else str(y)
        self.oled.text(f"{x_str},{y_str}", 0, 0)

        self.oled.show()
