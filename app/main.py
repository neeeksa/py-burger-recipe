from abc import abstractmethod, ABC


class Validator(ABC):
    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: type) -> object:
        if instance is None:
            return self
        return getattr(instance, self.protected_name, None)

    def __set__(self, instance: object, value: int | str) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: int | str) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int = 0, max_value: int = 3) -> None:
        self.max_value = max_value
        self.min_value = min_value

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if value < self.min_value or value > self.max_value:
            raise (ValueError
                   (f"Quantity should not be less than "
                    f"{self.min_value} and greater than {self.max_value}."))


class OneOf(Validator):
    def __init__(self, options: None = None) -> None:
        if options is None:
            options = "ketchup", "mayo", "burger"
        self.options = options

    def validate(self, value: str) -> None:
        if isinstance(value, str):
            if value not in self.options:
                raise ValueError(f"Expected "
                                 f"{value} to be one of {self.options}.")
        else:
            raise TypeError


class BurgerRecipe:
    buns = Number(min_value=2, max_value=3)
    cheese = Number(min_value=0, max_value=2)
    tomatoes = Number(min_value=0, max_value=3)
    cutlets = Number(min_value=1, max_value=3)
    eggs = Number(min_value=0, max_value=2)
    sauce = OneOf()

    def __init__(self, buns: int, cheese: int,
                 tomatoes: int, cutlets: int, eggs: int, sauce: str) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
