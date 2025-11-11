#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame # Biblioteca de pygame
import os # Biblioteca os para abrir imagenes
import random # Biblioteca random para generar números random 
from pygame import mixer # para poder reproducir sonido
pygame.init()
pygame.font.init()
ANCHO, ALTO = 800, 600  ## ancho y alto de la pantalla 
imaANCHO, imaALTO = 65, 65 # Ancho y alto de las imagenes
ROJO = (136,8,8) # Color rojo 
Blanco=(255,255,255) #Color Blanco
Negro = (0,0,0) # Color negro
Letra=pygame.font.SysFont('comicsans',70) # tipo de letra

ventana = pygame.display.set_mode((ANCHO, ALTO)) #Ventana de pygame
Record = "puntajes.txt"
#Obstaculos= pygame.Rect(100,250,10,10)
pygame.display.set_caption("Space Invaders")#Nombre de la pestaña

#sonido de fondo 
mixer.music.load('Musica_fondo.mpeg')
mixer.music.play(-1)
#Portada
P = pygame.transform.scale(pygame.image.load(os.path.join('imagenes','Portada.png')),(200,200))

#Fondo de pantalla
FP = pygame.transform.scale(pygame.image.load(os.path.join('imagenes','Fondo.png')),(ANCHO,ALTO))

#Imagen de jugador 2
Nave2 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('imagenes','Nave2.png')),(imaANCHO,imaALTO)),180)

#Imagen de jugador1
Nave1 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('imagenes','Nave1.png')),(imaANCHO,imaALTO)),180)

#Balas
Bala1= pygame.transform.scale(pygame.image.load(os.path.join('imagenes','Rayos_jugador.png')),(20,30))
Bala2= pygame.transform.scale(pygame.image.load(os.path.join('imagenes','Bala2.png')),(50,40))
Bala3= pygame.transform.scale(pygame.image.load(os.path.join('imagenes','Bala3.png')),(60,50))

#Imagen de enemigos
Enemigo1 = pygame.transform.scale(pygame.image.load(os.path.join('imagenes','enemigo.png')),(imaANCHO,imaALTO))
Enemigo2 = pygame.transform.scale(pygame.image.load(os.path.join('imagenes','enemigo2.png')),(imaANCHO,imaALTO))
jefe = pygame.transform.scale(pygame.image.load(os.path.join('imagenes','jefe.png')),(imaANCHO,imaALTO))

#Clase de los disparos, sirve para crear los disparos del jugador y los enemigos
class Disparos:
    def __init__(self,x,y,imagen):
        self.x= x
        self.y= y
        self.imagen=imagen
        self.hitbox = pygame.mask.from_surface(self.imagen)
    def dibujar(self, superficie):
        superficie.blit(self.imagen,(self.x,self.y))
    def movimiento(self,velocidad):
        self.y += velocidad
    def fuera_de_rango(self, ALTO):
        return not self.y <=ALTO and self.y >= 0
    def choque(self,obstaculo):
        return choque(self,obstaculo)
#Clase Nave, es para darle forma a las imagenes de los jugadores y los enemigos
class Nave:
    ESPERA=30 # Espera es el tiempo de espera entre disparo 
    def __init__(self,x,y, vida = 50):
        self.x = x
        self.y = y
        self.vida = vida
        self.jugador_imagen = None
        self.bala_imagen = None
        self.balas=[]
        self.contador_de_balas = 0
    def dibujar(self,superficie):
        superficie.blit(self.jugador_imagen, (self.x,self.y))
        for bala in self.balas:
            bala.dibujar(superficie)
    def movimiento_balas(self,velocidad,obstaculo):
        self.tiempo()
        for bala in self.balas:
            bala.movimiento(velocidad)
            if bala.fuera_de_rango(ALTO): #Pars las balas que se salen de la pantalla se borran de las lista donde se almacenan
                self.balas.remove(bala)
            elif bala.choque(obstaculo):
                obstaculo.vida -= 10
                self.balas.remove(bala)
    def tiempo(self): #Tiempo se encarga de la espera entre balas, se tiene como maximo un total de 5 balas y luego un tiempo  de esperar de 30 segundos
        if self.contador_de_balas >= self.ESPERA:
            self.contador_de_balas = 0
        elif self.contador_de_balas > 0:
            self.contador_de_balas += 1
            
    def disparar(self): #disparar se encarga de poner las balas en la lista 
        if self.contador_de_balas == 0:
            bala = Disparos(self.x,self.y,self.bala_imagen) 
            self.balas.append(bala)
            self.contador_de_balas = 1
            
