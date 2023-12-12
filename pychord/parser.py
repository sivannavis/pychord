from typing import Tuple, List
import re

from .quality import QualityManager, Quality
from .constants.scales import NOTE_VAL_DICT, RELATIVE_KEY_DICT, FLATTED_SCALE


inversion_re = re.compile("/([0-9]+)")


def parse(chord: str) -> Tuple[str, Quality, List[str], str]:
    """Parse a string to get chord component

    :param chord: str expression of a chord
    :return: (root, quality, appended, on)
    """
    if len(chord) > 1 and chord[1] in ("b", "#"):
        root = chord[:2]
        rest = chord[2:]
    else:
        root = chord[:1]
        rest = chord[1:]

    def check_note(note: str):
        """ Raise ValueError if note is invalid """
        if note not in NOTE_VAL_DICT:
            raise ValueError(f"Invalid note {note}")

    check_note(root)

    inversion = 0
    inversion_m = inversion_re.search(rest)
    if inversion_m:
        inversion = int(inversion_m.group(1))
        rest = inversion_re.sub("", rest)

    on_chord_idx = rest.find("/")
    if on_chord_idx >= 0:
        on = rest[on_chord_idx + 1:]
        rest = rest[:on_chord_idx]
        # change bass from number to note
        if bool(re.search(r'\d', on)):
            on_val = int(re.search(r'\d', on).group())
            on_val = RELATIVE_KEY_DICT['maj'][on_val-1]
            if 'b' in on:
                on_val -= 1
            elif '#' in on:
                on_val += 1
            bass_val = (NOTE_VAL_DICT[root] + on_val) % 12
            on = FLATTED_SCALE[bass_val]
        check_note(on)
    else:
        on = ""
    quality = QualityManager().get_quality(rest, inversion)
    # TODO: Implement parser for appended notes
    appended: List[str] = []
    return root, quality, appended, on
