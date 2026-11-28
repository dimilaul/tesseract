import io
import unittest
from contextlib import redirect_stdout

from tesseract.board_command import BoardCommand
from tesseract.board_controller import BoardController
from tesseract.board_model import BoardModel
from tesseract.board_view import BoardView
from tesseract.event_queue import EventQueue, ModelChangedEvent, ScreenUpdatedEvent
from tesseract.screen_renderer import ScreenRenderer
from tesseract.textual_color import TextualColor
from tesseract.tui.terminal.terminal_screen import TerminalScreenRenderer
from tesseract.tui.virtual_screen_pilot import (
    VirtualScreenPilotController,
    VirtualScreenPilotView,
)
from tesseract.virtual_textual_screen import VirtualTextualScreen


class RecordingRenderer(ScreenRenderer):
    def __init__(self, screen: VirtualTextualScreen):
        super().__init__(screen)
        self.clear_calls = 0
        self.render_calls = 0
        self.snapshots = []

    def clear(self) -> None:
        self.clear_calls += 1

    def render(self) -> None:
        self.render_calls += 1
        snapshot = [
            [self._screen.get_cell(x, y) for x in range(self._screen.get_width())]
            for y in range(self._screen.get_height())
        ]
        self.snapshots.append(snapshot)


class TestTwoEventQueues(unittest.TestCase):
    def test_controller_emits_model_changed_view_renders_screen_emits_screen_updated_renderer_renders(self):
        controller = VirtualScreenPilotController()
        screen = VirtualTextualScreen(3, 3)
        model_queue = controller.get_event_queue()
        screen_queue = screen.get_event_queue()

        recorded_model_events = []
        recorded_screen_events = []
        model_queue.subscribe(recorded_model_events.append)
        screen_queue.subscribe(recorded_screen_events.append)

        renderer = RecordingRenderer(screen)
        view = VirtualScreenPilotView(controller, screen)

        self.assertIs(view.get_event_queue(), model_queue)
        self.assertIs(renderer.get_event_queue(), screen_queue)
        self.assertIsNot(model_queue, screen_queue)

        # Renderer is only aware of screen, not view
        self.assertIs(renderer.get_screen(), screen)
        self.assertFalse(hasattr(renderer, "_board_view"))
        self.assertFalse(hasattr(screen, "_renderer"))

        # Initial render should emit ScreenUpdatedEvent and invoke renderer
        view.render()
        self.assertEqual(len(recorded_model_events), 0)
        self.assertEqual(len(recorded_screen_events), 1)
        self.assertIsInstance(recorded_screen_events[0], ScreenUpdatedEvent)
        self.assertIs(recorded_screen_events[0].screen, screen)
        self.assertEqual(renderer.render_calls, 1)
        self.assertEqual(renderer.snapshots[-1][0][0][0], "0")

        # Controller processes command -> emits ModelChangedEvent -> view renders -> screen emits ScreenUpdatedEvent -> renderer renders
        controller.process_command(BoardCommand.MOVE_RIGHT)
        self.assertEqual(len(recorded_model_events), 1)
        self.assertIsInstance(recorded_model_events[0], ModelChangedEvent)
        self.assertIs(recorded_model_events[0].model, controller.get_board_model())
        self.assertEqual(len(recorded_screen_events), 2)
        self.assertEqual(renderer.render_calls, 2)
        # Head moved from (0, 0) to (1, 0)
        self.assertEqual(renderer.snapshots[-1][0][0][0], " ")
        self.assertEqual(renderer.snapshots[-1][0][1][0], "0")

    def test_nop_and_blocked_move_do_not_emit_model_changed_event(self):
        controller = VirtualScreenPilotController()
        screen = VirtualTextualScreen(3, 3)
        renderer = RecordingRenderer(screen)
        VirtualScreenPilotView(controller, screen)

        controller.process_command(BoardCommand.NOP)
        controller.process_command(BoardCommand.MOVE_UP)
        controller.process_command(BoardCommand.MOVE_LEFT)

        self.assertEqual(renderer.render_calls, 0)

    def test_manual_dispatch_two_event_queues(self):
        controller = VirtualScreenPilotController()
        screen = VirtualTextualScreen(3, 3)
        model_queue = controller.get_event_queue()
        screen_queue = screen.get_event_queue()
        model_queue.set_auto_dispatch(False)
        screen_queue.set_auto_dispatch(False)

        renderer = RecordingRenderer(screen)
        VirtualScreenPilotView(controller, screen)

        controller.process_command(BoardCommand.MOVE_DOWN)
        # Queued in model_queue, not yet dispatched
        self.assertEqual(len(model_queue), 1)
        self.assertEqual(len(screen_queue), 0)
        self.assertEqual(renderer.render_calls, 0)

        # Dispatch model_queue -> view renders to screen and queues ScreenUpdatedEvent
        model_queue.process_events()
        self.assertTrue(model_queue.is_empty())
        self.assertEqual(len(screen_queue), 1)
        self.assertEqual(renderer.render_calls, 0)
        self.assertEqual(screen.get_cell(0, 1)[1], TextualColor.WHITE)

        # Dispatch screen_queue -> renderer renders
        screen_queue.process_events()
        self.assertTrue(screen_queue.is_empty())
        self.assertEqual(renderer.render_calls, 1)
        self.assertEqual(renderer.snapshots[-1][1][0][0], "0")

    def test_terminal_screen_renderer_listens_to_screen_queue(self):
        controller = VirtualScreenPilotController()
        screen = VirtualTextualScreen(3, 3)

        buf = io.StringIO()
        with redirect_stdout(buf):
            renderer = TerminalScreenRenderer(screen)
            VirtualScreenPilotView(controller, screen)
            controller.process_command(BoardCommand.MOVE_RIGHT)

        output = buf.getvalue()
        self.assertIs(renderer.get_screen(), screen)
        self.assertIs(renderer.get_event_queue(), screen.get_event_queue())
        self.assertIn("0", output)

    def test_base_classes_work_with_default_queues(self):
        model = BoardModel(2, 2, 2, 2)
        controller = BoardController(model)
        screen = VirtualTextualScreen(2, 2)
        renderer = RecordingRenderer(screen)
        view = BoardView(controller, screen)

        self.assertIs(view.get_event_queue(), controller.get_event_queue())
        self.assertIs(renderer.get_event_queue(), screen.get_event_queue())
        self.assertIsNot(controller.get_event_queue(), screen.get_event_queue())

        controller.emit_model_changed()
        self.assertEqual(renderer.render_calls, 1)


if __name__ == "__main__":
    unittest.main()