# Clase de jugador 1, le da la imagen a la nave principal y los movimientos de las balas
class Jugador1 (Nave):
    def __init__(self,x,y,vida=50):
        super().__init__(x,y,vida)
        self.jugador_imagen = Nave1
        self.bala_imagen = Bala1
        self.hitbox = pygame.mask.from_surface(self.jugador_imagen)
        self.vida_total = vida
    def movimiento_balas(self,velocidad,obstaculos):
        self.tiempo()
        for bala in self.balas:
            bala.movimiento(velocidad)
            if bala.fuera_de_rango(ALTO):
                self.balas.remove(bala)
            else:
                for obstaculo in obstaculos:
                    if bala.choque(obstaculo):
                        obstaculos.remove(obstaculo)
                        if bala in self.balas:
 
                            self.balas.remove(bala) 
                            
 # Clase jugador 2 le da la imagen y los movimientos de las balas al jugador 2                            
class Jugador2 (Nave):
    def __init__(self,x,y,vida=50):
        super().__init__(x,y,vida)
        self.jugador_imagen = Nave2
        self.bala_imagen = Bala1
        self.hitbox = pygame.mask.from_surface(self.jugador_imagen)
        self.vida_total = vida
    def movimiento_balas(self,velocidad,obstaculos):
        self.tiempo()
        for bala in self.balas:
            bala.movimiento(velocidad)
            if bala.fuera_de_rango(ALTO):
                self.balas.remove(bala)
            else:
                for obstaculo in obstaculos:
                    if bala.choque(obstaculo):
                        obstaculos.remove(obstaculo)
                        if bala in self.balas:
                            self.balas.remove(bala) 
                            
  # Clase enemigo se encarga de darle la imagen al enemigo, además incluye 3 tipos de enemigos en una lista y le da los movimientos y la forma de disparar                          
class Enemigo(Nave):
    Enemigos = {'Rojo':(Enemigo1,Bala2),'Rosado':(Enemigo2,Bala2),'Jefe':(jefe,Bala3)}
    def __init__(self,x,y,tipo, vida = 30):
        super().__init__(x,y,vida)
        self.jugador_imagen, self.bala_imagen = self.Enemigos[tipo]
        self.hitbox = pygame.mask.from_surface(self.jugador_imagen)
        
    def movimiento(self,velocidad):
        self.y += velocidad
    def disparar(self):
        if self.contador_de_balas == 0:
            bala = Disparos(self.x+20,self.y+30,self.bala_imagen) 
            self.balas.append(bala)
            self.contador_de_balas = 1

# Se encarga de calcular la diferencia de x y y y con la funcion overlap de pygame, hace que cuando entán uno sobre el otro el enemigo desaparezca o el jugador pierda vida       
def choque (obstaculo1,obstaculo2): 
    diferencia_y= obstaculo2.y - obstaculo1.y
    diferencia_x=obstaculo2.x - obstaculo1.x
    return obstaculo1.hitbox.overlap(obstaculo2.hitbox,(diferencia_x,diferencia_y))!=None
       
