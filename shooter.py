import pygame
import random

# CONSTANTES PARA COLORES
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()  # SONIDO
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # CREACION DE PANTALLA
pygame.display.set_caption("Shooter")  # TITULO DE VENTANA
clock = pygame.time.Clock()  # RELOJ PARA LOS FRAMES POR SEGUNDO




def draw_text(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)


def draw_shield_bar(surface, x, y, percentage):
	BAR_LENGHT = 100
	BAR_HEIGHT = 10
	fill = (percentage / 100) * BAR_LENGHT
	border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
	fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surface, GREEN, fill)
	pygame.draw.rect(surface, WHITE, border, 2)


# CLASE JUGADOR
class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("assets/player.png").convert()	#CARGA LA IMAGEN AL SPRITE
		self.image.set_colorkey(BLACK)	#QUITA EL COLOR NEGRO DE LA IMAGEN
		self.rect = self.image.get_rect()	#OBTIENE LAS COORDENADAS RECTANGULARES DE LA IMAGEN
		# ESTABLECE LAS PROPIEDADES RECT
		self.rect.centerx = WIDTH // 2		
		self.rect.bottom = HEIGHT - 10
		self.speed_x = 0		#VELOCIDAD DE MOVIMIENTO LATERAL
		self.shield = 100

	# METODO UPDATE PARA ACTUALIZAR EL MOVIMIENTO DEL JUGADOR
	def update(self):
		self.speed_x = 0	
		keystate = pygame.key.get_pressed()		#OBTIENE LA TECLA QUE FUE PRESIONADA
		if keystate[pygame.K_LEFT]:				#SI SE PRESIONA LA TECLA IZQUIERDA EL EJE X DISMINUYE
			self.speed_x = -5
		if keystate[pygame.K_RIGHT]:			#SI PRESIONA LA TECLA DERECHA EL EJE X AUMENTA
			self.speed_x = 5
		self.rect.x += self.speed_x				#ACTUALIZA EL EJE X SEGUN LA TECLA PRESIONADA
		# CONTROLA QUE NO SE PASE DE LOS LIMITES DE LA PANTALLA
		if self.rect.right > WIDTH:				
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)
		# laser_sound.play()



class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("assets/enemy.png").convert()
		#self.image.set_colorkey(BLACK)
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = -100
		self.speedy = 5
		self.speedx = 8
		self.shield = 100

	def update(self):
		self.rect.y += self.speedy
		# SE DETIENE LA NAVE PARA QUE QUEDE EN LA PARTE SUPERIOR DE LA PANTALLA
		if self.rect.y >= 3:
			self.speedy = 0
		
		if self.rect.x >= (WIDTH - self.rect.width) or self.rect.x <= 0:
			self.speedx *= -1

		self.rect.x += self.speedx


	def shoot(self):
		bullet = Bullet2(self.rect.centerx, self.rect.height)
		all_sprites.add(bullet)
		bullets.add(bullet)

class Meteor(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = random.choice(meteor_images)					#SE CARGA UNA IMAGEN RANDOM DE LA LISTA DE METEOROS
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)		#SE CREA EN UN RANGO IGUAL AL ANCHO DE LA PANTALLA MENOS EL ANCHO DEL METEORO
		self.rect.y = random.randrange(-140, -100)					#CREA LA SENSACION DE QUE EL METEORO VA BAJANDO DESDE ARRIBA DE LA PANTALLA
		self.speedy = random.randrange(1, 10)
		self.speedx = random.randrange(-5, 5)

	def update(self):
		self.rect.y += self.speedy
		self.rect.x += self.speedx
		# SI EL METEORO SALE DE LA PANTALLA VUELVE A TOMAR LOS VALORES RANDOM PARA VOLVER A APARECER
		if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-140, - 100)
			self.speedy = random.randrange(1, 10)





# CLASE PARA LOS PROYECTILES
class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("assets/laser1.png")
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.centerx = x		#CENTER: CENTRO DEL OBJETO
		self.speedy = -10			#DECRECIENTE PARA QUE EL PROYECTIL SE DISPARE HACIA ARRIBA

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:	#SE CHECKEA LA PARTE INFERIOR DEL SPRITE
			self.kill()				#SE REMUEVE DE LA LISTA

# CLASE PROYECTIL PARA EL ENEMIGO
class Bullet2(pygame.sprite.Sprite):	
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("assets/laser.png")
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.centerx = x		#CENTER: CENTRO DEL OBJETO
		self.speedy = 10			#DECRECIENTE PARA QUE EL PROYECTIL SE DISPARE HACIA ARRIBA

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:	#SE CHECKEA LA PARTE INFERIOR DEL SPRITE
			self.kill()				#SE REMUEVE DE LA LISTA

