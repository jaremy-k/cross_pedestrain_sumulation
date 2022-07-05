import random
import time
import threading
import pygame
import sys
from const import *
from scipy.stats import expon
import logger
from logger import MyAdapter
from logger import MyFilter

logger = logger.get_logger(__name__)
logger = MyAdapter(logger, {'id': None})


pygame.init()
simulation = pygame.sprite.Group()

class Ped(pygame.sprite.Sprite):
    def __init__(self, v, pos):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load(skin_ped)
        self.x = pos[0] + random.randint(-5,5)
        self.y = pos[1] + random.randint(-5,5)
        self.image = pygame.transform.scale(image,(50,50))
        self.rect = self.image.get_rect(center=[self.x, self.y])
        self._layer = 10
        self.dir = v
        self.crossed = 0

    def update(self, delta, screen):
        screen.blit(self.image, (self.x, self.y))
        pygame.sprite.Sprite.update(self)
        random_speed = random.uniform(0.01, 0.1) * delta

        if (self.dir[0] == 1 and self.dir[1] == 0):
            if (self.crossed == 0 and self.x > stopLines['right']):
                self.crossed = 1

            if (self.x <= defaultStop['right'] or self.crossed == 1 or (currentGreen == 0 and currentYellow == 0)):
                self.x += self.dir[0] * random_speed;

        if (self.dir[0] == 0 and self.dir[1] == 1):
            if (self.crossed == 0 and self.y > stopLines['down']):
                self.crossed = 1

            if (self.y <= defaultStop['down'] or self.crossed == 1 or (currentGreen == 1 and currentYellow == 0)):
                self.y += self.dir[1] * random_speed;



class TrafficSignal:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.signalText = ""


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = speeds[vehicleClass]
        self.direction_number = direction_number
        self.direction = direction
        self.x = x[direction][lane]
        self.y = y[direction][lane]
        self.crossed = 0
        vehicles[direction][lane].append(self)
        self.index = len(vehicles[direction][lane]) - 1
        path = "images/" + direction + "/" + vehicleClass + ".png"
        self.image = pygame.image.load(path)

        if (len(vehicles[direction][lane]) > 1 and vehicles[direction][lane][
            self.index - 1].crossed == 0):  # если более 1 транспортного средства находится в полосе движения транспортного средства до того, как оно пересекло стоп-линию
            if (direction == 'right'):
                self.stop = vehicles[direction][lane][self.index - 1].stop - vehicles[direction][lane][
                    self.index - 1].image.get_rect().width - stoppingGap  # установка координаты остановки: координата остановки следующего транспортного средства минус ширина следующего транспортного средства минус рассояние между ними
            elif (direction == 'left'):
                self.stop = vehicles[direction][lane][self.index - 1].stop + vehicles[direction][lane][
                    self.index - 1].image.get_rect().width + stoppingGap
            elif (direction == 'down'):
                self.stop = vehicles[direction][lane][self.index - 1].stop - vehicles[direction][lane][
                    self.index - 1].image.get_rect().height - stoppingGap
            elif (direction == 'up'):
                self.stop = vehicles[direction][lane][self.index - 1].stop + vehicles[direction][lane][
                    self.index - 1].image.get_rect().height + stoppingGap
        else:
            self.stop = defaultStop[direction]

        # Установка новых координат запуска и остановки
        if (direction == 'right'):
            temp = self.image.get_rect().width + stoppingGap
            x[direction][lane] -= temp
        elif (direction == 'left'):
            temp = self.image.get_rect().width + stoppingGap
            x[direction][lane] += temp
        elif (direction == 'down'):
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] -= temp
        elif (direction == 'up'):
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] += temp
        simulation.add(self)

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        if (self.direction == 'right'):
            if (self.crossed == 0 and self.x + self.image.get_rect().width > stopLines[
                self.direction]):  # если изображение пересекло стоп-линию сейчас
                self.crossed = 1
            if ((self.x + self.image.get_rect().width <= self.stop or self.crossed == 1 or (
                    currentGreen == 0 and currentYellow == 0)) and (
                    self.index == 0 or self.x + self.image.get_rect().width < (
                    vehicles[self.direction][self.lane][self.index - 1].x - movingGap))):
                # (если изображение не достигло координаты остановки, пересекло стоп-линию или имеет зеленый сигнал) и (либо это первое транспортное средство в этой полосе, либо расстояние до следующего транспортного средства в этой полосе достигло минимума)
                self.x += self.speed  # move the vehicle
        elif (self.direction == 'down'):
            if (self.crossed == 0 and self.y + self.image.get_rect().height > stopLines[self.direction]):
                self.crossed = 1
            if ((self.y + self.image.get_rect().height <= self.stop or self.crossed == 1 or (
                    currentGreen == 1 and currentYellow == 0)) and (
                    self.index == 0 or self.y + self.image.get_rect().height < (
                    vehicles[self.direction][self.lane][self.index - 1].y - movingGap))):
                self.y += self.speed
        elif (self.direction == 'left'):
            if (self.crossed == 0 and self.x < stopLines[self.direction]):
                self.crossed = 1
            if ((self.x >= self.stop or self.crossed == 1 or (currentGreen == 2 and currentYellow == 0)) and (
                    self.index == 0 or self.x > (
                    vehicles[self.direction][self.lane][self.index - 1].x + vehicles[self.direction][self.lane][
                self.index - 1].image.get_rect().width + movingGap))):
                self.x -= self.speed
        elif (self.direction == 'up'):
            if (self.crossed == 0 and self.y < stopLines[self.direction]):
                self.crossed = 1
            if ((self.y >= self.stop or self.crossed == 1 or (currentGreen == 3 and currentYellow == 0)) and (
                    self.index == 0 or self.y > (
                    vehicles[self.direction][self.lane][self.index - 1].y + vehicles[self.direction][self.lane][
                self.index - 1].image.get_rect().height + movingGap))):
                self.y -= self.speed


