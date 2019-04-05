from typing_coach.util import Observer
from typing_coach.constants import Colours, KeyStates

from .context import StylizedPhraseContext


class PhraseDisplay(Observer):
    """Contains key states, used to build pretty colour text"""

    def __init__(self, builder, document):

        # Style settings for entire phrase
        self.global_style = {
            'font_name': 'Times New Roman',
            'font_size': 24,
            'align': 'center',
            'color': Colours.White,
        }

        # State dependant style settings
        self.style_map = {
            KeyStates.CORRECT: {
                **self.global_style,
                'background_color': Colours.Green,
            },
            KeyStates.INCORRECT: {
                **self.global_style,
                'background_color': Colours.Red,
            },
            KeyStates.CURSOR: {
                **self.global_style,
                'background_color': Colours.Blue,
            },
            KeyStates.NONE: {
                **self.global_style,
                'background_color': Colours.Black,
            },
        }

        self._needs_refresh = True
        self._document = document
        self._context = StylizedPhraseContext(builder, self.style_map)

    def update(self):
        self._needs_refresh = True

    def refresh(self):
        if self._needs_refresh:
            for s in self._context:
                self._document.set_style(**s)
            self._needs_refresh = False
