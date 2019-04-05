import time
import itertools

import pyglet

from .logger import KeyLogger
from .builder import PhraseBuilder
from .cpm_display import CPMDisplay
from .phrase_display import PhraseDisplay
from typing_coach.constants import Colours


class KeyRunner(object):

    def __init__(self, phrase):

        self.phrase = phrase
        self.width = 1280
        self.height = 720

        # Window and display
        self.window = pyglet.window.Window(width=self.width, height=self.height, vsync=True)
        self.document = None
        self.layout = None
        self.fps_display = None
        self.cpm_document = None
        self.cpm_layout = None

        # Round variables
        self.logger = None
        self.builder = None
        self.cpm_display = None
        self.phrase_display = None

        # Setup
        self.setup_events()
        self.setup_display()
        self.setup_round()

    # --- SETUP ---

    def setup_events(self):
        self.window.on_draw = self._on_draw
        self.window.on_text = self._on_text
        self.window.on_text_motion = self._on_text_motion

    def setup_display(self):
        self.document = pyglet.text.document.FormattedDocument(self.phrase)
        self.layout = pyglet.text.layout.TextLayout(
            self.document, width=self.window.width - 32, height=(self.window.height*0.66) - 32,
            multiline=True, wrap_lines=True
        )
        self.layout.anchor_y = 'top'
        self.layout.x = 8
        self.layout.y = self.window.height - 16

        self.cpm_document = pyglet.text.document.UnformattedDocument("Test")
        self.cpm_layout = pyglet.text.layout.TextLayout(self.cpm_document, width=500, height=35)
        self.cpm_document.set_style(0, -1, {
            'font_name': 'Times New Roman',
            'font_size': 24,
            'align': 'right',
            'color': Colours.White,
        })
        self.cpm_layout.x = self.window.width - 555
        self.cpm_layout.y = 16

        self.fps_display = pyglet.clock.ClockDisplay()

    def setup_round(self):
        self.logger = KeyLogger()
        self.builder = PhraseBuilder(self.phrase, self.logger)
        self.cpm_display = CPMDisplay(self.logger, self.builder, self.cpm_document)
        self.phrase_display = PhraseDisplay(self.builder, self.document)
        self.logger.addObserver(self.builder)
        self.builder.addObserver(self.cpm_display)
        self.builder.addObserver(self.phrase_display)

    # --- EVENTS ---

    def _on_draw(self):
        self.window.clear()
        self.fps_display.draw()

        pyglet.graphics.draw(
            4, pyglet.gl.GL_QUADS,
            ('v2i', (
                4, self.height - 4,
                4, int(self.height*0.33) + 4,
                self.width - 4, int(self.height*0.33) + 4,
                self.width - 4, self.height - 4)),
            ('c4B', list(itertools.chain.from_iterable(itertools.repeat(Colours.White, 4))))
        )

        pyglet.graphics.draw(
            4, pyglet.gl.GL_QUADS,
            ('v2i', (
                8, self.height - 8,
                8, int(self.height*0.33) + 8,
                self.width - 8, int(self.height*0.33) + 8,
                self.width - 8, self.height - 8)),
            ('c4B', list(itertools.chain.from_iterable(itertools.repeat(Colours.Black, 4))))
        )

        self.layout.draw()
        self.cpm_layout.draw()

    def _on_text(self, text):
        self.logger.log(text)

    def _on_text_motion(self, motion):
        if motion == pyglet.window.key.MOTION_BACKSPACE:
            self.logger.log('\b')
        else:
            self.logger.log(motion)

    def _update(self, dt):
        self.phrase_display.refresh()
        self.cpm_display.refresh()

    # --- ENTRY-POINT ---

    def start(self):
        pyglet.clock.schedule_interval(self._update, 1/120.0)
        pyglet.app.run()