#Función para correr el juego
def principal():
    correr=True
    FPS = 60
    temporizador = pygame.time.Clock()
    letra=pygame.font.SysFont('comicsans',20)
    letra_GAMEOVER=pygame.font.SysFont('lucidaconsole',70)
    enemigos = []
    enemigos_velocidad = 1
    bala_velocidad= 2
    longitudnivel = 5
    vidas = 5
    niveles = 0
    jugador = Jugador1(300,500)
    jugador2 = Jugador2(500,500)
    velocidad_jugador = 4
    GAMEOVER = False
    GAMEOVER_TER = 0
    # La función pantalla se encarga de ponerle cosas escritas al juego y además dibujar las imagenes de enemigos y jugadores en la pantalla
    def pantalla():
        ventana.blit(FP,(0,0))
        Letra_vidas= letra.render(f"Vidas: {vidas}",1,(Blanco))
        Letra_niveles= letra.render(f"Nivel: {niveles}", 1,(Blanco))
        ventana.blit(Letra_vidas,(10,10))
        ventana.blit(Letra_niveles,(ANCHO - Letra_niveles.get_width()-10,10))
        
        for enemigo in enemigos:
            enemigo.dibujar(ventana)
            
        jugador.dibujar(ventana)
        jugador2.dibujar(ventana)
        #Mensaje cuando se pierde
        if GAMEOVER:
            MSJGAMEOVER = letra_GAMEOVER.render('GAME OVER',1,(Blanco))
            ventana.blit(MSJGAMEOVER,(ANCHO/2 - MSJGAMEOVER.get_width()/2,300))
        pygame.display.update() 
        # While loop para correr el juego varias veces y nunca pare 
    while correr:
        pantalla() 
        temporizador.tick(FPS)
        if vidas <= 0 or jugador2.vida <=0:
            GAMEOVER= True
            GAMEOVER_TER += 1
        if vidas <= 0 or jugador.vida <=0:
            GAMEOVER= True
            GAMEOVER_TER += 1
        if GAMEOVER:
            if GAMEOVER_TER > FPS*5:
                correr = False
                menu()
            else:
                continue
        #si la lista de enemigos es 0 se cambia de nivel y aumentan los enemigos 
        if len (enemigos)==0:
            niveles += 1
            longitudnivel += 5
            for i in range(longitudnivel):
                enemigo = Enemigo(random.randrange(20, ANCHO-100), random.randrange(-1400,-100), random.choice(['Rojo','Rosado','Jefe']))
                enemigos.append(enemigo)
         # en eventos si el evento de salir se inicia, se termina el juego        
        for eventos in pygame.event.get():
            if eventos.type == pygame.QUIT:
                correr = False 
                pygame.quit()
                

             
                 
                 
         # Toas las teclas de los jugadores        
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a] and jugador.x - velocidad_jugador > 0: #izquierda
            jugador.x -= velocidad_jugador
        if teclas[pygame.K_d] and jugador.x + velocidad_jugador + imaANCHO< ANCHO : #derecha
            jugador.x += velocidad_jugador
        if teclas[pygame.K_SPACE]:
            jugador.disparar()
            sonido_bala= mixer.Sound('disparo.wav')
            sonido_bala.play()
            
        if teclas[pygame.K_LEFT] and jugador2.x - velocidad_jugador > 0: #izquierda jugador 2
            jugador2.x -= velocidad_jugador
        if teclas[pygame.K_RIGHT] and jugador2.x + velocidad_jugador + imaANCHO< ANCHO : #derecha jugador 2
            jugador2.x += velocidad_jugador
        if teclas[pygame.K_p]:
            jugador2.disparar()
            sonido_bala= mixer.Sound('disparo.wav') #Sonido del disparo
            sonido_bala.play()
        # Esta parte se encarga de las funciones de un enemigo    
        for enemigo in enemigos[:]:
            enemigo.movimiento(enemigos_velocidad)
            enemigo.movimiento_balas(bala_velocidad, jugador) # Esto es para cuando la bala le pega al jugador, la bala desaparezca
            enemigo.movimiento_balas(bala_velocidad, jugador2)
            
            # Hace que los enemigos tengan un porcentaje de disparo, es decir si es 2*60 van a tener un 50% de probabilidad de disparo cada 60 segundos que son los FPS
            if random.randrange(0,10*60) ==1:
                enemigo.disparar()
             # si el enemigo choca con el jugador, el jugador pierde 10 de vida de los 50 que tiene    
            if choque(enemigo,jugador):
                jugador.vida -= 10
                enemigos.remove(enemigo)
            if choque(enemigo,jugador2):
                jugador2.vida -= 10
                enemigos.remove(enemigo)   
            if enemigo.y + imaALTO> ALTO:
                vidas -= 1
                enemigos.remove(enemigo)
        jugador.movimiento_balas(-bala_velocidad, enemigos)
        jugador2.movimiento_balas(-bala_velocidad, enemigos)


# Para poder escribir los elementos del menú
def Elementos_menu(Texto,Letra,color,superficie,x,y):
    texto= Letra.render(Texto,1,color)
    rectangulo= texto.get_rect()
    rectangulo.topleft = (x,y)
    superficie.blit(texto,rectangulo)
    
        
# Función del menú    
def menu():   

    Mouse=False  # Mouse es el click, click es False y es verdadero cuando se da sobre algún botón      
    Letra_menu= pygame.font.SysFont('comicsans',20)
    correr = True
    while correr:
        mx,my = pygame.mouse.get_pos() # get pos, me da la posición del mause en x y y
        ventana.blit(FP,(0,0))
        Boton_1= pygame.Rect(100,350,85,12)
        Boton1= Letra_menu.render('Modo normal',1 ,(Blanco))
        
        if Boton_1.collidepoint((mx,my)): # Si la posición del mouse da click con el rectangulo del botón, entonces hace lo que el botón indica
            if Mouse:
                submenu()

    
        Boton_2 = pygame.Rect(300,350,85,12)
        Boton2= Letra_menu.render('Multijugador ',1,(Blanco))
        
        if Boton_2.collidepoint((mx,my)):
            if Mouse:
                principal()
                

        Boton_4 = pygame.Rect(650,350,50,12)
        Boton4= Letra_menu.render('Ayuda',1,(Blanco))
        
        if Boton_4.collidepoint((mx,my)):
            if Mouse:
                Ayuda()
        pygame.draw.rect(ventana,(Negro),Boton_1)
        pygame.draw.rect(ventana,(Negro),Boton_2)
   
        pygame.draw.rect(ventana,(Negro),Boton_4)
        ventana.blit(P,(ANCHO/2- P.get_width()/2, 50))
        ventana.blit(Boton1,(100,350))
        ventana.blit(Boton2,(300,350))

        ventana.blit(Boton4,(650,350))
     
        
        
        pygame.display.update()
        Mouse=False
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr   = False
                pygame.quit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    Mouse=True
