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