class Explosion(pygame.sprite.Sprite):
	def __init__(self, center):
		super().__init__()
		self.image = explosion_anim[0]
		self.rect = self.image.get_rect()
		self.rect.center = center 
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50 # VELOCIDAD DE LA EXPLOSION

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_anim):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_anim[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

    

def show_go_screen():
	screen.blit(background, [0,0])
	draw_text(screen, "SHOOTER", 65, WIDTH // 2, HEIGHT // 4)
	draw_text(screen, "Presionar 1 para jugar", 27, WIDTH // 2, HEIGHT // 2)
	draw_text(screen, "0 para salir", 27, WIDTH // 2, (HEIGHT // 2) + 25)
	draw_text(screen, "Press Key", 20, WIDTH // 2, HEIGHT * 3/4)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_KP1 or event.key == pygame.K_1:
					waiting = False

				elif event.key == pygame.K_KP0 or event.key == pygame.K_0:
					pygame.quit()


	
		

# se cargan todas las imagenes de los meteoros en una lista
meteor_images = []
meteor_list = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png", "assets/meteorGrey_big4.png",
				"assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png", "assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png",
				"assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png"]
for img in meteor_list:
	meteor_images.append(pygame.image.load(img).convert())


# ----------------EXPLOTION IMAGENES --------------
explosion_anim = []
for i in range(9):
	file = "assets/regularExplosion0{}.png".format(i)
	img = pygame.image.load(file).convert()
	img.set_colorkey(BLACK)
	img_scale = pygame.transform.scale(img, (70,70))
	explosion_anim.append(img_scale)

# Cargar imagen de fondo
background = pygame.image.load("assets/background.png").convert()

# Cargar sonidos
laser_sound = pygame.mixer.Sound("assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
pygame.mixer.music.load("assets/music.ogg")
pygame.mixer.music.set_volume(0.5)


pygame.mixer.music.play(loops=-1) 		#LA MUSICA ENTRA EN UN BUCLE PARA QUE SE REPITA INFINITAMENTE


# ----------GAME OVER---------------
game_over = True
nivel = 1
contador = 0
running = True
jugandoLevel2 = True

while running:
	if game_over:

		show_go_screen()

		game_over = False
		all_sprites = pygame.sprite.Group()		#LISTA DE TODOS LOS SPRITES
		meteor_list = pygame.sprite.Group()		#LISTA DE METEOROS
		bullets = pygame.sprite.Group()

		player = Player()		#INICIALIZA EL JUGADOR
		all_sprites.add(player)	#SE AGREGA EL JUGADOR A LA LISTA        
		enemigo = Enemy()
		
		for i in range(5):		#SE CREAN 8 METEOROS
			meteor = Meteor()	
			all_sprites.add(meteor)
			meteor_list.add(meteor)
		
		score = 0

		
	clock.tick(60)	#FPS
	
	if jugandoLevel2:
		if nivel == 2:
				all_sprites.add(enemigo)
				jugandoLevel2 = False

	if nivel == 2:
		if contador % 50 == 0:
			enemigo.shoot()


	# CONTROLA LOS EVENTOS
	for event in pygame.event.get():
		if event.type == pygame.QUIT:	#CERRAR VENTANA
			running = False

		elif event.type == pygame.KEYDOWN:	#SE APRETA UNA TECLA
			if event.key == pygame.K_SPACE:	#SI ES LA BARRA ESPACIADORA EL JUGADOR DISPARA
				player.shoot()

			elif event.key == pygame.K_UP:
				pausa = True
				while pausa:
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							pausa = False
							running = False
							pygame.quit()
						
						if event.type == pygame.KEYDOWN:
							if event.key == pygame.K_c:
								pausa = False

	all_sprites.update()	#ACTUALIZA TODOS LOS SPRITES


	# colisiones - meteoro - laser
	hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True) 
	for hit in hits:
		score += 10
		# explosion_sound.play()
		explosion = Explosion(hit.rect.center)
		all_sprites.add(explosion)
		meteor = Meteor()
		all_sprites.add(meteor)
		meteor_list.add(meteor)

	# Checar colisiones - jugador - meteoro
	hits = pygame.sprite.spritecollide(player, meteor_list, True)
	for hit in hits:
		player.shield -= 25
		meteor = Meteor()
		all_sprites.add(meteor)
		meteor_list.add(meteor)
		if player.shield <= 0:
			game_over = True
			nivel = 1
			score = 0
			jugandoLevel2 = True


	hits = pygame.sprite.spritecollide(enemigo, bullets, True)
	for hit in hits:
		enemigo.shield -= 25
		score += 10
		if enemigo.shield <= 0:
			game_over = True
			nivel = 1
			score = 0
			jugandoLevel2 = True


	screen.blit(background, [0, 0])		#COLOCA LA IMAGEN DE FONDO EN LA PANTALLA

	all_sprites.draw(screen)			#SE DIBUJAN LOS SPRITES EN LA PANTALLA

	# Marcador
	draw_text(screen, str(score), 25, WIDTH // 2, 10)

	# Escudo.
	draw_shield_bar(screen, 5, 5, player.shield)
	if nivel == 2:
		draw_shield_bar(screen, 600, 5, enemigo.shield)

	pygame.display.flip()
	
	contador += 1

	if score >= 50:
		nivel = 2


pygame.quit()


