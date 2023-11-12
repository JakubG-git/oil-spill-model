class Field:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 50

    def __str__(self):
        return f"X: {self.x}, Y: {self.y}"


def create_fields(width, height) -> list[Field]:
    return [Field(x * 50, y * 50) for y in range(height // 50) for x in range(width // 50)]
