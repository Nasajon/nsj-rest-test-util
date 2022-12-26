from enum import Enum


class EnumCustom(Enum):
    def __eq__(self, other):
        valor1 = self.value
        valor2 = other
        if isinstance(other, Enum):
            valor2 = other.value
        return valor1 == valor2

    def __hash__(self):
        return super.__hash__(self)
