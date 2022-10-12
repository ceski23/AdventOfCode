from task_1 import Entry, Digit, parse_input
from typing import Any, Dict, Set


segments2digit = {
    frozenset({'a', 'b', 'c', 'e', 'f', 'g'}): 0,
    frozenset({'c', 'f'}): 1,
    frozenset({'a', 'c', 'd', 'e', 'g'}): 2,
    frozenset({'a', 'c', 'd', 'f', 'g'}): 3,
    frozenset({'b', 'c', 'd', 'f'}): 4,
    frozenset({'a', 'b', 'd', 'f', 'g'}): 5,
    frozenset({'a', 'b', 'd', 'e', 'f', 'g'}): 6,
    frozenset({'a', 'c', 'f'}): 7,
    frozenset({'a', 'b', 'c', 'd', 'e', 'f', 'g'}): 8,
    frozenset({'a', 'b', 'c', 'd', 'f', 'g'}): 9,
}


def segments(n: int):
    match n:
        case 0: return {'a', 'b', 'c', 'e', 'f', 'g'}
        case 1: return {'c', 'f'}
        case 2: return {'a', 'c', 'd', 'e', 'g'}
        case 3: return {'a', 'c', 'd', 'f', 'g'}
        case 4: return {'b', 'c', 'd', 'f'}
        case 5: return {'a', 'b', 'd', 'f', 'g'}
        case 6: return {'a', 'b', 'd', 'e', 'f', 'g'}
        case 7: return {'a', 'c', 'f'}
        case 8: return {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
        case 9: return {'a', 'b', 'c', 'd', 'f', 'g'}
        case _: raise Exception('Unknown digit')


class AdvancedEntry(Entry):
    signal_patterns: list[Digit]
    output_signals: list[Digit]
    mappings: Dict[str, Set[str]]

    def __init__(self, signal_patterns: list[Digit], output_signals: list[Digit]) -> None:
        super().__init__(signal_patterns, output_signals)
        self.mappings = dict.fromkeys(
            [chr(x + ord('a')) for x in range(7)],
            set(chr(x + ord('a')) for x in range(7))
        )

    def update_mappings(self, digit: Digit, n: int):
        for segment, mapping in self.mappings.items():
            if segment in segments(n):
                self.mappings[segment] = mapping & set(digit.signals)
            else:
                self.mappings[segment] = mapping - set(digit.signals)

    def find(self, condition: Any):
        return next(x for x in self.signal_patterns if condition(x))

    def decode_mappings(self):
        def is_1(digit: Digit):
            return len(digit.signals) == 2

        def is_7(digit: Digit):
            return len(digit.signals) == 3

        def is_4(digit: Digit):
            return len(digit.signals) == 4

        def is_8(digit: Digit):
            return len(digit.signals) == 7

        def is_9(digit: Digit):
            return len(digit.signals - (digit_4.signals | digit_7.signals)) == 1 and len(digit.signals) == 6

        def is_3(digit: Digit):
            return len(digit.signals - ((digit_9.signals - digit_4.signals) | digit_1.signals)) == 1

        def is_0(digit: Digit):
            return len(digit.signals - (digit_8.signals - (digit_3.signals - (digit_9.signals - digit_4.signals) - digit_1.signals))) == 0 and len(digit.signals) == 6

        def is_2(digit: Digit):
            return len(digit_9.signals - digit.signals) == 2 and len(digit.signals) == 5

        digit_1 = self.find(is_1)
        digit_4 = self.find(is_4)
        digit_7 = self.find(is_7)
        digit_8 = self.find(is_8)
        digit_9 = self.find(is_9)
        digit_3 = self.find(is_3)
        digit_0 = self.find(is_0)
        digit_2 = self.find(is_2)

        self.update_mappings(digit_1, 1)
        self.update_mappings(digit_7, 7)
        self.update_mappings(digit_4, 4)
        self.update_mappings(digit_9, 9)
        self.update_mappings(digit_3, 3)
        self.update_mappings(digit_0, 0)
        self.update_mappings(digit_2, 2)

        return {v.pop(): k for k, v in self.mappings.items()}

    def decode(self):
        reverse_mapping = self.decode_mappings()
        return int(''.join([str(decode_digit(digit, reverse_mapping)) for digit in self.output_signals]))


def decode_digit(digit: Digit, mappings: Dict[str, str]):
    return segments2digit[frozenset(mappings[x] for x in digit.signals)]


if __name__ == "__main__":
    entries = parse_input('input.txt')
    print(sum(AdvancedEntry(e.signal_patterns, e.output_signals).decode()
          for e in entries))
