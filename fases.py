import pygame

class Fase:
    def __init__(self):
        self.paredes=[pygame.Rect(50,150,800,20), pygame.Rect(50,430,800,20),pygame.Rect(50,150,20,300),pygame.Rect(830,150,20,300)]
        self.area_inicial= pygame.Rect(70,170,120,260)
        self.area_final= pygame.Rect(710,170,120,260)
        self.incio = (100,300)

    def desenhar(self,tela):
        pygame.draw.rect(tela,(240,240,255), (70,170,760,260))
        pygame.draw.rect(tela,(170,255,170),self.area_inicial)
        pygame.draw.rect(tela,(170,255,170),self.area_final)

        for parede in self.paredes:
            pygame.draw.rect(tela,(0,0,0),parede)