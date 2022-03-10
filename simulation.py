import random
import time
import threading
import pygame
import sys

# Default values of signal timers
defaultGreen = {0: 10, 1: 10, 2: 10, 3: 10}
defaultRed = 150
defaultYellow = 5

xt = 570
yt = 300

speed = 1

signals = []
noOfSignals = 4
currentGreen = 0  # Indicates which signal is green currently
nextGreen = (currentGreen + 1) % noOfSignals  # Indicates which signal will turn green next
currentYellow = 0  # Indicates whether yellow signal is on or off

speeds = {'car': 2.25, 'bus': 1.8, 'truck': 1.8, 'bike': 2.5}  # average speeds of vehicles

# Coordinates of vehicles' start
x = {'right': [0, 0, 0], 'down': [755, 727, 697], 'left': [1400, 1400, 1400], 'up': [602, 627, 657]}
y = {'right': [348, 370, 398], 'down': [0, 0, 0], 'left': [498, 466, 436], 'up': [800, 800, 800]}

vehicles = {'right': {0: [], 1: [], 2: [], 'crossed': 0}, 'down': {0: [], 1: [], 2: [], 'crossed': 0},
            'left': {0: [], 1: [], 2: [], 'crossed': 0}, 'up': {0: [], 1: [], 2: [], 'crossed': 0}}
vehicleTypes = {0: 'car', 1: 'bus', 2: 'truck', 3: 'bike'}
directionNumbers = {0: 'right', 1: 'down', 2: 'left', 3: 'up'}

# Coordinates of signal image, timer, and vehicle count
signalCoods = [(530, 230), (810, 230), (810, 570), (530, 570)]
signalTimerCoods = [(530, 210), (810, 210), (810, 550), (530, 550)]

# Coordinates of stop lines
stopLines = {'right': 590, 'down': 320, 'left': 800, 'up': 535}
defaultStop = {'right': 580, 'down': 310, 'left': 810, 'up': 545}
# stops = {'right': [580,580,580], 'down': [320,320,320], 'left': [810,810,810], 'up': [545,545,545]}

# Gap between vehicles
stoppingGap = 15  # stopping gap
movingGap = 15  # moving gap

pygame.init()
simulation = pygame.sprite.Group()



class Ped(pygame.sprite.Sprite):
    def __init__(self, v, pos):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('images/men.png')
        self.x = pos[0] + random.randint(-5,5)
        self.y = pos[1] + random.randint(-5,5)
        self.image = pygame.transform.scale(image,(50,50))
        self.rect = self.image.get_rect(center=[self.x, self.y])
        self._layer = 10
        self.dir = v
        self.crossed = 0

        # pedl = Ped([0,1],[xt, 0])

    #def render(self, screen):


    # def move(self):
    #     while True:
    #         self.x += 10

    def update(self, delta, screen):
        screen.blit(self.image, (self.x, self.y))
        pygame.sprite.Sprite.update(self)
        random_speed = random.uniform(0.01, 0.1) * delta

        if (self.dir[0] == 1 and self.dir[1] == 0):
            if (self.crossed == 0 and self.x > stopLines['right']):
                self.crossed = 1

            if (self.x <= defaultStop['right'] or self.crossed == 1 or (currentGreen == 0 and currentYellow == 0)):
                self.x += self.dir[0] * random_speed;
                # self.y += self.dir[1] * random_speed;

                # if self.collide:
                #     self.x -= self.dir[0] * random_speed;

        if (self.dir[0] == 0 and self.dir[1] == 1):
            if (self.crossed == 0 and self.y > stopLines['down']):
                self.crossed = 1

            if (self.y <= defaultStop['down'] or self.crossed == 1 or (currentGreen == 1 and currentYellow == 0)):
                # self.x += self.dir[0] * random.uniform(0.01, 0.1) * delta;
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
            self.index - 1].crossed == 0):  # if more than 1 vehicle in the lane of vehicle before it has crossed stop line
            if (direction == 'right'):
                self.stop = vehicles[direction][lane][self.index - 1].stop - vehicles[direction][lane][
                    self.index - 1].image.get_rect().width - stoppingGap  # setting stop coordinate as: stop coordinate of next vehicle - width of next vehicle - gap
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

        # Set new starting and stopping coordinate
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
                self.direction]):  # if the image has crossed stop line now
                self.crossed = 1
            if ((self.x + self.image.get_rect().width <= self.stop or self.crossed == 1 or (
                    currentGreen == 0 and currentYellow == 0)) and (
                    self.index == 0 or self.x + self.image.get_rect().width < (
                    vehicles[self.direction][self.lane][self.index - 1].x - movingGap))):
                # (if the image has not reached its stop coordinate or has crossed stop line or has green signal) and (it is either the first vehicle in that lane or it is has enough gap to the next vehicle in that lane)
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


