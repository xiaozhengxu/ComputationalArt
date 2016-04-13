""" Xiaozheng Xu's code for a music pulser from a set of images """  
import alsaaudio
import audioop 
import pygame 
from pygame.locals import QUIT, KEYDOWN, MOUSEMOTION, MOUSEBUTTONDOWN

#set up pygame 
pygame.init()
size = (350, 350)
screen = pygame.display.set_mode(size)

def music_pulser(movie_number=9):
    running=True
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,0)
    inp.setchannels(1)
    inp.setrate(16000)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp.setperiodsize(160)
            
    while running:
        l,data = inp.read()
        if l:
            volume=audioop.rms(data,2)
            print volume

        frame_num=min(volume/5+1,100)

        image=pygame.image.load('/home/xiaozheng/Softdes/ComputationalArt/movie_frames/movie'+str(movie_number)+'/frame'+str(frame_num)+'.png').convert_alpha()
        screen.blit(image,(0,0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False


music_pulser(8)