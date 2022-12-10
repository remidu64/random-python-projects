import pygame
from decimal import *

#initialiser le code
pygame.init()

#des couleurs
rouge = (255, 0, 0)
vert = (0, 255, 0)
bleu = (0, 0, 255)
blanc= (255, 255, 255)
noir = (0, 0, 0)
violet = (127, 0, 255)
orange = (255, 165, 0)
bleu_clair = (0 ,255, 255)
rose = (255, 0, 255)
bleu_fonce = (0, 0, 63)

#définir l'écran
ecran_Y = 720
ecran_X = round(ecran_Y * (16/9))
ecran = pygame.display.set_mode([ecran_X,ecran_Y])
pygame.display.set_caption("test")
arriere_plan = bleu_fonce
fps = 60
font = pygame.font.Font("freesansbold.ttf", 20)
timer = pygame.time.Clock()

#variables
pointsproj = []
vertices = []
temp = []
temp2 = []

#truc utiles
def drawline(p1,p2,color = noir):
    pygame.draw.line(ecran,color,p1,p2,width=3)

def figure3D(points,trait , c = [2,2,2]):
    global pointsproj
    global vertices
    global temp
    global temp2
    temp3 = []

    pointsproj = []
    vertices = []
    temp = []
    temp2 = []

    for i in range(len(points)):
        temp = points[i]
        temp2 = []
        temp3 = []
        # Xp = ((x - xc) * ((z - zc) / z)) + x
        # la meme chose pour Yp
        temp[0] = ((temp[0] - c[0]) * ((temp[2] - c[2]) / temp[2])) + temp[0]
        temp[1] = ((temp[1] - c[1]) * ((temp[2] - c[2]) / temp[2])) + temp[1]

        pointsproj += temp2

    for i in range(len(trait)):
        for j in range(2):
            temp3 = []
            temp = trait[i]
            temp2 = temp[j]

            if temp2 > len(trait):
                temp2 = len(trait) - 1
            temp3 += pointsproj[temp2]

        vertices += temp3











    print(vertices)

def axe():
    global vertices
    vertices = [[[150.0, 150.0], [150.0, 250.0]], [[150.0, 150.0], [250.0, 150.0]], [[150.0, 150.0], [175.0, 175.0]]]

def drawfig(vertice):
    NV = len(vertice)
    temp = []
    for i in range(NV):
        point = vertice[i]
        drawline(point[0],point[1])







#mettre le code en dessous

figure3D([[24,46,64],[241,23,126],[555,75,234]],[[0,1],[1,2],[2,0]])

#mettre le code au desssus


#la où ya le code
run = True
while run:

    timer.tick(fps)

    #quitter le jeu

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    ecran.fill(arriere_plan)
    drawfig(vertices)


    pygame.display.flip()

pygame.quit()


