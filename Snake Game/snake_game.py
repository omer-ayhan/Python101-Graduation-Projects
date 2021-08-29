import pygame
import random
import sys

pencere_genisligi = 600
pencere_yuksekligi = 600

kare_boy = 20
kare_genisligi = pencere_genisligi / kare_boy
kare_yuksekligi = pencere_yuksekligi / kare_boy

acik_mavi = (191,239,255)
koyu_mavi = (173,216,230)
yemek_renk = (255,0,0)  # kırmızı
yilan_renk = (54,54,54)  # koyuGri

yukari = (0,-1)
asagi = (0,1)
saga = (1,0)
sola = (-1,0)

class YİLAN:
    def __init__(self):
        self.pozisyons = [((pencere_genisligi / 2), (pencere_yuksekligi / 2))]
        self.uzunluk = 1
        self.yon = random.choice([yukari,asagi,saga,sola])
        self.renk = yilan_renk
        self.puan = 0
    def ciz(self, yuzey):
        for p in self.pozisyons:
            dortgen = pygame.Rect((p[0], p[1]), (kare_boy,kare_boy))
            pygame.draw.rect(yuzey, self.renk, dortgen)
    def hareket(self):
        bas = self.pozisyons[0]
        x,y = self.yon
        yeni = ((bas[0] + (x * kare_boy)), (bas[1] + (y * kare_boy)))
        if yeni[0] in range(0, pencere_genisligi) and yeni[1] in range(0, pencere_yuksekligi) and not yeni in self.pozisyons[2:]:
            self.pozisyons.insert(0,yeni)
            if len(self.pozisyons) > self.uzunluk:
                self.pozisyons.pop()
        else:
            self.sifirla()
    def sifirla(self):
        self.uzunluk = 1
        self.pozisyons = [((pencere_genisligi / 2), (pencere_yuksekligi / 2))]
        self.yon = random.choice([yukari, asagi, saga, sola])
        self.puan = 0

    def anahtarlar(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(yukari)
                elif event.key == pygame.K_DOWN:
                    self.turn(asagi)
                elif event.key == pygame.K_RIGHT:
                    self.turn(saga)
                elif event.key == pygame.K_LEFT:
                    self.turn(sola)
    def turn(self,yon):
        if (yon[0] * -1 , yon[1] * -1) == self.yon:
            return
        else:
            self.yon = yon



class YEMEK:
    def __init__(self):
        self.pozisyon = (0,0)
        self.renk = yemek_renk
        self.rastgele_pozisyon()
    def rastgele_pozisyon(self):
        self.pozisyon = (random.randint(0,kare_genisligi-1)*kare_boy, random.randint(0,kare_yuksekligi-1)*kare_boy)
    def ciz(self,yuzey):
        dortgen = pygame.Rect((self.pozisyon[0],self.pozisyon[1]),(kare_boy, kare_boy))
        pygame.draw.rect(yuzey, self.renk, dortgen)


def kare_ciz(yuzey):
    for y in range(0, int(kare_yuksekligi)):
        for x in range(0, int(kare_genisligi)):
            if (x + y) % 2 == 0:
                acik = pygame.Rect((x * kare_boy, y * kare_boy),(kare_boy, kare_boy))
                pygame.draw.rect(yuzey,acik_mavi,acik)
            else:
                koyu = pygame.Rect((x * kare_boy, y * kare_boy), (kare_boy, kare_boy))
                pygame.draw.rect(yuzey,koyu_mavi,koyu)
def main():
    pygame.init()
    pencere = pygame.display.set_mode((pencere_genisligi,pencere_yuksekligi))
    saat = pygame.time.Clock()
    yazi_tipi = pygame.font.SysFont("arial",25)
    yuzey = pygame.Surface(pencere.get_size())
    yuzey = yuzey.convert()

    yemek = YEMEK()
    yilan = YİLAN()


    while True:
        saat.tick(5)
        yilan.anahtarlar()
        yilan.hareket()
        kare_ciz(yuzey)
        if yilan.pozisyons[0] == yemek.pozisyon:
            yilan.uzunluk += 1
            yilan.puan += 1
            yemek.rastgele_pozisyon()
        yilan.ciz(yuzey)
        yemek.ciz(yuzey)
        pencere.blit(yuzey,(0,0))
        puan_metni = yazi_tipi.render("Puan:{0}".format(yilan.puan), True, (0, 0, 0))
        pencere.blit(puan_metni,(10,10))
        pygame.display.update()

main()