# Initialization of signals with default values
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
    while (signals[currentGreen].green > 0):  # while the timer of current green signal is not zero
        updateValues()
        time.sleep(1)
    currentYellow = 1  # set yellow signal on
    # reset stop coordinates of lanes and vehicles 
    for i in range(0, 3):
        for vehicle in vehicles[directionNumbers[currentGreen]][i]:
            vehicle.stop = defaultStop[directionNumbers[currentGreen]]
    while (signals[currentGreen].yellow > 0):  # while the timer of current yellow signal is not zero
        updateValues()
        time.sleep(1)
    currentYellow = 0  # set yellow signal off

    # reset all signal times of current signal to default times
    signals[currentGreen].green = defaultGreen[currentGreen]
    signals[currentGreen].yellow = defaultYellow
    signals[currentGreen].red = defaultRed

    currentGreen = nextGreen  # set next signal as green signal
    nextGreen = (currentGreen + 1) % noOfSignals  # set next green signal
    signals[nextGreen].red = signals[currentGreen].yellow + signals[
        currentGreen].green  # set the red time of next to next signal as (yellow time + green time) of next signal
    repeat()


# Update values of the signal timers after every second
def updateValues():
    for i in range(0, noOfSignals):
        if (i == currentGreen):
            if (currentYellow == 0):
                signals[i].green -= 1
            else:
                signals[i].yellow -= 1
        else:
            signals[i].red -= 1


# Generating vehicles in the simulation
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

# def pedmove():
#     global speed
#     for speed in range(0, 100):
#         global xt
#         xt += speed
#     return xt

class Main:
    thread1 = threading.Thread(name="initialization", target=initialize, args=())  # initialization
    thread1.daemon = True
    thread1.start()

    # Colours 
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Screensize 
    screenWidth = 1400
    screenHeight = 800
    screenSize = (screenWidth, screenHeight)

    # Setting background image i.e. image of intersection
    background = pygame.image.load('images/intersection.png')
    ped = pygame.image.load('images/men.png')
    ped = pygame.transform.scale(ped, (50, 50))

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("SIMULATION")

    # Loading signal images and font
    redSignal = pygame.image.load('images/signals/red.png')
    yellowSignal = pygame.image.load('images/signals/yellow.png')
    greenSignal = pygame.image.load('images/signals/green.png')
    font = pygame.font.Font(None, 30)

    thread2 = threading.Thread(name="generateVehicles", target=generateVehicles, args=())  # Generating vehicles
    thread2.daemon = True
    thread2.start()


    pedsGroup = pygame.sprite.Group()
    allGroup = pygame.sprite.LayeredUpdates()

    # ped_l = Ped([1, 0], [xt, yt])
    # pedsGroup.add(ped_l)

    # ped_r = Ped([0, 1], [xt, yt])
    # pedsGroup.add(ped_r)

    # ped_l = Ped([1,0],[xt,yt])
    # pedsGroup.add(ped_l)
    #
    # ped_r = Ped([0, 1], [xt, yt])
    # pedsGroup.add(ped_r)

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == banana_event:
                pedl = Ped([0, 1], [xt, 0])
                pedsGroup.add(pedl)
                pedl = Ped([1, 0], [0, yt])
                pedsGroup.add(pedl)
                banana_delay = random.randint(500, 1500)  # random from 0.5 to 3 seconds
                pygame.time.set_timer(banana_event, banana_delay)

                # if self.collide:
                #     self.x -= self.dir[0] * random_speed;

        screen.blit(background, (0, 0))  # display background in simulation

        # print(ped_l.x)
        # if ped_l.x >= 1000:
        #     ped_l.x = Ped([0, 1], [xt, 0])
        #     pedsGroup.add(ped_l)

        # # pedmove()
        #pedsGroup.render(screen)

        #allGroup.add(projectileGroup)

        # if yt < 400:
        #     yt += 1
        # if yt >= 400:
        #     yt -= 1
        #     print(yt)

        for p in pedsGroup:
            if p.x > screenWidth or p.x < 0 or p.y > screenHeight or p.y < 0:
                p.kill()

        for i in range(0,
                       noOfSignals):  # display signal and set timer according to current status: green, yellow, or red
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

        # display signal timer
        for i in range(0, noOfSignals):
            signalTexts[i] = font.render(str(signals[i].signalText), True, white, black)
            screen.blit(signalTexts[i], signalTimerCoods[i])

        # display the vehicles
        for vehicle in simulation:
            screen.blit(vehicle.image, [vehicle.x, vehicle.y])
            vehicle.move()

        # x = 50
        # y = 50

        # speed = 1

        # for speed in range(0 , 100):
        #     x += i
        #     screen.blit(ped, [x, y])

        pedsGroup.update(delta, screen)


        pygame.display.update()


Main()
