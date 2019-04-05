import time

import pyglet
from constants import Colours


class BasicTextViewer(object):
    """Displays basic text using label"""

    def __init__(self):
        self.window = pyglet.window.Window()

        self.label = pyglet.text.Label(
            'Hello World!',
            font_name='Times New Roman',
            font_size=36,
            x=self.window.width//2, y=self.window.height//2,
            anchor_x='center', anchor_y='center',
        )

        self.window.on_draw = self._on_draw

    def _on_draw(self):
        self.window.clear()
        self.label.draw()

    def start(self):
        pyglet.app.run()


class BasicTextWrap(object):
    """Displays basic text using document and layout"""

    def __init__(self):
        self.window = pyglet.window.Window()

        self.document = pyglet.text.decode_text(
            'Hello World!\nHere is some more text to wrap your head around.',
        )
        self.document.set_style(start=0, end=0, attributes=dict(
            font_name='Times New Roman', font_size=36, color=Colours.Blue, align='center')
        )

        self.layout = pyglet.text.layout.TextLayout(
            self.document, width=self.window.width, height=self.window.height,
            multiline=True, wrap_lines=True
        )
        self.layout.content_valign = 'center'

        self.window.on_draw = self._on_draw

    def _on_draw(self):
        self.window.clear()
        self.layout.draw()

    def start(self):
        pyglet.app.run()


# ----------------


class KeyState(object):
    CORRECT = 'CORRECT'
    INCORRECT = 'INCORRECT'
    CURSOR = 'CURSOR'
    INCOMING = 'INCOMING'


class KeyRunnerContext(object):
    def __init__(self, phrase):
        if len(phrase) == 0:
            raise NotImplementedError('RunnerContext can not handle 0-length strings')
        self.phrase = phrase
        self.spans = [KeyState.INCOMING] * len(phrase)
        self.spans[0] = KeyState.CURSOR
        self.index = 0

    def consume(self, key):
        """Consumes the key, modifies span based on comparison, return true if phrase is not complete"""
        if self.index < len(self.phrase):
            if key == '\b' and self.index > 0:
                self.spans[self.index] = KeyState.INCOMING
                self.index -= 1
            else:
                self.spans[self.index] = KeyState.CORRECT if key == self.phrase[self.index] else KeyState.INCORRECT
                self.index += 1
                if self.index < len(self.phrase):
                    self.spans[self.index] = KeyState.CURSOR
            return True
        else:
            return False

    def __iter__(self):
        i = 0
        idx, k = i, self.spans[i]
        while i < len(self.phrase):
            if self.spans[i] != k:
                yield {'start': idx, 'end': i, 'state': k}
                idx, k = i, self.spans[i]
            i += 1
        if i != idx:
            yield {'start': idx, 'end': i, 'state': k}


class KeyRunner(object):

    def __init__(self, phrase):

        # My Thing
        self.phrase = phrase

        # Style settings for entire phrase
        self.global_style = {
            'font_name': 'Times New Roman',
            'font_size': 36,
            'align': 'center',
            'color': Colours.White,
        }

        # State dependant style settings
        self.style_map = {
            KeyState.CORRECT: {
                **self.global_style,
                'background_color': Colours.Green,
            },
            KeyState.INCORRECT: {
                **self.global_style,
                'background_color': Colours.Red,
            },
            KeyState.CURSOR: {
                **self.global_style,
                'background_color': Colours.Blue,
            },
            KeyState.INCOMING: {
                **self.global_style,
                'background_color': Colours.Black,
            },
        }

        self.context = KeyRunnerContext(phrase)

        self.window = pyglet.window.Window()

        self.document = pyglet.text.document.FormattedDocument(phrase)
        self.document.set_style(start=0, end=-1, attributes=self.style_map[KeyState.INCOMING])
        self.apply_context()

        self.layout = pyglet.text.layout.TextLayout(
            self.document, width=self.window.width, height=self.window.height,
            multiline=True, wrap_lines=True
        )
        self.layout.content_valign = 'center'

        self.window.on_draw = self._on_draw

    def _on_draw(self):
        self.window.clear()
        # self.apply_context()
        self.layout.draw()

    def start(self):
        import threading
        t = threading.Thread(target=self.simple_test)
        t.start()
        pyglet.clock.schedule_interval(self.apply_context, 1 / 120.0)
        pyglet.app.run()
        t.join()

    def apply_context(self, *args):
        for s in self.context:
            print(s)
            self.document.set_style(start=s['start'], end=s['end'], attributes=self.style_map[s['state']])
        print('***')

    def simple_test(self):
        for c in self.phrase:
            time.sleep(0.3)
            self.context.consume(c)


def main():
    KeyRunner('Hello World!').start()


if __name__ == '__main__':
    main()
