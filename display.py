import time
import framebuf


class QueueItem:

    def __init__(self, item_type: str, data: dict = None, secs_between_frames: float = None):
        self.item_type: str = item_type
        self.data: dict = data
        self.secs_between_frames: float = secs_between_frames


class Display:

    def __init__(self, oled):
        self.oled = oled
        self.queue: list = []
        self.GRID_WIDTH = 8
        self.GRID_HEIGHT = 8

    def queue_item(self, queue_item: QueueItem):
        self.queue.append(queue_item)

    def run(self):
        while True:
            if len(self.queue) < 1:
                time.sleep(0.3)
                continue
            queue_item: QueueItem = self.queue.pop(0)
            if queue_item.item_type == "animation":
                self.display_animation(queue_item)
            elif queue_item.item_type == "clear":
                self.clear_screen()
            elif queue_item.item_type == "image":
                self.display_image(queue_item)

    def clear_screen(self):
        self.oled.fill(0)
        self.oled.show()

    def _show_frame(self, frame):
        frame_buffer = framebuf.FrameBuffer(frame, 128, 64, framebuf.MONO_HMSB)
        self.oled.fill(0)
        self.oled.blit(frame_buffer, 0, 0, 0)
        self.oled.show()

    def display_image(self, queue_item: QueueItem):
        frame = queue_item.data["frame"]
        self._show_frame(frame)

    def display_animation(self, queue_item: QueueItem):
        sequence = queue_item.data["sequence"]
        frames = queue_item.data["frames"]
        delay = queue_item.secs_between_frames

        for index in sequence:
            frame = frames[index]
            self._show_frame(frame)
            time.sleep(delay)  # Display is in a dedicated thread

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

    def render_house(self, queue_item: QueueItem):
        self.oled.fill(0)

        self.oled.rect(63, 0, 64, 64, 1)

        construction: list = queue_item.data["construction"]
        for item in construction:
            passable = item["passable"]
            loc = item["local_location"]
            if not passable:
                if item["material_type"] == "player":
                    self._local_grid_icon_coords(loc[0], loc[1], "X")
                else:
                    self._local_grid_fill_coords(loc[0], loc[1])

        self.oled.show()
