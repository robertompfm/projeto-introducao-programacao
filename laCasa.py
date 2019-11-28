import pygame


pygame.init()

# constants
BLACK = (0, 0, 0)
GREY = (235, 235, 235)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WIDTH = 520
HEIGHT = 376

WALK_RIGHT = [pygame.image.load('images/R1.png'), pygame.image.load('images/R2.png'), pygame.image.load('images/R3.png')]
WALK_LEFT = [pygame.image.load('images/L1.png'), pygame.image.load('images/L2.png'), pygame.image.load('images/L3.png')]
WALK_FRONT = [pygame.image.load('images/F1.png'), pygame.image.load('images/F2.png'), pygame.image.load('images/F3.png')]
WALK_BACK = [pygame.image.load('images/B1.png'), pygame.image.load('images/B2.png'), pygame.image.load('images/B3.png')]

FPS = 27

BG = pygame.image.load('images/background7.png')

MSG_DICT = {"bed":"Nossa ele dorme!!", "robot": "''Hello stranger, a resposta é muito fácil, basta multiplicar 111 x 10''",
		"shelf": "A coleção de the Big Bang Theory... e um livro velho, 'Código Binário'", "vgame": "Prefiro Mario Kart...",
		"table": "Quem tem uma tabela periodica no quarto? talvez seja uma dica!"}

RIDDLE = ["Riddle me this:", "Arrah, Arrah, and gather ’round,", "this hero is legion-bound,",
         "He multiplies N by the number of He,", "and in this room the thing you’ll see."]

# set up fonts
BASIC_FONT = pygame.font.Font("fonts/advanced_pixel.ttf", 54)
CLOCK_FONT = pygame.font.Font("fonts/advanced_pixel.ttf", 34)
TEXT_FONT = pygame.font.Font("fonts/advanced_pixel.ttf", 24)
FONT_TEST = pygame.font.Font("fonts/advanced_pixel.ttf", 30)
LACASA_FONT = pygame.font.Font("fonts/lacasa.otf", 34)


TEXT_INTRO = "O Professor Marcelo te deu nota baixa novamente. Mas nem tudo esta perdido!\n"\
            "Você acabou de invadir a casa dele e podera mudar sua nota acessando o computador do Professor.\n"\
            "Porem para ter esse acesso você precisara responder um enigma\n"\
            "Seja rapido! O Professor volta do cinema em 5 minutos\n"\
            "Use as setas do teclado para se mover.\n"\
            "Aperte ESPAÇO para interagir com os objetos. Eles podem conter dicas.\n"\
            "\n"\
            "Aperte qualquer tecla para começar!"

# useful functions

def textFormat(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)

    return newText

def blit_text(surface, text, pos, font, color=WHITE):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    word_height = 0
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.