# Opción de Ayuda
def Ayuda():
    correr = True
    Tamaño= pygame.font.SysFont('comicsans',20)
    while correr:
        
        ventana.blit(FP,(0,0))
        Elementos_menu('Ayuda',Letra , Blanco, ventana, ANCHO/2-100, 100)
        
        Ayuda1= Tamaño.render('Controles',1 ,(Blanco))
        ventana.blit(Ayuda1,(ANCHO/2-50,200))
        Ayuda2 = Tamaño.render('Escape = Atrás, a = Derecha, d = Izquierda, Esapcio = Disparar',1 ,(Blanco))
        ventana.blit(Ayuda2,(ANCHO/2-200,250))
        Ayuda3 = Tamaño.render('Segundo jugador',1 ,(Blanco))
        ventana.blit(Ayuda3,(ANCHO/2-65,350))
        Ayuda4 = Tamaño.render('Flecha derecha = Derecha, Flecha Izquierda = Izquierda , p = Disparar',1 ,(Blanco))
        ventana.blit(Ayuda4,(ANCHO/2-240,400))
        pygame.display.update()
       
        
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr   = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:# si se preciona escape, se devuelve 
                    menu()
#Es el submenú del modo normal, el cual indica el modo fácil, medio y díficil                    
def submenu():
    
    # Este es el modo normal del juego donde es una persona, lo unico diferente es que la clase jugador 2 no existe, es igual para medio y dificil, en medio cambia la forma de juego donde la velocidad es mayor y más enemigos y en díficil la vida es menos y la velocidad aumenta 
    Mouse=False       
    Letra_menu= pygame.font.SysFont('comicsans',20)
    correr = True
    while correr:
        mx,my = pygame.mouse.get_pos()
        ventana.blit(FP,(0,0))
        Boton_1= pygame.Rect(100,350,85,12)
        Boton1= Letra_menu.render('Modo fácil',1 ,(Blanco))
        
        if Boton_1.collidepoint((mx,my)):
            if Mouse:
                Normal()

    
        Boton_2 = pygame.Rect(300,350,85,12)
        Boton2= Letra_menu.render('Modo medio ',1,(Blanco))
        
        if Boton_2.collidepoint((mx,my)):
            if Mouse:
                Medio()
                

        Boton_3 = pygame.Rect(650,350,50,12)
        Boton3= Letra_menu.render('Modo díficl',1,(Blanco))
        
        if Boton_3.collidepoint((mx,my)):
            if Mouse:
                Dificil()
        pygame.draw.rect(ventana,(Negro),Boton_1)
        pygame.draw.rect(ventana,(Negro),Boton_2)
   
        pygame.draw.rect(ventana,(Negro),Boton_3)
        ventana.blit(P,(ANCHO/2- P.get_width()/2, 50))
        ventana.blit(Boton1,(100,350))
        ventana.blit(Boton2,(300,350))

        ventana.blit(Boton3,(650,350))
     
        
        
        pygame.display.update()
        Mouse=False
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr   = False
                pygame.quit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    Mouse=True
