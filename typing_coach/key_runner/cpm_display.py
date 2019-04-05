from typing_coach.util import Observer
from typing_coach.constants import Colours, KeyStates


class CPMDisplay(Observer):
    """Contains key states, used to build pretty colour text"""

    def __init__(self, logger, builder, document):

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
        self._logger = logger
        self._builder = builder
        self._document = document

        self._raw_cpm = 0
        self._adjusted_cpm = 0

    def calculate_cpm(self):
        times = self._logger.times
        if times:
            dt = (float((times[-1] - times[0])) or 1)/60
            self._raw_cpm = len(times) / dt
            self._adjusted_cpm = self._builder.good / dt

    def get_output(self):
        return f'Raw CPM = {int(self._raw_cpm)}, Adjusted CPM = {int(self._adjusted_cpm)}'

    def update(self):
        self._needs_refresh = True

    def refresh(self):
        if self._needs_refresh:
            self.calculate_cpm()
            self._document.text = self.get_output()
            self._needs_refresh = False
