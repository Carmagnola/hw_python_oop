class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration, distance, speed, calories) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return 'Тип тренировки: %s; ' \
               'Длительность: %.3f ч.; ' \
               'Дистанция: %.3f км; ' \
               'Ср. скорость: %.3f км/ч; ' \
               'Потрачено ккал: %.3f.' % (
                   self.training_type, self.duration, self.distance, self.speed, self.calories)

        pass


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60
    # минут в часе
    S_IN_H = 3600

    # секунд в часе

    # рост в метрах

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.duration = duration
        self.weight = weight
        self.action = action

        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance
        pass

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed
        pass

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration, self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())
        pass


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        # ((CALORIES_MEAN_SPEED_MULTIPLIER * средняя_скорость + CALORIES_MEAN_SPEED_SHIFT)
        #  * вес_спортсмена / M_IN_KM * время тренировки_в_минутах)
        duration = self.duration * self.MIN_IN_H
        spent_calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                          * self.weight / self.M_IN_KM * duration)
        return spent_calories

    pass


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    def __init__(self, action: int, duration: float, weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        # ((0.035 * вес + (средняя_скорость_в_метрах_в_секунду**2 / рост_в_метрах)
        #  * 0.029 * вес) * время_тренировки_в_минутах)
        height = self.height / self.CM_IN_M  # +
        duration = self.duration * self.MIN_IN_H  # +
        speed = self.get_mean_speed() * self.KMH_IN_MSEC  # метры в сек
        spent_calories = (self.CALORIES_WEIGHT_MULTIPLIER * self.weight + (
            (speed ** 2 / height) * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)) * duration
        return spent_calories

    pass


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2

    def __init__(self, action: int, duration: float, weight: float, length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.count_pool = count_pool
        self.length_pool = length_pool

    def get_mean_speed(self) -> float:
        mean_speed = self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        """Получить среднюю скорость движения."""
        return mean_speed

    def get_spent_calories(self) -> float:
        temp = self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT
        # (средняя_скорость + 1.1) * 2 * вес * время_тренировки
        spent_calories = temp * self.CALORIES_WEIGHT_MULTIPLIER * self.weight * self.duration
        return spent_calories

    pass


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type == 'SWM':
        return Swimming(data[0], data[1], data[2], data[3], data[4])
    elif workout_type == 'RUN':
        return Running(data[0], data[1], data[2])
    elif workout_type == 'WLK':
        return SportsWalking(data[0], data[1], data[2], data[3])
    pass


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)