def Normal():
    
    class Disparos:
        def __init__(self,x,y,imagen):
            self.x= x
            self.y= y
            self.imagen=imagen
            self.hitbox = pygame.mask.from_surface(self.imagen)
        def dibujar(self, superficie):
            superficie.blit(self.imagen,(self.x,self.y))
        def movimiento(self,velocidad):
            self.y += velocidad
        def fuera_de_rango(self, ALTO):
            return not self.y <=ALTO and self.y >= 0
        def choque(self,obstaculo):
            return choque(self,obstaculo)

    class Nave:
        ESPERA=30
        def __init__(self,x,y, vida = 50):
            self.x = x
            self.y = y
            self.vida = vida
            self.jugador_imagen = None
            self.bala_imagen = None
            self.balas=[]
            self.contador_de_balas = 0
        def dibujar(self,superficie):
            superficie.blit(self.jugador_imagen, (self.x,self.y))
            for bala in self.balas:
                bala.dibujar(superficie)
        def movimiento_balas(self,velocidad,obstaculo):
            self.tiempo()
            for bala in self.balas:
                bala.movimiento(velocidad)
                if bala.fuera_de_rango(ALTO):
                    self.balas.remove(bala)
                elif bala.choque(obstaculo):
                    obstaculo.vida -= 10
                    self.balas.remove(bala)
        def tiempo(self):
            if self.contador_de_balas >= self.ESPERA:
                self.contador_de_balas = 0
            elif self.contador_de_balas > 0:
                self.contador_de_balas += 1
            
        def disparar(self):
            if self.contador_de_balas == 0:
                bala = Disparos(self.x,self.y,self.bala_imagen) 
                self.balas.append(bala)
                self.contador_de_balas = 1
            

    class Jugador1 (Nave):
        def __init__(self,x,y,vida=50):
            super().__init__(x,y,vida)
            self.jugador_imagen = Nave1
            self.bala_imagen = Bala1
            self.hitbox = pygame.mask.from_surface(self.jugador_imagen)
            self.vida_total = vida
            
        def movimiento_balas(self,velocidad,obstaculos):
            self.tiempo()
            for bala in self.balas:
                bala.movimiento(velocidad)
                if bala.fuera_de_rango(ALTO):
                    self.balas.remove(bala)
                else:
                    for obstaculo in obstaculos:
                        if bala.choque(obstaculo):
                            obstaculos.remove(obstaculo)
                            
                            
                            
                            if bala in self.balas:
                                self.balas.remove(bala) 

    class Enemigo(Nave):
        Enemigos = {'Rojo':(Enemigo1,Bala2),'Rosado':(Enemigo2,Bala2),'Jefe':(jefe,Bala3)}
        def __init__(self,x,y,tipo, vida = 30):
            super().__init__(x,y,vida)
            self.jugador_imagen, self.bala_imagen = self.Enemigos[tipo]
            self.hitbox = pygame.mask.from_surface(self.jugador_imagen)
        
        def movimiento(self,velocidad):
            self.y += velocidad
        def disparar(self):
            if self.contador_de_balas == 0:
                bala = Disparos(self.x+20,self.y+30,self.bala_imagen) 
                self.balas.append(bala)
                self.contador_de_balas = 1

       
    def choque (obstaculo1,obstaculo2): 
        diferencia_y= obstaculo2.y - obstaculo1.y
        diferencia_x=obstaculo2.x - obstaculo1.x
        return obstaculo1.hitbox.overlap(obstaculo2.hitbox,(diferencia_x,diferencia_y))!=None
       
#Función para correr el juego
    def principal2():
        correr=True
        FPS = 60
        temporizador = pygame.time.Clock()
        letra=pygame.font.SysFont('comicsans',20)
        letra_GAMEOVER=pygame.font.SysFont('lucidaconsole',70)
        enemigos = []
        enemigos_velocidad = 1
        bala_velocidad= 2
        longitudnivel = 5
        vidas = 10
        niveles = 0
        score = 0
        jugador = Jugador1(300,500)
        velocidad_jugador = 4
        GAMEOVER = False
        GAMEOVER_TER = 0
     
            
        def pantalla():
            ventana.blit(FP,(0,0))
            Letra_vidas= letra.render(f"Vidas: {vidas}",1,(Blanco))
            Letra_niveles= letra.render(f"Nivel: {niveles}", 1,(Blanco))
            Letra_puntos = letra.render (f'Puntos: {score}',1,(Blanco))
            ventana.blit(Letra_puntos,(10,25))
            ventana.blit(Letra_vidas,(10,10))
            ventana.blit(Letra_niveles,(ANCHO - Letra_niveles.get_width()-10,10))
        
            for enemigo in enemigos:
                enemigo.dibujar(ventana)
            
            jugador.dibujar(ventana)
         

            if GAMEOVER:
                MSJGAMEOVER = letra_GAMEOVER.render('GAME OVER',1,(Blanco))
                ventana.blit(MSJGAMEOVER,(ANCHO/2 - MSJGAMEOVER.get_width()/2,300))
            pygame.display.update() 
        while correr:
            pantalla() 
            temporizador.tick(FPS)
            if vidas <= 0 or jugador.vida <=0:
                GAMEOVER= True
                GAMEOVER_TER += 1
            if GAMEOVER:
                if GAMEOVER_TER > FPS*5:
                    correr = False
                    menu()
                else:
                    continue
            if len (enemigos)==0:
                niveles += 1
                score += 100
                longitudnivel += 5
                for i in range(longitudnivel):
                    enemigo = Enemigo(random.randrange(20, ANCHO-100), random.randrange(-1400,-100), random.choice(['Rojo','Rosado','Jefe']))
                    enemigos.append(enemigo)
            
                
            for eventos in pygame.event.get():
                if eventos.type == pygame.QUIT:
                    correr = False 
                    pygame.quit()
                

             
                 
                 
                 
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_a] and jugador.x - velocidad_jugador > 0: #izquierda
                jugador.x -= velocidad_jugador
            if teclas[pygame.K_d] and jugador.x + velocidad_jugador + imaANCHO< ANCHO : #derecha
                jugador.x += velocidad_jugador
            if teclas[pygame.K_SPACE]:
                jugador.disparar()
                sonido_bala= mixer.Sound('disparo.wav')
                sonido_bala.play()
            
            for enemigo in enemigos[:]:
                enemigo.movimiento(enemigos_velocidad)
                enemigo.movimiento_balas(bala_velocidad, jugador)
  
            
            
                if random.randrange(0,10*60) ==1:
                    enemigo.disparar()
                
                if choque(enemigo,jugador):
                    jugador.vida -= 10
                    enemigos.remove(enemigo)
                
                if enemigo.y + imaALTO> ALTO:
                    vidas -= 1
                    enemigos.remove(enemigo)
            jugador.movimiento_balas(-bala_velocidad, enemigos)
    principal2()
