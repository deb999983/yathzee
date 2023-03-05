from functools import cached_property


class Dice:
    FACES = {
        1: (
            "┌─────────┐",
            "│         │",
            "│    ●    │",
            "│         │",
            "└─────────┘",
        ),
        2: (
            "┌─────────┐",
            "│  ●      │",
            "│         │",
            "│      ●  │",
            "└─────────┘",
        ),
        3: (
            "┌─────────┐",
            "│  ●      │",
            "│    ●    │",
            "│      ●  │",
            "└─────────┘",
        ),
        4: (
            "┌─────────┐",
            "│  ●   ●  │",
            "│         │",
            "│  ●   ●  │",
            "└─────────┘",
        ),
        5: (
            "┌─────────┐",
            "│  ●   ●  │",
            "│    ●    │",
            "│  ●   ●  │",
            "└─────────┘",
        ),
        6: (
            "┌─────────┐",
            "│  ●   ●  │",
            "│  ●   ●  │",
            "│  ●   ●  │",
            "└─────────┘",
        ),
    }
    def __init__(
            self, dice_rolls: list[int], name = "", include_id_header=False
    ) -> None:
        self.WIDTH = len(self.FACES[1][0])
        self.HEIGHT = len(self.FACES[1])
        self.SEPARATOR = " "
        
        self.dice_rolls = dice_rolls
        self.name = name
        self.include_id_header = include_id_header

        l = len(dice_rolls)
        self.totalWidth = max(len(name), self.WIDTH * l + l - 1)
    
    def get_header(self):
        dice_rolls = self.dice_rolls
        L = len(dice_rolls)

        header = ["~"*self.totalWidth]
        if self.include_id_header:
            id_str = ''
            for index in range(L):
                id_str += f"{index + 1}".center(self.WIDTH) + self.SEPARATOR
            header.append(id_str.center(self.totalWidth))
            header.append("~"*self.totalWidth)
        return header

    def get_body(self):
        dice_rolls = self.dice_rolls
        body = []
        for r in range(self.HEIGHT):
            face_row = []
            for roll in dice_rolls:
                face = self.FACES[roll]
                face_row.append(face[r])
            body.append(self.SEPARATOR.join(face_row).center(self.totalWidth))
        return body

    @cached_property
    def data(self):
        return [
            *self.get_header(),
            *self.get_body()
        ]
