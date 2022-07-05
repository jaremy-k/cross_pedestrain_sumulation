NAME_MY_PROGRAM = 'Cross Peds train similation'

# цвета для текста под светофорами
black = (0, 0, 0)
white = (255, 255, 255)

# Размер открываемого окна приложения
screenWidth = 1400
screenHeight = 800

# Значения таймеров сигналов по умолчанию
defaultGreen = {0: 10, 1: 10, 2: 10, 3: 10}
defaultRed = 150
defaultYellow = 5

# координаты появления пешеходов
# xt - положение по x (для пешехода идущего сверху)
# yt - положение по y (для пешехода идущего слева)
xt = 570
yt = 300

skin_ped = 'images/men.png'
background_img = 'images/intersection.png'
signal_red_img = 'images/signals/red.png'
signal_yellow_img = 'images/signals/yellow.png'
signal_green_img = 'images/signals/green.png'

speed = 1

signals = []
noOfSignals = 4
currentGreen = 0  # Указывает, какой сигнал зеленый в данный момент
nextGreen = (currentGreen + 1) % noOfSignals  # Указывает, какой сигнал станет зеленым следующим
currentYellow = 0  # Указывает, включен или выключен желтый сигнал

speeds = {'car': 2.25, 'bus': 1.8, 'truck': 1.8, 'bike': 2.5}  # Средняя скорость транспортных средств

# Координаты старта автомобилей
x = {'right': [0, 0, 0], 'down': [755, 727, 697], 'left': [1400, 1400, 1400], 'up': [602, 627, 657]}
y = {'right': [348, 370, 398], 'down': [0, 0, 0], 'left': [498, 466, 436], 'up': [800, 800, 800]}

vehicles = {'right': {0: [], 1: [], 2: [], 'crossed': 0}, 'down': {0: [], 1: [], 2: [], 'crossed': 0},
            'left': {0: [], 1: [], 2: [], 'crossed': 0}, 'up': {0: [], 1: [], 2: [], 'crossed': 0}}
vehicleTypes = {0: 'car', 1: 'bus', 2: 'truck', 3: 'bike'}
directionNumbers = {0: 'right', 1: 'down', 2: 'left', 3: 'up'}

# Координаты изображения сигналов, таймеров и количество транспортных средств
signalCoods = [(530, 230), (810, 230), (810, 570), (530, 570)]
signalTimerCoods = [(530, 210), (810, 210), (810, 550), (530, 550)]

# Координаты линий остановки для транспорта
stopLines = {'right': 590, 'down': 320, 'left': 800, 'up': 535}
defaultStop = {'right': 580, 'down': 310, 'left': 810, 'up': 545}

# Промежуток между транспортными средствами
stoppingGap = 15  # рассояние для остановки
movingGap = 15  # расстояние между движещимеся машинами