def Medio():
    
    class Disparos:
        def __init__(self,x,y,imagen):
            self.x= x
            self.y= y
            self.imagen=imagen
            self.hitbox = pygame.mask.from_surface(self.imagen)
        def dibujar(self, superficie):
            superficie.blit(self.imagen,(self.x,self.y))
        def movimiento(self,velocidad):
            self.y += velocidad
        def fuera_de_rango(self, ALTO):
            return not self.y <=ALTO and self.y >= 0
        def choque(self,obstaculo):
            return choque(self,obstaculo)

    class Nave:
        ESPERA=30
        def __init__(self,x,y, vida = 50):
            self.x = x
            self.y = y
            self.vida = vida
            self.jugador_imagen = None
            self.bala_imagen = None
            self.balas=[]
            self.contador_de_balas = 0
        def dibujar(self,superficie):
            superficie.blit(self.jugador_imagen, (self.x,self.y))
            for bala in self.balas:
                bala.dibujar(superficie)
        def movimiento_balas(self,velocidad,obstaculo):
            self.tiempo()
            for bala in self.balas:
                bala.movimiento(velocidad)
                if bala.fuera_de_rango(ALTO):
                    self.balas.remove(bala)
                elif bala.choque(obstaculo):
                    obstaculo.vida -= 10
                    self.balas.remove(bala)
        def tiempo(self):
            if self.contador_de_balas >= self.ESPERA:
                self.contador_de_balas = 0
            elif self.contador_de_balas > 0:
                self.contador_de_balas += 1
            
        def disparar(self):
            if self.contador_de_balas == 0:
                bala = Disparos(self.x,self.y,self.bala_imagen) 
                self.balas.append(bala)
                self.contador_de_balas = 1
            

    class Jugador1 (Nave):
        def __init__(self,x,y,vida=50):
            super().__init__(x,y,vida)
            self.jugador_imagen = Nave1
            self.bala_imagen = Bala1
            self.hitbox = pygame.mask.from_surface(self.jugador_imagen)
            self.vida_total = vida
            
        def movimiento_balas(self,velocidad,obstaculos):
            self.tiempo()
            for bala in self.balas:
                bala.movimiento(velocidad)
                if bala.fuera_de_rango(ALTO):
                    self.balas.remove(bala)
                else:
                    for obstaculo in obstaculos:
                        if bala.choque(obstaculo):
                            obstaculos.remove(obstaculo)
                            
                            
                            
                            if bala in self.balas:
                                self.balas.remove(bala) 

    class Enemigo(Nave):
        Enemigos = {'Rojo':(Enemigo1,Bala2),'Rosado':(Enemigo2,Bala2),'Jefe':(jefe,Bala3)}
        def __init__(self,x,y,tipo, vida = 30):
            super().__init__(x,y,vida)
            self.jugador_imagen, self.bala_imagen = self.Enemigos[tipo]
            self.hitbox = pygame.mask.from_surface(self.jugador_imagen)
        
        def movimiento(self,velocidad):
            self.y += velocidad
        def disparar(self):
            if self.contador_de_balas == 0:
                bala = Disparos(self.x+20,self.y+30,self.bala_imagen) 
                self.balas.append(bala)
                self.contador_de_balas = 1

       
    def choque (obstaculo1,obstaculo2): 
        diferencia_y= obstaculo2.y - obstaculo1.y
        diferencia_x=obstaculo2.x - obstaculo1.x
        return obstaculo1.hitbox.overlap(obstaculo2.hitbox,(diferencia_x,diferencia_y))!=None
       
