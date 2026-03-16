class Assign:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class AddAssign:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class ForLoop:
    def __init__(self, var, limit, body):
        self.var = var
        self.limit = limit
        self.body = body


class Print:
    def __init__(self, value):
        self.value = value

class VectorAdd:
    def _init_(self, dest, a, b, size):
        self.dest = dest
        self.a = a
        self.b = b
        self.size = size

class VectorScale:
    def _init_(self, arr, factor, size):
        self.arr = arr
        self.factor = factor
        self.size = size

class VectorAdd:
    def __init__(self, a, b, dest, size):
        self.a = a
        self.b = b
        self.dest = dest
        self.size = size


class VectorMul:
    def __init__(self, a, b, dest, size):
        self.a = a
        self.b = b
        self.dest = dest
        self.size = size

class TiledLoop:

    def __init__(self, outer_var, inner_var, limit, tile_size, body):

        self.outer_var = outer_var
        self.inner_var = inner_var
        self.limit = limit
        self.tile_size = tile_size
        self.body = body