class HouseObjects(object):
    def __init__(self, x, y, width, height, name):
        self.name = name
        self.smallRect = pygame.Rect(x, y, width, height)
        self.bigRect = pygame.Rect(x - 6, y - 6, width + 12, height + 12)


    def checkCollision(self, rect):
        return self.smallRect.colliderect(rect)


    def checkInteraction(self, rect):
        return self.bigRect.colliderect(rect)


    def drawMessage(self, win):
        if self.name != "computer":
            pygame.draw.rect(win, GREY, (0, 296, 516, 80))
            pygame.draw.rect(win, BLACK, (5, 301, 506, 70), 2)
            text = TEXT_FONT.render(MSG_DICT[self.name], True, BLACK)
            text_rect = pygame.Rect(10, 316, 506, 65)
            win.blit(text, text_rect)
        else:
            rect_origin = [(WIDTH//10), (HEIGHT//10)]
            rect_dimensions = [(WIDTH - 2 * (WIDTH//10)), (HEIGHT - 2 * (HEIGHT//10))]
            pygame.draw.rect(win, GREY, (rect_origin, rect_dimensions))
            pygame.draw.rect(win, BLACK, (rect_origin[0] + 5, rect_origin[1] + 5,\
                 rect_dimensions[0] - 10, rect_dimensions[1] - 10), 2)
            self.drawRiddleText(win)
            if game.inputting:
                self.drawInput(win)
            else:
                self.drawResult(win)


    def drawRiddleText(self, win):
        spacing = 30
        counter = 1
        for line in RIDDLE:
            lineText = textFormat(line, "fonts/advanced_pixel.ttf", 30, BLACK)
            linePos = ((WIDTH//2 - lineText.get_rect().width//2), (HEIGHT//2 - 150 + counter * spacing))
            win.blit(lineText, linePos)
            counter += 1


    def drawInput(self, win):
        titleText = textFormat("Answer: ", "fonts/advanced_pixel.ttf", 30, BLACK)
        titlePos = ((WIDTH//2 - titleText.get_rect().width), (HEIGHT//2 + 70))
        win.blit(titleText, titlePos)
        
        answerText = textFormat(game.input, "fonts/advanced_pixel.ttf", 30, BLACK)
        answerPos = ((WIDTH//2), (HEIGHT//2 + 70))
        win.blit(answerText, answerPos)


    def drawResult(self, win):
        message = "WRONG!"
        if game.victory:
            message = "CORRECT!"

        resultText = textFormat(message, "fonts/advanced_pixel.ttf", 36, BLACK)
        resultPos = ((WIDTH//2 - resultText.get_rect().width//2), (HEIGHT//2 + 70))
        win.blit(resultText, resultPos)


class player(object):
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.vel = 5
        self.left = False
        self.right = False
        self.front = False
        self.back = False
        self.walkCount = 0
        self.hitbox = pygame.Rect(x, y, 35, 63)
        self.lastPos = WALK_BACK


    def draw(self, win):
        if self.walkCount + 1 >= FPS:
            self.walkCount = 0

        if self.left:
            win.blit(WALK_LEFT[self.walkCount // 9], (self.hitbox.left, self.hitbox.top))
            self.walkCount += 1

        elif self.right:
            win.blit(WALK_RIGHT[self.walkCount // 9], (self.hitbox.left, self.hitbox.top))
            self.walkCount += 1

        elif self.front:
            win.blit(WALK_FRONT[self.walkCount // 9], (self.hitbox.left, self.hitbox.top))
            self.walkCount += 1

        elif self.back:
            win.blit(WALK_BACK[self.walkCount // 9], (self.hitbox.left, self.hitbox.top))
            self.walkCount += 1

        #aqui é a imagem quando está em repouso
        else:
            win.blit(self.lastPos[1], (self.hitbox.left, self.hitbox.top))


    def update(self, keys):
        if keys[pygame.K_LEFT] and self.hitbox.left > self.vel:
            self.lastPos = WALK_LEFT
            self.hitbox.left -= self.vel
            self.left = True
            self.right = False
            self.front = False
            self.back = False

        elif keys[pygame.K_RIGHT] and self.hitbox.left < WIDTH - self.width - self.vel:
            self.lastPos = WALK_RIGHT
            self.hitbox.left += self.vel
            self.right = True
            self.left = False
            self.front = False
            self.back = False

        elif keys[pygame.K_UP] and self.hitbox.top > 25 - self.vel:
            self.lastPos = WALK_BACK
            self.hitbox.top -= self.vel
            self.right = False
            self.left = False
            self.front = False
            self.back = True

        elif keys[pygame.K_DOWN] and self.hitbox.top < 310 - self.vel:
            self.lastPos = WALK_FRONT
            self.hitbox.top += self.vel
            self.left = False
            self.right = False
            self.front = True
            self.back = False

        else:
            self.front = False
            self.back = False
            self.right = False
            self.left = False
            self.walkCount = 0


    def canRead(self, objects):
        for object in objects:
            if object.checkInteraction(self.hitbox):
                return (True, object)
        return (False, None)


    def canMove(self, objects):
        for object in objects:
            if object.checkCollision(self.hitbox):
                return False
        return True



class Game:
    def __init__(self):
        pygame.display.set_caption("La Casa de Marcelo")
        self.win = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        self.man = player(200, 300, 36, 65)
        self.bed = HouseObjects(10, 240, 62, 55, "bed")
        self.robot = HouseObjects(43, 38, 36, 35, "robot")
        self.computer = HouseObjects(276, 41, 89, 38, "computer")
        self.shelf = HouseObjects(379, 13, 61, 67, "shelf")
        self.vgame = HouseObjects(448, 51, 49, 74, "vgame")
        self.table = HouseObjects(149, 20, 69, 8, "table")
        self.objects = [self.bed, self.robot, self.computer, self.shelf, self.vgame, self.table]
        self.activeObject = None
        self.run = True
        self.displayMsg = False
        self.startTime = 60 * 5
        self.totalTime = 5 * 60
        self.frameCount = 0
        self.clock = pygame.time.Clock()
        self.victory = False
        self.inputting = False
        self.input = ""
        self.password = "14"
        pygame.mixer.music.load('sound/loop.wav')


    def timer(self):
        self.totalTime = self.startTime - (self.frameCount // FPS)
        # When time runs out, the game is over.
        if self.totalTime == 0:
            self.run = False

        # Decreases time
        minutes = self.totalTime // 60
        seconds = self.totalTime % 60
        time_string = "{0:02}:{1:02}".format(minutes, seconds)
        time_text = CLOCK_FONT.render(time_string, True, BLACK)
        self.win.blit(time_text, [445, 10])
        self.frameCount += 1


    def redrawGameWindow(self):
        self.win.blit(BG, (0, 0))
        self.man.draw(self.win)
        self.timer()
        if self.displayMsg:
            self.activeObject.drawMessage(self.win)
            
        pygame.display.update()


    def newGame(self):
        # reset
        self.victory = False
        self.startTime = 60 * 5
        self.frameCount = 0
        self.run = True
        self.input = ""
        # start game
        self.menuScreen()
        self.intro()
        self.gameLoop()
        if self.victory:
            self.youWin()
        else:
            self.gameOver()


    def quitHandler(self, event):
        if event.type == pygame.QUIT:
            self.run = False
            pygame.quit()
            quit()
    

    def messageHandler(self, event):
        if self.man.canRead(self.objects)[0] and self.displayMsg == False and event.key == pygame.K_SPACE:
            self.displayMsg = True
            if self.man.canRead(self.objects)[1].name == "computer":
                self.inputting = True
            self.activeObject = self.man.canRead(self.objects)[1]
        elif self.displayMsg == True and \
            (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE):
            self.displayMsg = False
            if self.victory:
                self.run = False
    

    def inputHandler(self, event):
        key = pygame.key.name(event.key)  # Returns string id of pressed key.
        if len(key) == 1:  # This covers all letters and numbers not on numpad.
            self.input += key.upper()
        elif key == "backspace":
            self.input = self.input[:len(self.input) - 1]
        elif event.key == pygame.K_RETURN:  # Finished typing.
            if self.input == self.password:
                self.victory = True
            self.input = ""
            self.inputting = False


    def menuScreen(self):
        menu = True
        selected = "start"

        while menu:
            for event in pygame.event.get():
                self.quitHandler(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = "start"
                    elif event.key == pygame.K_DOWN:
                        selected = "quit"
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        if selected == "start":
                            menu = False
                        if selected=="quit":
                            pygame.quit()
                            quit()
        
            self.win.fill(BLACK)
            title1 = textFormat("La casa", "fonts/lacasa.otf", 58, WHITE)
            title2 = textFormat("de", "fonts/lacasa.otf", 48, WHITE)
            title3 = textFormat("Marcelo", "fonts/lacasa.otf", 58, WHITE)
            if selected == "start":
                textStart = textFormat("START", "fonts/lacasa.otf", 36, GREY)
            else:
                textStart = textFormat("START", "fonts/lacasa.otf", 30, WHITE)
            if selected == "quit":
                textQuit = textFormat("QUIT", "fonts/lacasa.otf", 36, GREY)
            else:
                textQuit = textFormat("QUIT", "fonts/lacasa.otf", 30, WHITE)

            titleRect1 = title1.get_rect()
            titleRect2 = title2.get_rect()
            titleRect3 = title3.get_rect()
            startRect = textStart.get_rect()
            quitRect = textQuit.get_rect()
            
            self.win.blit(title1, (WIDTH / 3.4 - (titleRect1[2] / 2), 90))
            pygame.draw.rect(self.win, RED, (238, 92, 45, 45))
            self.win.blit(title2, (WIDTH / 2 - (titleRect2[2] / 2), 95))
            self.win.blit(title3, (WIDTH / 1.4  - (titleRect3[2] / 2), 90))
            self.win.blit(textStart, (WIDTH / 2 - (startRect[2] / 2), 280))
            self.win.blit(textQuit, (WIDTH / 2 - (quitRect[2] / 2), 320))
            pygame.display.update()
            self.clock.tick(FPS)


    def intro(self):
        self.win.fill(BLACK)
        blit_text(self.win, TEXT_INTRO, (0, 0), FONT_TEST)

        pygame.display.update()

        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                self.quitHandler(event)
                if event.type == pygame.KEYUP:
                    running = False


    def gameLoop(self):
        pygame.mixer.music.play(-1)
        while self.run:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                self.quitHandler(event)
                if (event.type == pygame.KEYUP) and self.inputting:
                    self.inputHandler(event)
                elif (event.type == pygame.KEYUP):
                    self.messageHandler(event)

            if not self.displayMsg:
                keys = pygame.key.get_pressed()
                
                antX, antY = self.man.hitbox.left, self.man.hitbox.top
                
                self.man.update(keys)

                if not self.man.canMove(self.objects):
                    self.man.hitbox.left, self.man.hitbox.top = antX, antY

            self.redrawGameWindow()

    
    def gameOver(self):
        pygame.mixer.music.stop()
        menu = True
        selected = "restart"
        while menu:
            for event in pygame.event.get():
                self.quitHandler(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = "restart"
                    elif event.key == pygame.K_DOWN:
                        selected = "quit"
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        if selected == "restart":
                            menu = False
                            self.newGame()
                        if selected =="quit":
                            pygame.quit()
                            quit()

            
            self.win.fill(RED)
            title1 = textFormat("OVER", "fonts/lacasa.otf", 58, BLACK)
            title2 = textFormat("Prof. Marcelo te pegou no flagra!", "fonts/lacasa.otf", 38, BLACK)
            title3 = textFormat("GAME", "fonts/lacasa.otf", 58, BLACK)

            prof = pygame.Rect(190, 140, 0, 20)
            profImage = pygame.image.load('images/prof.png').convert_alpha()
            profStrechedImage = pygame.transform.scale(profImage, (130,132))

            if selected == "restart":
                textStart = textFormat("RESTART", "fonts/lacasa.otf", 36, GREY)
            else:
                textStart = textFormat("RESTART", "fonts/lacasa.otf", 30, BLACK)
            if selected == "quit":
                textQuit = textFormat("QUIT", "fonts/lacasa.otf", 36, GREY)
            else:
                textQuit = textFormat("QUIT", "fonts/lacasa.otf", 30, BLACK)


            titleRect1 = title1.get_rect()
            titleRect3 = title3.get_rect()

            startRect = textStart.get_rect()
            quitRect = textQuit.get_rect()

            self.win.blit(profStrechedImage, prof)
            self.win.blit(title1, (WIDTH / 1.6 - (titleRect1[2] / 2), 90))
            self.win.blit(title3, (WIDTH / 2.5  - (titleRect3[2] / 2), 90))
            self.win.blit(title2, (80, 40))
            self.win.blit(textStart, (WIDTH / 2 - (startRect[2] / 2), 280))
            self.win.blit(textQuit, (WIDTH / 2 - (quitRect[2] / 2), 320))
            pygame.display.update()
            self.clock.tick(FPS)

    
    def youWin(self):
        pygame.mixer.music.stop()
        self.win.fill(WHITE)
        titlewin1 = textFormat("Nota alterada com sucesso.", "fonts/lacasa.otf", 32, BLACK)
        titlewin2 = textFormat("Aluno APROVADO!", "fonts/lacasa.otf", 32, BLACK)
        titlewin3 = textFormat("O mercado de Trabalho te espera!", "fonts/lacasa.otf", 32, BLACK)

        diplo = pygame.Rect(220, 90, 0, 20)
        diploImage = pygame.image.load('images/diploma.png').convert_alpha()
        diploStrechedImage = pygame.transform.scale(diploImage, (70, 70))

        boss = pygame.Rect(190, 212, 0, 20)
        bossImage = pygame.image.load('images/ronald.png').convert_alpha()
        bossStrechedImage = pygame.transform.scale(bossImage, (150, 150))

        self.win.blit(diploStrechedImage, diplo)
        self.win.blit(bossStrechedImage, boss)
        self.win.blit(titlewin1, (120, 20))
        self.win.blit(titlewin2, (185, 55))
        self.win.blit(titlewin3, (90, 185))
        pygame.display.update()
        self.clock.tick(FPS)

        running = True
        while running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                self.quitHandler(event)
                if event.type == pygame.KEYUP:
                    running = False


game = Game()
game.newGame()