#Función para correr el juego
    def principal3():
        correr=True
        FPS = 60
        temporizador = pygame.time.Clock()
        letra=pygame.font.SysFont('comicsans',20)
        letra_GAMEOVER=pygame.font.SysFont('lucidaconsole',70)
        enemigos = []
        enemigos_velocidad = 1
        bala_velocidad= 2
        longitudnivel = 5
        vidas = 5
        niveles = 0
        score = 0
        jugador = Jugador1(300,500)
        velocidad_jugador = 5
        GAMEOVER = False
        GAMEOVER_TER = 0
     
            
        def pantalla():
            ventana.blit(FP,(0,0))
            Letra_vidas= letra.render(f"Vidas: {vidas}",1,(Blanco))
            Letra_niveles= letra.render(f"Nivel: {niveles}", 1,(Blanco))
            Letra_puntos = letra.render (f'Puntos: {score}',1,(Blanco))
            ventana.blit(Letra_puntos,(10,25))
            ventana.blit(Letra_vidas,(10,10))
            ventana.blit(Letra_niveles,(ANCHO - Letra_niveles.get_width()-10,10))
        
            for enemigo in enemigos:
                enemigo.dibujar(ventana)
            
            jugador.dibujar(ventana)
         

            if GAMEOVER:
                MSJGAMEOVER = letra_GAMEOVER.render('GAME OVER',1,(Blanco))
                ventana.blit(MSJGAMEOVER,(ANCHO/2 - MSJGAMEOVER.get_width()/2,300))
            pygame.display.update() 
        while correr:
            pantalla() 
            temporizador.tick(FPS)
            if vidas <= 0 or jugador.vida <=0:
                GAMEOVER= True
                GAMEOVER_TER += 1
            if GAMEOVER:
                if GAMEOVER_TER > FPS*5:
                    correr = False
                    menu()
                else:
                    continue
            if len (enemigos)==0:
                niveles += 1
                score += 100
                longitudnivel += 7
                for i in range(longitudnivel):
                    enemigo = Enemigo(random.randrange(20, ANCHO-100), random.randrange(-1400,-100), random.choice(['Rojo','Rosado','Jefe']))
                    enemigos.append(enemigo)
            
                
            for eventos in pygame.event.get():
                if eventos.type == pygame.QUIT:
                    correr = False 
                    pygame.quit()
                

             
                 
                 
                 
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_a] and jugador.x - velocidad_jugador > 0: #izquierda
                jugador.x -= velocidad_jugador
            if teclas[pygame.K_d] and jugador.x + velocidad_jugador + imaANCHO< ANCHO : #derecha
                jugador.x += velocidad_jugador
            if teclas[pygame.K_SPACE]:
                jugador.disparar()
                sonido_bala= mixer.Sound('disparo.wav')
                sonido_bala.play()
            
            for enemigo in enemigos[:]:
                enemigo.movimiento(enemigos_velocidad)
                enemigo.movimiento_balas(bala_velocidad, jugador)
  
            
            
                if random.randrange(0,10*60) ==1:
                    enemigo.disparar()
                
                if choque(enemigo,jugador):
                    jugador.vida -= 10
                    enemigos.remove(enemigo)
                
                if enemigo.y + imaALTO> ALTO:
                    vidas -= 1
                    enemigos.remove(enemigo)
            jugador.movimiento_balas(-bala_velocidad, enemigos)
    principal3()
def Dificil():

    
    class Disparos:
        def __init__(self,x,y,imagen):
            self.x= x
            self.y= y
            self.imagen=imagen
            self.hitbox = pygame.mask.from_surface(self.imagen)
        def dibujar(self, superficie):
            superficie.blit(self.imagen,(self.x,self.y))
        def movimiento(self,velocidad):
            self.y += velocidad
        def fuera_de_rango(self, ALTO):
            return not self.y <=ALTO and self.y >= 0
        def choque(self,obstaculo):
            return choque(self,obstaculo)

    class Nave:
        ESPERA=30
        def __init__(self,x,y, vida = 50):
            self.x = x
            self.y = y
            self.vida = vida
            self.jugador_imagen = None
            self.bala_imagen = None
            self.balas=[]
            self.contador_de_balas = 0
        def dibujar(self,superficie):
            superficie.blit(self.jugador_imagen, (self.x,self.y))
            for bala in self.balas:
                bala.dibujar(superficie)
        def movimiento_balas(self,velocidad,obstaculo):
            self.tiempo()
            for bala in self.balas:
                bala.movimiento(velocidad)
                if bala.fuera_de_rango(ALTO):
                    self.balas.remove(bala)
                elif bala.choque(obstaculo):
                    obstaculo.vida -= 10
                    self.balas.remove(bala)
        def tiempo(self):
            if self.contador_de_balas >= self.ESPERA:
                self.contador_de_balas = 0
            elif self.contador_de_balas > 0:
                self.contador_de_balas += 1
            
        def disparar(self):
            if self.contador_de_balas == 0:
                bala = Disparos(self.x,self.y,self.bala_imagen) 
                self.balas.append(bala)
                self.contador_de_balas = 1
            

    class Jugador1 (Nave):
        def __init__(self,x,y,vida=50):
            super().__init__(x,y,vida)
            self.jugador_imagen = Nave1
            self.bala_imagen = Bala1
            self.hitbox = pygame.mask.from_surface(self.jugador_imagen)
            self.vida_total = vida
            
        def movimiento_balas(self,velocidad,obstaculos):
            self.tiempo()
            for bala in self.balas:
                bala.movimiento(velocidad)
                if bala.fuera_de_rango(ALTO):
                    self.balas.remove(bala)
                else:
                    for obstaculo in obstaculos:
                        if bala.choque(obstaculo):
                            obstaculos.remove(obstaculo)
                            
                            
                            
                            if bala in self.balas:
                                self.balas.remove(bala) 

    class Enemigo(Nave):
        Enemigos = {'Rojo':(Enemigo1,Bala2),'Rosado':(Enemigo2,Bala2),'Jefe':(jefe,Bala3)}
        def __init__(self,x,y,tipo, vida = 30):
            super().__init__(x,y,vida)
            self.jugador_imagen, self.bala_imagen = self.Enemigos[tipo]
            self.hitbox = pygame.mask.from_surface(self.jugador_imagen)
        
        def movimiento(self,velocidad):
            self.y += velocidad
        def disparar(self):
            if self.contador_de_balas == 0:
                bala = Disparos(self.x+20,self.y+30,self.bala_imagen) 
                self.balas.append(bala)
                self.contador_de_balas = 1

       
    def choque (obstaculo1,obstaculo2): 
        diferencia_y= obstaculo2.y - obstaculo1.y
        diferencia_x=obstaculo2.x - obstaculo1.x
        return obstaculo1.hitbox.overlap(obstaculo2.hitbox,(diferencia_x,diferencia_y))!=None
       
