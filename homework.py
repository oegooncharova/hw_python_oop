from dataclasses import dataclass
from typing import Union


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories()
                                   )
        return info_message


class Running(Training):
    """Тренировка: бег."""
    RUN_CALORIES_COEFF_1 = 18
    RUN_CALORIES_COEFF_2 = 20
    MIN_IN_HOUR = 60

    def get_spent_calories(self):
        duration_min: float = self.duration * self.MIN_IN_HOUR
        spent_cal_min: float = (
            (self.RUN_CALORIES_COEFF_1
             * self.get_mean_speed()
             - self.RUN_CALORIES_COEFF_2)
            * self.weight / self.M_IN_KM
        )
        spent_calories = spent_cal_min * duration_min
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WALK_CALORIES_COEFF_1 = 0.035
    WALK_CALORIES_COEFF_2 = 0.029
    MIN_IN_HOUR = 60

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        spent_calories = (
            (self.WALK_CALORIES_COEFF_1 * self.weight
             + self.get_mean_speed()**2 // self.height
             * self.WALK_CALORIES_COEFF_2
             * self.weight) * self.duration * self.MIN_IN_HOUR
        )
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SWIM_CALORIES_COEFF_1 = 1.1
    SWIM_CALORIES_COEFF_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        distance_m: float = self.length_pool * self.count_pool
        return distance_m / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.SWIM_CALORIES_COEFF_1)
            * self.SWIM_CALORIES_COEFF_2 * self.weight
        )


def read_package(workout_type: str, data: list) -> Union[Training, str]:
    """Прочитать данные полученные от датчиков."""
    training_types = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        any_training: Training = training_types[workout_type](*data)
    except KeyError:
        return 'Неизвестный тип тренировки'
    except TypeError:
        return 'Неизвестные данные'
    else:
        return any_training


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
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
