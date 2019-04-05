class PhraseContext(object):
    def __init__(self, builder):
        self._builder = builder

    def _iter_inner(self, k, start, end):
        for i in range(start + 1, end):
            if self._builder.states[i] != k:
                return i
        return end

    def __iter__(self):
        """Traverse the keys, yielding spans"""
        start, end = 0, len(self._builder.phrase)
        while start < end:
            k = self._builder.states[start]
            m = self._iter_inner(k, start, end)
            yield {'start': start, 'end': m, 'state': k}
            start = m


class StylizedPhraseContext(object):
    def __init__(self, builder, style_map):
        self._context = PhraseContext(builder)
        self._style_map = style_map

    def __iter__(self):
        """Converts spans into stylized spans"""
        for r in self._context:
            r['attributes'] = self._style_map[r.pop('state')]
            yield r
