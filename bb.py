import pygame
import math
import sys
import os
import requests


GREY = (44, 41, 40)
YELLOW = (223, 168, 33)
DARK_GREY = (141,140,141)
BLACK = (0, 0, 0)
LIGHT_GREY = (230,239,201)
RED = (255, 0, 0)
WHITE = (255, 255, 255)


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
    #return relative_path



class Blackboard():
    def __init__(self, local_host_url=""):
        pygame.init()
        
        self.width = 500
        self.height = 500
        
        self.exit = False
        self.erase_on = False
        self.mouse_down = False

        self.clock = pygame.time.Clock()
        self.fps = math.inf

        self.bgcolor = GREY
        self.fgcolor = YELLOW

        self.size = 3
        self.drawing = dict.fromkeys([])

        self.logo = pygame.image.load(resource_path('logo.ico'))

        self.ctrl_pressed = True
        self.letter_key = None

        self.prev_pos = None
        self.is_down_count = 0

        self.release_points = dict.fromkeys([])

        self.right_click_undo_box = None
        self.right_click_enter_box = None
        self.right_click_change_pen_color_box = None
        self.right_click_change_bg_color_box = None
        self.right_click_clear_box = None
        self.right_click_help_box = None

        self.right_click_undo_box_border = None
        self.right_click_enter_box_border = None
        self.right_click_change_pen_color_box_border = None
        self.right_click_change_bg_color_box_border = None
        self.right_click_clear_box_border = None
        self.right_click_help_box_border = None

        self.right_click_undo_text = None
        self.right_click_enter_text = None
        self.right_click_change_pen_color_text = None
        self.right_click_change_bg_color_text = None
        self.right_click_clear_text = None
        self.right_click_help_text = None

        self.change_fg_color_red_box = None
        self.change_fg_color_red_box_border = None

        self.change_fg_color_white_box = None
        self.change_fg_color_white_box_border = None

        self.change_fg_color_yellow_box = None
        self.change_fg_color_yellow_box_border = None

        self.change_fg_color_black_box = None
        self.change_fg_color_black_box_border = None

        self.change_bg_color_red_box = None
        self.change_bg_color_red_box_border = None

        self.change_bg_color_white_box = None
        self.change_bg_color_white_box_border = None

        self.change_bg_color_yellow_box = None
        self.change_bg_color_yellow_box_border = None

        self.change_bg_color_black_box = None
        self.change_bg_color_black_box_border = None

        self.right_click_pos = None

        self.help = False

        self.ubuntu = pygame.font.Font(resource_path('Ubuntu-Light.ttf'), 14) 

        self.chalk = pygame.font.Font(resource_path('SqueakyChalkSound-ZG8.ttf'), 100) 

        self.marker = pygame.font.Font(resource_path('SmoothMarker-45d6.ttf'), 14) 

        self.firaCode = pygame.font.Font(resource_path('FiraCode-VariableFont_wght.ttf'), 14) 

        Blackboard.gameWindow = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        Blackboard.windowName = pygame.display.set_caption("Blackboard")
        Blackboard.icon = pygame.display.set_icon(self.logo)
        
        self.localhost_url = local_host_url


    def complete_line(self, srf, color, start, end, radius=1):
        if end is None:
            end = start
        dx = end[0]-start[0]
        dy = end[1]-start[1]
        distance = max(abs(dx), abs(dy))
        for i in range(distance):
            x = int( start[0]+float(i)/distance*dx)
            y = int( start[1]+float(i)/distance*dy)
            pygame.draw.circle(srf, color, (x, y), radius)
            self.drawing[((x, y, color, radius))] = None

    def draw(self, color, pos, completeLine, size=3):
        pygame.draw.circle(self.gameWindow, color, (pos[0], pos[1]), size)
        self.drawing[((pos[0], pos[1], color, size))] = None
        if completeLine:
            self.complete_line(self.gameWindow, color, (pos[0], pos[1]), self.prev_pos,  size)
        self.prev_pos = (pos[0], pos[1])


        

    def redraw_text(self):
        self.gameWindow.fill(self.bgcolor)
        for i in list(self.drawing):
            self.draw(i[2], i[:2], False, i[3])
        

        self.right_click_undo_box = None
        self.right_click_enter_box = None
        self.right_click_change_pen_color_box = None
        self.right_click_change_bg_color_box = None
        self.right_click_clear_box = None
        self.right_click_help_box = None

        self.right_click_undo_box_border = None
        self.right_click_enter_box_border = None
        self.right_click_change_pen_color_box_border = None
        self.right_click_change_bg_color_box_border = None
        self.right_click_clear_box_border = None
        self.right_click_help_box_border = None

        self.right_click_enter_text = None
        self.right_click_undo_text = None
        self.right_click_change_pen_color_text = None
        self.right_click_change_bg_color_text = None
        self.right_click_clear_text = None
        self.right_click_help_text = None

        self.change_fg_color_red_box = None
        self.change_fg_color_red_box_border = None

        self.change_fg_color_white_box = None
        self.change_fg_color_white_box_border = None

        self.change_fg_color_yellow_box = None
        self.change_fg_color_yellow_box_border = None

        self.change_fg_color_black_box = None
        self.change_fg_color_black_box_border = None


        self.change_bg_color_red_box = None
        self.change_bg_color_red_box_border = None

        self.change_bg_color_white_box = None
        self.change_bg_color_white_box_border = None

        self.change_bg_color_yellow_box = None
        self.change_bg_color_yellow_box_border = None

        self.change_bg_color_black_box = None
        self.change_bg_color_black_box_border = None


    def undo(self):
        if not len(list(self.release_points)) > 0:
            self.redraw_text()
            return None
        rel_pos = list(self.release_points)
        rev_draw = list(self.drawing)[::-1]


        if not len(rel_pos) > 1:
            rev_draw = []
        else:
            for e, i in enumerate(rev_draw):
                if (i[0], i[1]) == rel_pos[-2]:
                    rev_draw = rev_draw[e+1:]
                    break
        
        self.drawing = dict.fromkeys(rev_draw[::-1])
        self.release_points = dict.fromkeys(rel_pos[:-1])
        self.redraw_text()
        
    def evaluate(self):

        self.redraw_text()
        pygame.image.save(self.gameWindow, "ss.png")
        if self.localhost_url.endswith('/'):
            requests.get(f"http://{self.localhost_url}blackboard_data")
        else:
            requests.get(f"http://{self.localhost_url}/blackboard_data")
         


    def erase(self, pos, size):
        drawing = list(self.drawing)
        for index, i in enumerate(drawing):

            if abs(i[0] - pos[0]) < size  and abs(i[1] - pos[1]) < size:
                i = list(i)
                i[2] = self.bgcolor
                i = tuple(i)
                drawing[index] = i
                
            else:
                self.drawing[((pos[0], pos[1], self.bgcolor, size))] = None

        
        self.drawing = dict.fromkeys(drawing)
        self.redraw_text()


    def change_pen_color(self, fgcolor):

        prev_fg_color = self.fgcolor

        new_drawing = list(self.drawing)


        for e, i in enumerate(new_drawing):
            i = list(i)
            if i[2] == prev_fg_color:
                i[2] = fgcolor

            i = tuple(i)

            new_drawing[e] = i

        


        self.fgcolor = fgcolor
        self.drawing = dict.fromkeys(new_drawing)

        self.redraw_text()


    def change_bg_color(self, bgcolor):

        self.bgcolor = bgcolor

        self.redraw_text()

    
    def show_change_fg_color_box(self, x, y):
        x_coord = x + self.box_width
        y_coord = y

        color_box_len = 20
        color_box_height = 20
        border_width = 1

        self.change_bg_color_red_box = None
        self.change_bg_color_red_box_border = None

        self.change_bg_color_white_box = None
        self.change_bg_color_white_box_border = None

        self.change_bg_color_yellow_box = None
        self.change_bg_color_yellow_box_border = None

        self.change_bg_color_black_box = None
        self.change_bg_color_black_box_border = None

        self.redraw_text()
        self.right_click(self.right_click_pos)

        #RED
        self.change_fg_color_red_box = pygame.Rect(x_coord, y_coord, color_box_len, color_box_height)

        self.change_fg_color_red_box_border = pygame.Rect(x_coord, y_coord, color_box_len, color_box_height)

        pygame.draw.rect(self.gameWindow, RED, self.change_fg_color_red_box)

        pygame.draw.rect(self.gameWindow, DARK_GREY, self.change_fg_color_red_box_border, border_width)

        #WHITE
        self.change_fg_color_white_box = pygame.Rect(x_coord, y_coord+color_box_height, color_box_len, color_box_height)

        self.change_fg_color_white_box_border = pygame.Rect(x_coord, y_coord+color_box_height, color_box_len, color_box_height)

        pygame.draw.rect(self.gameWindow, WHITE, self.change_fg_color_white_box)

        pygame.draw.rect(self.gameWindow, DARK_GREY, self.change_fg_color_white_box_border, border_width)

        #YELLOW
        self.change_fg_color_yellow_box = pygame.Rect(x_coord, y_coord+color_box_height+color_box_height, color_box_len, color_box_height)

        self.change_fg_color_yellow_box_border = pygame.Rect(x_coord, y_coord+color_box_height+color_box_height, color_box_len, color_box_height)

        pygame.draw.rect(self.gameWindow, YELLOW, self.change_fg_color_yellow_box)

        pygame.draw.rect(self.gameWindow, DARK_GREY, self.change_fg_color_yellow_box_border, border_width)
        
        #BLACK
        self.change_fg_color_black_box = pygame.Rect(x_coord, y_coord+color_box_height+color_box_height+color_box_height, color_box_len, color_box_height)

        self.change_fg_color_black_box_border = pygame.Rect(x_coord, y_coord+color_box_height+color_box_height+color_box_height, color_box_len, color_box_height)

        pygame.draw.rect(self.gameWindow, GREY, self.change_fg_color_black_box)

        pygame.draw.rect(self.gameWindow, DARK_GREY, self.change_fg_color_black_box_border, border_width)

    
    def show_change_bg_color_box(self, x, y):
        x_coord = x + self.box_width
        y_coord = y

        color_box_len = 20
        color_box_height = 20
        border_width = 1

        self.change_fg_color_red_box = None
        self.change_fg_color_red_box_border = None

        self.change_fg_color_white_box = None
        self.change_fg_color_white_box_border = None

        self.change_fg_color_yellow_box = None
        self.change_fg_color_yellow_box_border = None

        self.change_fg_color_black_box = None
        self.change_fg_color_black_box_border = None

        self.redraw_text()
        self.right_click(self.right_click_pos)

        #RED
        self.change_bg_color_red_box = pygame.Rect(x_coord, y_coord, color_box_len, color_box_height)

        self.change_bg_color_red_box_border = pygame.Rect(x_coord, y_coord, color_box_len, color_box_height)

        pygame.draw.rect(self.gameWindow, RED, self.change_bg_color_red_box)

        pygame.draw.rect(self.gameWindow, DARK_GREY, self.change_bg_color_red_box_border, border_width)

        #WHITE
        self.change_bg_color_white_box = pygame.Rect(x_coord, y_coord+color_box_height, color_box_len, color_box_height)

        self.change_bg_color_white_box_border = pygame.Rect(x_coord, y_coord+color_box_height, color_box_len, color_box_height)

        pygame.draw.rect(self.gameWindow, WHITE, self.change_bg_color_white_box)

        pygame.draw.rect(self.gameWindow, DARK_GREY, self.change_bg_color_white_box_border, border_width)

        #YELLOW
        self.change_bg_color_yellow_box = pygame.Rect(x_coord, y_coord+color_box_height+color_box_height, color_box_len, color_box_height)

        self.change_bg_color_yellow_box_border = pygame.Rect(x_coord, y_coord+color_box_height+color_box_height, color_box_len, color_box_height)

        pygame.draw.rect(self.gameWindow, YELLOW, self.change_bg_color_yellow_box)

        pygame.draw.rect(self.gameWindow, DARK_GREY, self.change_bg_color_yellow_box_border, border_width)
        
        #BLACK
        self.change_bg_color_black_box = pygame.Rect(x_coord, y_coord+color_box_height+color_box_height+color_box_height, color_box_len, color_box_height)

        self.change_bg_color_black_box_border = pygame.Rect(x_coord, y_coord+color_box_height+color_box_height+color_box_height, color_box_len, color_box_height)

        pygame.draw.rect(self.gameWindow, GREY, self.change_bg_color_black_box)

        pygame.draw.rect(self.gameWindow, DARK_GREY, self.change_bg_color_black_box_border, border_width)



    def right_click(self, pos):
        self.right_click_pos = pos

        self.redraw_text()


        self.box_width = 130
        box_len = 26
        border_width = 1
        text_margin_left = 5

        self.right_click_enter_box = pygame.Rect(pos[0], pos[1], self.box_width, box_len)
        self.right_click_undo_box = pygame.Rect(pos[0], pos[1]+box_len, self.box_width, box_len)
        self.right_click_change_pen_color_box = pygame.Rect(pos[0], pos[1]+ 2*box_len, self.box_width, box_len)
        self.right_click_change_bg_color_box = pygame.Rect(pos[0], pos[1]+ 3*box_len, self.box_width, box_len)
        self.right_click_clear_box = pygame.Rect(pos[0], pos[1]+ 4*box_len, self.box_width, box_len)
        self.right_click_help_box = pygame.Rect(pos[0], pos[1]+ 5*box_len, self.box_width, box_len)

        self.right_click_enter_box_border = pygame.Rect(pos[0], pos[1], self.box_width, box_len)
        self.right_click_undo_box_border = pygame.Rect(pos[0], pos[1]+box_len, self.box_width, box_len)
        self.right_click_change_pen_color_box_border = pygame.Rect(pos[0], pos[1]+ 2*box_len, self.box_width, box_len)
        self.right_click_change_bg_color_box_border = pygame.Rect(pos[0], pos[1]+ 3*box_len, self.box_width, box_len)
        self.right_click_clear_box_border = pygame.Rect(pos[0], pos[1]+ 4*box_len, self.box_width, box_len)
        self.right_click_help_box_border = pygame.Rect(pos[0], pos[1]+ 5*box_len, self.box_width, box_len)

        self.right_click_enter_text = self.ubuntu.render('Evaluate', True, BLACK)
        self.right_click_undo_text = self.ubuntu.render('Undo', True, BLACK)
        self.right_click_change_pen_color_text = self.ubuntu.render('Change pen color', True, BLACK)
        self.right_click_change_bg_color_text = self.ubuntu.render('Change board color', True, BLACK)
        self.right_click_clear_text = self.ubuntu.render('Clear Board', True, BLACK)
        self.right_click_help_text = self.ubuntu.render('More...', True, BLACK)

        rect_center0 = self.right_click_enter_text.get_rect(midleft=(self.right_click_enter_box.midleft[0]+text_margin_left, self.right_click_enter_box.midleft[1]))
        rect_center1 = self.right_click_undo_text.get_rect(midleft=(self.right_click_undo_box.midleft[0]+text_margin_left, self.right_click_undo_box.midleft[1]))
        rect_center2 = self.right_click_change_pen_color_text.get_rect(midleft=(self.right_click_change_pen_color_box.midleft[0]+text_margin_left, self.right_click_change_pen_color_box.midleft[1]))
        rect_center3 = self.right_click_change_bg_color_text.get_rect(midleft=(self.right_click_change_bg_color_box.midleft[0]+text_margin_left, self.right_click_change_bg_color_box.midleft[1]))
        rect_center4 = self.right_click_clear_text.get_rect(midleft=(self.right_click_clear_box.midleft[0]+text_margin_left, self.right_click_clear_box.midleft[1]))
        rect_center5 = self.right_click_help_text.get_rect(midleft=(self.right_click_help_box.midleft[0]+text_margin_left, self.right_click_help_box.midleft[1]))

        pygame.draw.rect(self.gameWindow, LIGHT_GREY, self.right_click_enter_box)
        pygame.draw.rect(self.gameWindow, LIGHT_GREY, self.right_click_undo_box)
        pygame.draw.rect(self.gameWindow, LIGHT_GREY, self.right_click_change_pen_color_box)
        pygame.draw.rect(self.gameWindow, LIGHT_GREY, self.right_click_change_bg_color_box)
        pygame.draw.rect(self.gameWindow, LIGHT_GREY, self.right_click_clear_box)
        pygame.draw.rect(self.gameWindow, LIGHT_GREY, self.right_click_help_box)

        pygame.draw.rect(self.gameWindow, DARK_GREY, self.right_click_enter_box_border, border_width)
        pygame.draw.rect(self.gameWindow, DARK_GREY, self.right_click_undo_box_border, border_width)
        pygame.draw.rect(self.gameWindow, DARK_GREY, self.right_click_change_pen_color_box_border, border_width)
        pygame.draw.rect(self.gameWindow, DARK_GREY, self.right_click_change_bg_color_box_border, border_width)
        pygame.draw.rect(self.gameWindow, DARK_GREY, self.right_click_clear_box_border, border_width)
        pygame.draw.rect(self.gameWindow, DARK_GREY, self.right_click_help_box_border, border_width)

        self.gameWindow.blit(self.right_click_enter_text, rect_center0)
        self.gameWindow.blit(self.right_click_undo_text, rect_center1)
        self.gameWindow.blit(self.right_click_change_pen_color_text, rect_center2)
        self.gameWindow.blit(self.right_click_change_bg_color_text, rect_center3)
        self.gameWindow.blit(self.right_click_clear_text, rect_center4)
        self.gameWindow.blit(self.right_click_help_text, rect_center5)



    def mainBoard(self):
        self.gameWindow.fill(self.bgcolor)

        self.back = None
        self.headRect = None
        self.sizeUpRect = None
        self.sizeDownRect = None
        self.undoRect = None
        self.enterRect = None
        self.eraseRect = None
        self.clearRect = None

        if self.drawing:
            self.redraw_text()



        while not self.exit and not self.help:
            self.letter_key = None
            self.mouse = pygame.mouse.get_pos()
            
            if self.drawing == {}:
                self.release_points = dict.fromkeys([])

            if self.mouse_down:
                if not self.erase_on:
                    if self.is_down_count > 0:
                        self.draw(self.fgcolor, self.mouse, True, self.size)
                    else:
                        self.draw(self.fgcolor, self.mouse, False, self.size)
                else:
                    if self.is_down_count > 0:
                        self.erase(self.mouse, self.size)
                    else:
                        self.erase(self.mouse, self.size)
            else:
                # if self.is_down_count > 0:
                self.is_down_count = 0
                


            for event in pygame.event.get():

                if event.type  == pygame.QUIT:
                    self.exit = True

                if event.type == pygame.VIDEORESIZE:
                    self.redraw_text()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button != 3:
                        if self.right_click_enter_box or self.right_click_undo_box or self.right_click_change_pen_color_box or self.right_click_change_bg_color_box or self.right_click_clear_box or self.right_click_help_box:
                            if self.change_fg_color_red_box or self.change_fg_color_white_box or self.change_fg_color_yellow_box or self.change_fg_color_black_box:
                                if self.right_click_enter_box_border.collidepoint(self.mouse) and not self.right_click_undo_box_border.collidepoint(self.mouse) and not self.right_click_change_pen_color_box_border.collidepoint(self.mouse) and not self.right_click_change_bg_color_box_border.collidepoint(self.mouse) and not self.right_click_clear_box_border.collidepoint(self.mouse) and not self.right_click_help_box_border.collidepoint(self.mouse) and not self.change_fg_color_red_box.collidepoint(self.mouse) and not self.change_fg_color_white_box.collidepoint(self.mouse) and not self.change_fg_color_yellow_box.collidepoint(self.mouse) and not self.change_fg_color_black_box.collidepoint(self.mouse) :
                                    self.redraw_text()
                                    self.right_click_box = None
                                    self.mouse_down = True
                                    

                            elif self.change_bg_color_red_box or self.change_bg_color_white_box or self.change_bg_color_yellow_box or self.change_bg_color_black_box:
                                if not self.right_click_enter_box_border.collidepoint(self.mouse) and not self.right_click_undo_box_border.collidepoint(self.mouse) and not self.right_click_change_pen_color_box_border.collidepoint(self.mouse) and not self.right_click_change_bg_color_box_border.collidepoint(self.mouse) and not self.right_click_clear_box_border.collidepoint(self.mouse) and not self.right_click_help_box_border.collidepoint(self.mouse) and not self.change_bg_color_red_box.collidepoint(self.mouse) and not self.change_bg_color_white_box.collidepoint(self.mouse) and not self.change_bg_color_yellow_box.collidepoint(self.mouse) and not self.change_bg_color_black_box.collidepoint(self.mouse) :
                                    self.redraw_text()
                                    self.right_click_box = None
                                    self.mouse_down = True



                            else:
                                if not self.right_click_enter_box_border.collidepoint(self.mouse) and not self.right_click_undo_box_border.collidepoint(self.mouse) and not self.right_click_change_pen_color_box_border.collidepoint(self.mouse) and not self.right_click_change_bg_color_box_border.collidepoint(self.mouse) and not self.right_click_clear_box_border.collidepoint(self.mouse) and not self.right_click_help_box_border.collidepoint(self.mouse):
                                    self.redraw_text()
                                    self.right_click_box = None
                                    self.mouse_down = True




                        else:
                            self.mouse_down = True

                if event.type == pygame.MOUSEMOTION:
                    if self.mouse_down:
                        self.is_down_count+=1


                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button != 3:
                        if self.right_click_enter_box or self.right_click_undo_box or self.right_click_change_pen_color_box or self.right_click_change_bg_color_box or self.right_click_clear_box or self.right_click_help_box:
                            if (self.change_fg_color_red_box or self.change_fg_color_white_box or self.change_fg_color_yellow_box or self.change_fg_color_black_box):                            
                                if not (self.right_click_undo_box.collidepoint(self.mouse) or self.right_click_enter_box.collidepoint(self.mouse) or self.right_click_change_pen_color_box.collidepoint(self.mouse) or self.right_click_change_bg_color_box.collidepoint(self.mouse) or self.right_click_clear_box.collidepoint(self.mouse) or self.right_click_help_box.collidepoint(self.mouse) or self.change_fg_color_red_box.collidepoint(self.mouse) or self.change_fg_color_white_box.collidepoint(self.mouse) or self.change_fg_color_yellow_box.collidepoint(self.mouse) or self.change_fg_color_black_box.collidepoint(self.mouse)):
                                    self.mouse_down = False
                                    self.release_points[(self.mouse)] = None
                                    self.redraw_text()

                                elif self.change_fg_color_red_box.collidepoint(self.mouse):
                                    self.change_pen_color(RED)

                                elif self.change_fg_color_white_box.collidepoint(self.mouse):
                                    self.change_pen_color(WHITE)

                                elif self.change_fg_color_yellow_box.collidepoint(self.mouse):
                                    self.change_pen_color(YELLOW)

                                elif self.change_fg_color_black_box.collidepoint(self.mouse):
                                    self.change_pen_color(GREY)


                                elif self.right_click_undo_box_border.collidepoint(self.mouse):
                                    self.undo()
                                    self.right_click_box = None
                                    
                                elif self.right_click_enter_box_border.collidepoint(self.mouse):
                                    self.evaluate()
                                    self.right_click_box = None

                                    
                                elif self.right_click_change_pen_color_box_border.collidepoint(self.mouse):
                                    self.show_change_fg_color_box(
                                        self.right_click_change_pen_color_box_border.x,
                                        self.right_click_change_pen_color_box_border.y
                                    )

                                

                                elif self.right_click_change_bg_color_box_border.collidepoint(self.mouse):
                                    self.show_change_bg_color_box(
                                        self.right_click_change_bg_color_box.x,
                                        self.right_click_change_bg_color_box.y

                                    )

                                elif self.right_click_clear_box_border.collidepoint(self.mouse):
                                    self.gameWindow.fill(self.bgcolor)
                                    self.drawing = dict.fromkeys([])
                                    self.release_points = dict.fromkeys([])
                                    self.right_click_pos = None
                                    
                                    self.right_click_box = None
                                    
                                    self.right_click_undo_box = None
                                    self.right_click_enter_box = None
                                    self.right_click_change_pen_color_box = None
                                    self.right_click_change_bg_color_box = None
                                    self.right_click_clear_box = None
                                    self.right_click_help_box = None
                            
                                    self.right_click_undo_box_border = None
                                    self.right_click_enter_box_border = None
                                    self.right_click_change_pen_color_box_border = None
                                    self.right_click_change_bg_color_box_border = None
                                    self.right_click_clear_box_border = None
                                    self.right_click_help_box_border = None
                            
                                    self.right_click_undo_text = None
                                    self.right_click_enter_text = None
                                    self.right_click_change_pen_color_text = None
                                    self.right_click_change_bg_color_text = None
                                    self.right_click_clear_text = None
                                    self.right_click_help_text = None
                                    
                                    self.redraw_text()
    


                                elif self.right_click_help_box_border.collidepoint(self.mouse):
                                    self.help = True


                            elif (self.change_bg_color_red_box or self.change_bg_color_white_box or self.change_bg_color_yellow_box or self.change_bg_color_black_box):                            
                                if not (self.right_click_undo_box.collidepoint(self.mouse) or self.right_click_enter_box.collidepoint(self.mouse) or self.right_click_change_pen_color_box.collidepoint(self.mouse) or self.right_click_change_bg_color_box.collidepoint(self.mouse) or self.right_click_clear_box.collidepoint(self.mouse) or self.right_click_help_box.collidepoint(self.mouse) or self.change_bg_color_red_box.collidepoint(self.mouse) or self.change_bg_color_white_box.collidepoint(self.mouse) or self.change_bg_color_yellow_box.collidepoint(self.mouse) or self.change_bg_color_black_box.collidepoint(self.mouse)):
                                    self.mouse_down = False
                                    self.release_points[(self.mouse)] = None
                                    self.redraw_text()

                                elif self.change_bg_color_red_box.collidepoint(self.mouse):
                                    self.change_bg_color(RED)

                                elif self.change_bg_color_white_box.collidepoint(self.mouse):
                                    self.change_bg_color(WHITE)

                                elif self.change_bg_color_yellow_box.collidepoint(self.mouse):
                                    self.change_bg_color(YELLOW)

                                elif self.change_bg_color_black_box.collidepoint(self.mouse):
                                    self.change_bg_color(GREY)


                                elif self.right_click_undo_box_border.collidepoint(self.mouse):
                                    self.undo()
                                    self.right_click_box = None
                                    
                                elif self.right_click_enter_box_border.collidepoint(self.mouse):
                                    self.evaluate()
                                    self.right_click_box = None

                                    
                                elif self.right_click_change_pen_color_box_border.collidepoint(self.mouse):
                                    self.show_change_fg_color_box(
                                        self.right_click_change_pen_color_box_border.x,
                                        self.right_click_change_pen_color_box_border.y
                                    )

                                

                                elif self.right_click_change_bg_color_box_border.collidepoint(self.mouse):
                                    self.show_change_bg_color_box(
                                        self.right_click_change_bg_color_box.x,
                                        self.right_click_change_bg_color_box.y

                                    )

                                elif self.right_click_clear_box_border.collidepoint(self.mouse):
                                    self.gameWindow.fill(self.bgcolor)
                                    self.drawing = dict.fromkeys([])
                                    self.release_points = dict.fromkeys([])
                                    self.right_click_pos = None
                                    
                                    self.right_click_box = None
                                    
                                    self.right_click_undo_box = None
                                    self.right_click_enter_box = None
                                    self.right_click_change_pen_color_box = None
                                    self.right_click_change_bg_color_box = None
                                    self.right_click_clear_box = None
                                    self.right_click_help_box = None
                            
                                    self.right_click_undo_box_border = None
                                    self.right_click_enter_box_border = None
                                    self.right_click_change_pen_color_box_border = None
                                    self.right_click_change_bg_color_box_border = None
                                    self.right_click_clear_box_border = None
                                    self.right_click_help_box_border = None
                            
                                    self.right_click_undo_text = None
                                    self.right_click_enter_text = None
                                    self.right_click_change_pen_color_text = None
                                    self.right_click_change_bg_color_text = None
                                    self.right_click_clear_text = None
                                    self.right_click_help_text = None
                                    
                                    self.redraw_text()
    


                                elif self.right_click_help_box_border.collidepoint(self.mouse):
                                    self.help = True

                                
                            else:

                                if not (self.right_click_undo_box.collidepoint(self.mouse) or self.right_click_enter_box.collidepoint(self.mouse) or self.right_click_change_pen_color_box.collidepoint(self.mouse) or self.right_click_change_bg_color_box.collidepoint(self.mouse) or self.right_click_clear_box.collidepoint(self.mouse) or self.right_click_help_box.collidepoint(self.mouse)):
                                    self.mouse_down = False
                                    self.release_points[(self.mouse)] = None

                                elif self.right_click_undo_box_border.collidepoint(self.mouse):
                                    self.undo()
                                    self.right_click_box = None
                                    
                                elif self.right_click_enter_box_border.collidepoint(self.mouse):
                                    self.evaluate()
                                    self.right_click_box = None

                                    
                                elif self.right_click_change_pen_color_box_border.collidepoint(self.mouse):
                                    self.show_change_fg_color_box(
                                        self.right_click_change_pen_color_box_border.x,
                                        self.right_click_change_pen_color_box_border.y
                                    )

                                

                                elif self.right_click_change_bg_color_box_border.collidepoint(self.mouse):
                                    self.show_change_bg_color_box(
                                        self.right_click_change_bg_color_box.x,
                                        self.right_click_change_bg_color_box.y

                                    )

                                elif self.right_click_clear_box_border.collidepoint(self.mouse):
                                        self.gameWindow.fill(self.bgcolor)
                                        self.drawing = dict.fromkeys([])
                                        self.release_points = dict.fromkeys([])
                                        self.right_click_pos = None
                                        
                                        self.right_click_box = None
                                        
                                        self.right_click_undo_box = None
                                        self.right_click_enter_box = None
                                        self.right_click_change_pen_color_box = None
                                        self.right_click_change_bg_color_box = None
                                        self.right_click_clear_box = None
                                        self.right_click_help_box = None
                                
                                        self.right_click_undo_box_border = None
                                        self.right_click_enter_box_border = None
                                        self.right_click_change_pen_color_box_border = None
                                        self.right_click_change_bg_color_box_border = None
                                        self.right_click_clear_box_border = None
                                        self.right_click_help_box_border = None
                                
                                        self.right_click_undo_text = None
                                        self.right_click_enter_text = None
                                        self.right_click_change_pen_color_text = None
                                        self.right_click_change_bg_color_text = None
                                        self.right_click_clear_text = None
                                        self.right_click_help_text = None
                                        
                                        self.redraw_text()
                                elif self.right_click_help_box_border.collidepoint(self.mouse):
                                    self.help = True

                        else:
                            self.mouse_down = False
                            self.release_points[(self.mouse)] = None


                    else:
                        self.right_click(self.mouse)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL:
                        self.ctrl_pressed = True
                    self.letter_key = event.key
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.redraw_text()
                        


            if self.ctrl_pressed and self.letter_key == pygame.K_c:
                self.gameWindow.fill(self.bgcolor)
                self.drawing = dict.fromkeys([])
                self.release_points = dict.fromkeys([])
                self.right_click_undo_box = None
                self.right_click_enter_box = None
                self.right_click_change_pen_color_box = None
                self.right_click_change_bg_color_box = None
                self.right_click_clear_box = None
                self.right_click_help_box = None
        
                self.right_click_undo_box_border = None
                self.right_click_enter_box_border = None
                self.right_click_change_pen_color_box_border = None
                self.right_click_change_bg_color_box_border = None
                self.right_click_clear_box_border = None
                self.right_click_help_box_border = None
        
                self.right_click_undo_text = None
                self.right_click_enter_text = None
                self.right_click_change_pen_color_text = None
                self.right_click_change_bg_color_text = None
                self.right_click_clear_text = None
                self.right_click_help_text = None

            if self.ctrl_pressed and self.letter_key == pygame.K_z:
                self.undo()
            if self.ctrl_pressed and self.letter_key == pygame.K_RETURN:
                self.evaluate()
            if self.ctrl_pressed and self.letter_key == pygame.K_e:
                if not self.erase_on:
                    self.erase_on = True
                else:
                    self.erase_on = False

            if self.ctrl_pressed and self.letter_key == pygame.K_EQUALS:
                self.size +=1

            if self.ctrl_pressed and self.letter_key == pygame.K_MINUS:
                self.size -=1

            pygame.display.update()

            self.clock.tick(self.fps)

        if self.help:
            self.show_help_page()
            
            
        if self.exit:
            if self.localhost_url.endswith('/'):
                requests.get(f"https://{self.localhost_url}blackboard_quit")
            else:
                requests.get(f"https://{self.localhost_url}/blackboard_quit")

            pygame.quit()
            sys.exit(0)


    def draw_settings(self):
        self.gameWindow.fill(GREY)

        size = self.gameWindow.get_size()
        left_margin = size[0]//10
        right_margin = size[0]//4+45

        self.chalk = pygame.font.Font(resource_path('SqueakyChalkSound-ZG8.ttf'), size[1]//9) 
        self.firaCode = pygame.font.Font(resource_path('FiraCode-VariableFont_wght.ttf'), size[1]//18) 
        self.firaCodeLarger = pygame.font.Font(resource_path('FiraCode-VariableFont_wght.ttf'), size[1]//13) 
        self.marker = pygame.font.Font(resource_path('SmoothMarker-45d6.ttf'), size[1]//13) 

        self.back = pygame.image.load(resource_path('arrow.png'))

        heading = self.chalk.render('Controls', True, YELLOW)
        
        sizeUp = self.marker.render('Increase pen size', True, YELLOW)
        sizeDown = self.marker.render('Decrase pen size', True, YELLOW)
        undo = self.marker.render('Undo drawing', True, YELLOW)
        erase = self.marker.render('Toggle eraser', True, YELLOW)
        clear = self.marker.render('Clear board', True, YELLOW)
        enter = self.marker.render('Evaluate', True, YELLOW)

        sizeUpAns = self.firaCode.render('ctrl +', True, YELLOW)
        sizeDownAns = self.firaCode.render('ctrl -', True, YELLOW)
        undoAns = self.firaCode.render('ctrl z', True, YELLOW)
        eraseAns = self.firaCode.render('ctrl e', True, YELLOW)
        clearAns = self.firaCode.render('ctrl c', True, YELLOW)
        enterAns = self.firaCode.render('ctrl enter', True, YELLOW)


        self.headRect = pygame.Rect(0, size[1]//15, size[0], 30)

        self.sizeUpRect = pygame.Rect(0, 4*size[1]//15, size[0], 30)
        self.sizeDownRect = pygame.Rect(0, 4*size[1]//15+ size[1]//10, size[0], 30)
        self.undoRect = pygame.Rect(0, 4*size[1]//15+ 2*size[1]//10, size[0], 30)
        self.eraseRect = pygame.Rect(0, 4*size[1]//15+ 3*size[1]//10, size[0], 30)
        self.clearRect = pygame.Rect(0, 4*size[1]//15+ 4*size[1]//10, size[0], 30)
        self.enterRect = pygame.Rect(0, 4*size[1]//15+ 5*size[1]//10, size[0], 30)

        rectCenter = heading.get_rect(center=(self.headRect.center[0], self.headRect.center[1]))

        rectUp = heading.get_rect(midleft=(self.sizeUpRect.midleft[0]+left_margin, self.sizeUpRect.midleft[1]))
        rectDown = heading.get_rect(midleft=(self.sizeDownRect.midleft[0]+left_margin, self.sizeDownRect.midleft[1]))
        rectUndo = heading.get_rect(midleft=(self.undoRect.midleft[0]+left_margin, self.undoRect.midleft[1]))
        rectErase = heading.get_rect(midleft=(self.eraseRect.midleft[0]+left_margin, self.eraseRect.midleft[1]))
        rectClear = heading.get_rect(midleft=(self.clearRect.midleft[0]+left_margin, self.clearRect.midleft[1]))
        rectEnter = heading.get_rect(midleft=(self.enterRect.midleft[0]+left_margin, self.enterRect.midleft[1]))

        rectUpAns = heading.get_rect(midleft=(self.sizeUpRect.midright[0] - right_margin, self.sizeUpRect.midright[1]))
        rectDownAns = heading.get_rect(midleft=(self.sizeDownRect.midright[0] - right_margin, self.sizeDownRect.midright[1]))
        rectUndoAns = heading.get_rect(midleft=(self.undoRect.midright[0] - right_margin, self.undoRect.midright[1]))
        rectEraseAns = heading.get_rect(midleft=(self.eraseRect.midright[0] - right_margin, self.eraseRect.midright[1]))
        rectClearAns = heading.get_rect(midleft=(self.clearRect.midright[0] - right_margin, self.clearRect.midright[1]))
        rectEnterAns = heading.get_rect(midleft=(self.enterRect.midright[0] - right_margin, self.enterRect.midright[1]))
        
        self.gameWindow.blit(self.back, (5+size[0]//150,15+size[1]//150))

        self.gameWindow.blit(heading, rectCenter)

        self.gameWindow.blit(sizeUp, rectUp)
        self.gameWindow.blit(sizeDown, rectDown)
        self.gameWindow.blit(undo, rectUndo)
        self.gameWindow.blit(erase, rectErase)
        self.gameWindow.blit(clear, rectClear)
        self.gameWindow.blit(enter, rectEnter)

        self.gameWindow.blit(sizeUpAns, rectUpAns)
        self.gameWindow.blit(sizeDownAns, rectDownAns)
        self.gameWindow.blit(undoAns, rectUndoAns)
        self.gameWindow.blit(eraseAns, rectEraseAns)
        self.gameWindow.blit(clearAns, rectClearAns)
        self.gameWindow.blit(enterAns, rectEnterAns)


    def show_help_page(self):
        self.draw_settings()
        while not self.exit and self.help:
            self.mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.help = False

                if event.type  == pygame.QUIT:
                    self.exit = True

                if event.type == pygame.VIDEORESIZE:
                    self.draw_settings()

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.back.get_rect().collidepoint(self.mouse):
                        if event.button != 3:
                            self.help = False

            pygame.display.update()
            self.clock.tick(self.fps)

        if not self.help:
            self.mainBoard()

        if self.exit:
            if self.localhost_url.endswith('/'):
                requests.get(f"https://{self.localhost_url}blackboard_quit")
            else:
                requests.get(f"https://{self.localhost_url}/blackboard_quit")

            pygame.quit()
            sys.exit(0)



    def run(self):
        #try:
        self.mainBoard()
        #except Exception as e:
            #print(e)
    

if __name__ == '__main__':
    Blackboard().run()