#Función para correr el juego
    def principal4():
        correr=True
        FPS = 60
        temporizador = pygame.time.Clock()
        letra=pygame.font.SysFont('comicsans',20)
        letra_GAMEOVER=pygame.font.SysFont('lucidaconsole',70)
        enemigos = []
        enemigos_velocidad = 1
        bala_velocidad= 5
        longitudnivel = 5
        vidas = 3
        niveles = 0
        score = 0
        jugador = Jugador1(300,500)
        velocidad_jugador = 6
        GAMEOVER = False
        GAMEOVER_TER = 0
     
            
        def pantalla():
            ventana.blit(FP,(0,0))
            Letra_vidas= letra.render(f"Vidas: {vidas}",1,(Blanco))
            Letra_niveles= letra.render(f"Nivel: {niveles}", 1,(Blanco))
            Letra_puntos = letra.render (f'Puntos: {score}',1,(Blanco))
            ventana.blit(Letra_puntos,(10,25))
            ventana.blit(Letra_vidas,(10,10))
            ventana.blit(Letra_niveles,(ANCHO - Letra_niveles.get_width()-10,10))
        
            for enemigo in enemigos:
                enemigo.dibujar(ventana)
            
            jugador.dibujar(ventana)
         

            if GAMEOVER:
                MSJGAMEOVER = letra_GAMEOVER.render('GAME OVER',1,(Blanco))
                ventana.blit(MSJGAMEOVER,(ANCHO/2 - MSJGAMEOVER.get_width()/2,300))
            pygame.display.update() 
        while correr:
            pantalla() 
            temporizador.tick(FPS)
            if vidas <= 0 or jugador.vida <=0:
                GAMEOVER= True
                GAMEOVER_TER += 1
            if GAMEOVER:
                if GAMEOVER_TER > FPS*5:
                    correr = False
                    menu()
                else:
                    continue
            if len (enemigos)==0:
                niveles += 1
                score += 100
                longitudnivel += 10 # aumenta enemigos
                for i in range(longitudnivel):
                    enemigo = Enemigo(random.randrange(20, ANCHO-100), random.randrange(-1400,-100), random.choice(['Rojo','Rosado','Jefe']))
                    enemigos.append(enemigo)
            
                
            for eventos in pygame.event.get():
                if eventos.type == pygame.QUIT:
                    correr = False 
                    pygame.quit()
                

             
                 
                 
                 
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_a] and jugador.x - velocidad_jugador > 0: #izquierda
                jugador.x -= velocidad_jugador
            if teclas[pygame.K_d] and jugador.x + velocidad_jugador + imaANCHO< ANCHO : #derecha
                jugador.x += velocidad_jugador
            if teclas[pygame.K_SPACE]:
                jugador.disparar()
                sonido_bala= mixer.Sound('disparo.wav')
                sonido_bala.play()
            
            for enemigo in enemigos[:]:
                enemigo.movimiento(enemigos_velocidad)
                enemigo.movimiento_balas(bala_velocidad, jugador)
  
            
            
                if random.randrange(0,10*60) ==1:
                    enemigo.disparar()
                
                if choque(enemigo,jugador):
                    jugador.vida -= 10
                    enemigos.remove(enemigo)
                
                if enemigo.y + imaALTO> ALTO:
                    vidas -= 1
                    enemigos.remove(enemigo)
            jugador.movimiento_balas(-bala_velocidad, enemigos)
    principal4() # llama la función principal 4
menu()
    