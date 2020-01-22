class Entity():
  def __init__(self, name, age):
    self.name = name
    self.age = age

  @staticmethod
  def print_class():
    print(__class__.__name__)
  
  def print_name(self):
    print(self.name)

class People(Entity):
  def __init__(self, name, age, legs, hands):
    super().__init__(name, age)
    self.legs = 2
    self.hands = 2

  def show_name(self):
    print(self.is_alive)

Ivan = Entity('Ivan', 43)

Ivan.print_class()
Ivan.print_name()