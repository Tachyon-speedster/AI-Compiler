from copy import deepcopy


class TiledLoop:
    def __init__(self, iterator, start, end, tile_size, body):
        self.iterator = iterator
        self.start = start
        self.end = end
        self.tile_size = tile_size
        self.body = body

    def __repr__(self):
        return (
            f"TiledLoop(iterator={self.iterator}, start={self.start}, "
            f"end={self.end}, tile_size={self.tile_size}, body={self.body})"
        )


def _can_tile(instr):
    if not isinstance(instr, dict):
        return False
    if instr.get("type") != "for":
        return False
    loop_count = instr.get("iter")
    return isinstance(loop_count, int) and loop_count > 8


def tile_loops(ir, tile_size=4):
    if not isinstance(ir, list):
        return ir

    result = []

    for instr in deepcopy(ir):
        if _can_tile(instr):
            result.append(
                TiledLoop(
                    iterator=instr.get("iterator", "i"),
                    start=0,
                    end=instr.get("iter"),
                    tile_size=tile_size,
                    body=instr.get("body", []),
                )
            )
        else:
            result.append(instr)

    return result


def apply_loop_tiling(ir, tile_size=4):
    return tile_loops(ir, tile_size)


def tile(ir, tile_size=4):
    return tile_loops(ir, tile_size)
