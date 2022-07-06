from typing import Union


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str,
                 duration: float, distance: float,
                 speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> Union[str, float]:
        message: Union[str, float] = (f'Тип тренировки: {self.training_type}; '
                                      f'Длительность: {self.duration:.3f} ч.; '
                                      f'Дистанция: {self.distance:.3f} км; '
                                      f'Ср. скорость: '
                                      f'{self.speed:.3f} км/ч; '
                                      f'Потрачено ккал: '
                                      f'{self.calories:.3f}.')
        return message


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MINUTES: int = 60

    def __init__(self, action: int, duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> None:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите get_spent_calories в %s.'
                                  % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def __init__(self, action: int, duration: float, weight: float) -> str:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        H_IN_M: float = (self.duration * self.MINUTES)
        res: float = ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                      - self.COEFF_CALORIE_2)
                      * self.weight / self.M_IN_KM * H_IN_M)
        return res


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: int = 2
    COEFF_CALORIE_3: float = 0.029

    def __init__(self, action: int, duration: float, weight: float,
                 height: float) -> str:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        H_IN_M: float = (self.duration * self.MINUTES)
        res: float = (self.COEFF_CALORIE_1 * self.weight
                      + (self.get_mean_speed()**self.COEFF_CALORIE_2
                         // self.height) * self.COEFF_CALORIE_3
                      * self.weight) * H_IN_M
        return res


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: int = 2

    def __init__(self, action: int, duration: float,
                 weight: float,
                 length_pool: int, count_pool: float) -> str:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        res: float = ((self.get_mean_speed() + self.COEFF_CALORIE_1)
                      * self.COEFF_CALORIE_2 * self.weight)
        return res


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_name: dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in training_name:
        raise ValueError('Тренировка не найдена')
    return training_name[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
