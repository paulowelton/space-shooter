import pygame
from random import randint

pygame.init()

largura, altura = 600, 400
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo da Nave")

espaco = pygame.image.load('assets/espaco.png')
espaco = pygame.transform.scale(espaco, (largura, altura))

tamanho_nave = 70
velocidade_nave = 5
pos_nave = [0, altura - tamanho_nave - 10]
nave = pygame.image.load('assets/nave.png')
nave = pygame.transform.scale(nave, (tamanho_nave, tamanho_nave))

inimigo_img = pygame.image.load('assets/inimigo.png')
inimigo_img = pygame.transform.scale(inimigo_img, (tamanho_nave, tamanho_nave))

tiros = []

inimigos = []

pontos = 0
vidas = 3

fonte = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()
rodando = True

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                tiro_x = pos_nave[0] + (tamanho_nave / 2) - 2
                tiro_y = pos_nave[1]
                tiros.append([tiro_x, tiro_y])

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_RIGHT] and pos_nave[0] < largura - tamanho_nave:
        pos_nave[0] += velocidade_nave
    if teclas[pygame.K_LEFT] and pos_nave[0] > 0:
        pos_nave[0] -= velocidade_nave

    tela.blit(espaco, (0, 0))

    tela.blit(nave, (pos_nave[0], pos_nave[1]))

    for tiro in tiros[:]:
        tiro[1] -= 10
        pygame.draw.rect(tela, (255, 255, 255), pygame.Rect(tiro[0], tiro[1], 4, 11))
        if tiro[1] < 0:
            tiros.remove(tiro)

    if len(inimigos) < 5:
        pos_inimigo_x = randint(0, largura - tamanho_nave)
        pos_inimigo_y = -tamanho_nave
        inimigos.append([pos_inimigo_x, pos_inimigo_y])

    for inimigo in inimigos[:]:
        inimigo[1] += 4
        tela.blit(inimigo_img, (inimigo[0], inimigo[1]))
        inimigo_rect = pygame.Rect(inimigo[0], inimigo[1], tamanho_nave, tamanho_nave)

        if inimigo[1] > altura:
            inimigos.remove(inimigo)
            continue

        for tiro in tiros[:]:
            tiro_rect = pygame.Rect(tiro[0], tiro[1], 4, 11)
            if inimigo_rect.colliderect(tiro_rect):
                inimigos.remove(inimigo)
                tiros.remove(tiro)
                pontos += 1
                break

    texto_pontos = fonte.render(f"Pontos: {pontos}", True, (255, 255, 255))
    texto_vidas = fonte.render(f"Vidas: {vidas}", True, (255, 255, 255))
    tela.blit(texto_pontos, (10, 10))
    tela.blit(texto_vidas, (10, 40))

    if vidas <= 0:
        game_over_texto = fonte.render("GAME OVER", True, (255, 0, 0))
        tela.blit(game_over_texto, (largura // 2 - 80, altura // 2 - 20))
        pygame.display.flip()
        pygame.time.wait(3000)
        rodando = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
