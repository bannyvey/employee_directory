import sys
from modes import mode_1, mode_2, mode_3, mode_4, mode_5, mode_6


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            raise IndexError("Не указан режим работы")
        mode = sys.argv[1]
        if mode == '1':
            mode_1()
        elif mode == '2':
            if len(sys.argv) != 5:
                raise ValueError(
                    'Для режима 2 нужно указать данные в формате: '
                    'python main.py 2 <"Фамилия Имя отчество"> <Год-Месяц-День> <Пол>'
                )
            mode_2(sys.argv[2], sys.argv[3], sys.argv[4])
        elif mode == '3':
            mode_3()
        elif mode == '4':
            mode_4(start_letter_for_filter='F')
        elif mode == '5':
            mode_5()
        elif mode == '6':
            mode_6()
        else:
            print(f"Неизвестный режим: {mode}. Доступные режимы: 1, 2, 3, 4, 5, 6")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
