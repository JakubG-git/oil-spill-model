class Field:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 100

    def __str__(self):
        return f"X: {self.x}, Y: {self.y}"


def create_fields(width, height) -> list[Field]:
    return [Field(x * 100, y * 100) for y in range(height // 100) for x in range(width // 100)]
