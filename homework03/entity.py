class Entity():

    def __init__(self, name, age):
        self.name = name
        self.age = age

    @staticmethod
    def show_class() -> None:
        print(__class__.__name__)

    def show_name(self) -> None:
        print(self.name)


class People(Entity):

    def __init__(self, name, age, is_alive):
        super().__init__(name, age)
        self.is_alive = is_alive

    def show_name(self) -> None:
        print(self.is_alive)


jake = Entity('jake', 19)
jake.show_class()