# Инициализация сигналов со значениями по умолчанию
def initialize():
    ts1 = TrafficSignal(0, defaultYellow, defaultGreen[0])
    signals.append(ts1)
    ts2 = TrafficSignal(ts1.red + ts1.yellow + ts1.green, defaultYellow, defaultGreen[1])
    signals.append(ts2)
    ts3 = TrafficSignal(defaultRed, defaultYellow, defaultGreen[2])
    signals.append(ts3)
    ts4 = TrafficSignal(defaultRed, defaultYellow, defaultGreen[3])
    signals.append(ts4)
    repeat()


def repeat():
    global currentGreen, currentYellow, nextGreen
    while (signals[currentGreen].green > 0):  #пока таймер текущего зеленого сигнала не равен нулю
        updateValues()
        time.sleep(1)
    currentYellow = 1  # включить желтый сигнал
    # сбросить координаты остановок полос и транспортных средств
    for i in range(0, 3):
        for vehicle in vehicles[directionNumbers[currentGreen]][i]:
            vehicle.stop = defaultStop[directionNumbers[currentGreen]]
    while (signals[currentGreen].yellow > 0):  # пока таймер текущего желтого сигнала не равен нулю
        updateValues()
        time.sleep(1)
    currentYellow = 0  # отключить желтый сигнал

    # сбрасывает все таймеры каждого цвета светофора текущего цикла на время по умолчанию
    signals[currentGreen].green = defaultGreen[currentGreen]
    signals[currentGreen].yellow = defaultYellow
    signals[currentGreen].red = defaultRed

    currentGreen = nextGreen  # установить следующий сигнал как зеленый сигнал
    nextGreen = (currentGreen + 1) % noOfSignals  # установить следующий зеленый сигнал
    signals[nextGreen].red = signals[currentGreen].yellow + signals[
        currentGreen].green  # установливает время красного цвета до следующего цвета (время желтого + время зеленого)
    repeat()


# Обновляет значения таймеров светофора каждую секунду
def updateValues():
    for i in range(0, noOfSignals):
        if (i == currentGreen):
            if (currentYellow == 0):
                signals[i].green -= 1
            else:
                signals[i].yellow -= 1
        else:
            signals[i].red -= 1


