def greet():
    print(".....................................")
    print("Добро пожаловать в игру Крест и Ноль")
    print(".....................................")
    print(" формат ввода: x y ")
    print(" x - номер строки  ")
    print(" y - номер столбца ")
    print("....................")
    print("....................")
greet()     # Приветствие пипла

field = [[" "] * 3 for i in range(3) ]   # Создаём квадрат
def show():
    print(f"  0 1 2")
    for i in range(3):
        row_info = " ".join(field[i])
        print(f"{i} {row_info}")
    print("....................")
show()      # Печатаем квадрат
def ask():
    while True:
        try:
            x, y = map(int, input("! Ваш ход: ").split())
            if 0 > x or x > 2 or 0 > y or y > 2:
                print(" Координаты вне диапазона! ")
                continue
            if field[x][y] != " ":
                print(" Клетка занята! ")
                continue
            return x, y
        except ValueError:
            print(" Неправильный ввод! Пожалуйста, введите два целых числа через пробел (например, '0 1').")
ask()   # Умоляем ввести в куб силы, две убогих цыфры, вида = 0 1
def check_win():
    win_cord = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)))
    for cord in win_cord:
        symbols = []
        for c in cord:
            symbols.append(field[c[0]][c[1]])
        if symbols == ["X", "X", "X"]:
            print("Выиграл X!!!")
            return True
        if symbols == ["0", "0", "0"]:
            print("Выиграл 0!!!")
            return True
    return False

check_win()
count = 0
while True:
    count += 1
    show()
    if count % 2 == 1:
        print(" Ходит крестик!")
    else:
        print(" Ходит нолик!")
    x, y = ask()
    if count % 2 == 1:
        field[x][y] = "X"
    else:
        field[x][y] = "0"
    if check_win():
        break
    if count == 9:
        print(" Ничья!")
        break