# Генерация транспорта
def generateVehicles():
    while (True):
        vehicle_type = random.randint(0, 3)
        lane_number = random.randint(1, 2)
        temp = random.randint(0, 99)
        direction_number = 0
        dist = [25, 50, 75, 100]
        if (temp < dist[0]):
            direction_number = 0
        elif (temp < dist[1]):
            direction_number = 1
        elif (temp < dist[2]):
            direction_number = 2
        elif (temp < dist[3]):
            direction_number = 3
        Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number, directionNumbers[direction_number])
        time.sleep(1)


class Main:
    thread1 = threading.Thread(name="initialization", target=initialize, args=())  # инициализация
    thread1.daemon = True
    thread1.start()

    # Размер открываемого окна приложения
    screenSize = (screenWidth, screenHeight)

    # Установка фонового изображения, т.е. изображения перекрестка
    background = pygame.image.load(background_img)
    ped = pygame.image.load(skin_ped)
    ped = pygame.transform.scale(ped, (50, 50))

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption(NAME_MY_PROGRAM)

    # Загрузка изображений сигналов и шрифта
    redSignal = pygame.image.load(signal_red_img)
    yellowSignal = pygame.image.load(signal_yellow_img)
    greenSignal = pygame.image.load(signal_green_img)
    font = pygame.font.Font(None, 30)

    thread2 = threading.Thread(name="generateVehicles", target=generateVehicles, args=())  # Генерация транспорта
    thread2.daemon = True
    thread2.start()

    pedsGroup = pygame.sprite.Group()
    allGroup = pygame.sprite.LayeredUpdates()

    clock = pygame.time.Clock()

    delay = 500
    banana_event = pygame.USEREVENT + 1
    pygame.time.set_timer(banana_event, delay)

    while True:

        if pygame.key.get_pressed()[pygame.K_w]:
            pedl = Ped([0,1],[xt, 0])
            pedsGroup.add(pedl)

        clock.tick(140)
        delta = clock.get_time()
        x_expo = expon.rvs(scale=40, size=60000)
        x_i = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == banana_event:
                pedl = Ped([0, 1], [xt, 0])
                pedsGroup.add(pedl)
                pedl = Ped([1, 0], [0, yt])
                pedsGroup.add(pedl)

                if x_i == len(x_expo)-1:
                    x_i = 0
                banana_delay = int((x_expo[x_i] / x_expo.max()) * 60000)
                logger.info('Установка задержки', id=banana_delay)
                x_i+=1

                pygame.time.set_timer(banana_event, banana_delay)

        screen.blit(background, (0, 0))  # отрисовка основного фона

        for p in pedsGroup:
            if p.x > screenWidth or p.x < 0 or p.y > screenHeight or p.y < 0:
                p.kill()

        for i in range(0,
                       noOfSignals):  # отображает сигнал и устанавливает таймер в соответствии с текущим состоянием: зеленый, желтый или красный
            if (i == currentGreen):
                if (currentYellow == 1):
                    signals[i].signalText = signals[i].yellow
                    screen.blit(yellowSignal, signalCoods[i])
                else:
                    signals[i].signalText = signals[i].green
                    screen.blit(greenSignal, signalCoods[i])
            else:
                if (signals[i].red <= 10):
                    signals[i].signalText = signals[i].red
                else:
                    signals[i].signalText = "---"
                screen.blit(redSignal, signalCoods[i])
        signalTexts = ["", "", "", ""]

        # отрисовка signal timer
        for i in range(0, noOfSignals):
            signalTexts[i] = font.render(str(signals[i].signalText), True, white, black)
            screen.blit(signalTexts[i], signalTimerCoods[i])

        # отрисовка vehicles
        for vehicle in simulation:
            screen.blit(vehicle.image, [vehicle.x, vehicle.y])
            vehicle.move()

        pedsGroup.update(delta, screen)
        pygame.display.update()
Main()
