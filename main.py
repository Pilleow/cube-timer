import pygame
import json
import random

from classes import button, timer, slider

RES = (1280, 720)
FPS = 90

pygame.init()

''' LOADING '''
shuffle_font = pygame.font.Font("fonts/Poppins-Regular.ttf", 32)
timer_font = pygame.font.Font("fonts/Poppins-Regular.ttf", 160)
misc_font = pygame.font.Font("fonts/Poppins-Regular.ttf", 56)
btn_font = pygame.font.Font("fonts/Poppins-Light.ttf", 48)

with open('data/data.json', mode='r', encoding='utf') as f:
    data = json.load(f)
with open('data/config.json', mode='r', encoding='utf') as f:
    config = json.load(f)

''' STUFF '''
display = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

# main menu // mode = 0
timer = timer.Timer(timer_font)
p_record_lbl = misc_font.render("PR: " + data['highscore'], 0, (237, 224, 212))
delete_btn = None
dnf_btn = None
plus_two_btn = None

# settings // mode = 1
shuffle_size_lbl = btn_font.render(
    f"Shuffle length  -  {config['cfg']['shuffle_size']}",
    0, (255, 244, 232)
)
shuffle_size_sldr = slider.Slider((710, 160), (400, 50), 0.5)

# other
ready = False
finished = False
lmb_down = False

buttons_0 = []
buttons_1 = []
buttons_2 = []

for btn in config['btns']['0']:
    buttons_0.append(button.Button(btn[0], btn[1], btn[2], btn[3], btn[4], btn[5], btn_font))
for btn in config['btns']['1']:
    buttons_1.append(button.Button(btn[0], btn[1], btn[2], btn[3], btn[4], btn[5], btn_font))
for btn in config['btns']['2']:
    buttons_2.append(button.Button(btn[0], btn[1], btn[2], btn[3], btn[4], btn[5], btn_font))

mode = 0
# 0 = main menu (timer)
# 1 = settings
# 2 = statistics

''' FUNCTIONS '''
def new_shuffle():
    global shuffle_txt
    shuffle_txt = ', '.join(generate_shuffle(config['cfg']['shuffle_size']))
    buttons_0[-1].set_text(shuffle_txt)
    buttons_0[-1].set_pos((
        (RES[0] - shuffle_font.size(shuffle_txt)[0])//2 - 20, 430
    ))
    buttons_0[-1].clicked = False


def time_str_to_int(time: str, divisor: str = ":"):
    return int(''.join(time.split(divisor)))


def generate_shuffle(size: int = 20) -> list:
    moves = ['U', 'B', 'L', 'R', 'D', 'F']
    shuffle = []
    prev_move = None

    for i in range(size):
        moves_copy = moves.copy()
        if prev_move:
            moves_copy.remove(prev_move)
        move = random.choice(moves_copy)
        mult = random.choice(['', '', '2'])
        inv = random.choice(['','\''])
        shuffle.append(f"{mult}{move}{inv}")
        prev_move = move

    return shuffle

shuffle_txt = ', '.join(generate_shuffle(config['cfg']['shuffle_size']))
buttons_0.append(button.Button(
    ((RES[0] - shuffle_font.size(shuffle_txt)[0])//2 - 20, 430),
    (20, 10),
    shuffle_txt,
    (237, 224, 212),
    (176, 137, 104),
    (147, 109, 77),
    shuffle_font
))


def save_time(timer: object):
    parsed_time = f"{timer.value['h']}:{timer.value['m']}:{timer.value['s']}:{timer.value['ms']}"
    data['times'].append(parsed_time)
    if data['highscore'] == "N/A" or time_str_to_int(parsed_time) < time_str_to_int(data['highscore']):
        data['highscore'] = parsed_time

    with open('data/data.json', mode='w', encoding='utf') as f:
        json.dump(data, f)


def draw_all(display: object):
    if timer.active:
        bg_color = (221, 184, 146)
    elif ready:
        bg_color = (185, 150, 121)
    elif finished:
        bg_color = (216, 173, 131)
    else:
        bg_color = (176, 137, 104)
    display.fill(bg_color)

    if mode == 0:
        timer.render(display, (
            RES[0]//2 - timer_font.size('0')[0]*5, 
            (RES[1] - timer_font.size('0')[1])//2 - 20
        ))
        if not finished and not ready and not timer.active:
            for btn in buttons_0:
                btn.render(display, btn.is_over(mouse_pos))

            p_record_size = misc_font.size("PR: " + data['highscore'])
            pygame.draw.rect(display, (160, 119, 84), (
                (RES[0] - p_record_size[0])//2 - 20,
                620,
                p_record_size[0] + 40,
                p_record_size[1] + 20 
            ))
            display.blit(p_record_lbl, (
                (RES[0] - p_record_size[0])//2, 
                630
            ))

    elif mode == 1:
        for btn in buttons_1:
            btn.render(display, btn.is_over(mouse_pos))
        display.blit(shuffle_size_lbl, (200, 150))
        shuffle_size_sldr.render(display)

    elif mode == 2:
        for btn in buttons_2:
            btn.render(display, btn.is_over(mouse_pos))

    pygame.display.update()


''' MAINLOOP '''
run = True
while run:
    clock.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()

    ''' SLIDER ACTION '''
    if lmb_down and mode == 1:
        if shuffle_size_sldr.is_over(mouse_pos):
            shuffle_size_sldr.set_value( # (m.x - sldr.x) / sldr.width 
                (mouse_pos[0] - shuffle_size_sldr.rect[0]) / shuffle_size_sldr.rect[2], 1
            )
            config['cfg']['shuffle_size'] = int(15 + 10 * shuffle_size_sldr.value)
            shuffle_size_lbl = btn_font.render(
                f"Shuffle length  -  {config['cfg']['shuffle_size']}",
                0, (255, 244, 232)
            )

    ''' BUTTON ACTION '''
    if mode == 0:
        active_buttons = buttons_0
        if buttons_0[0].clicked: 
            mode = 1
        elif buttons_0[1].clicked:
            mode = 2
        elif buttons_0[-1].clicked:
            new_shuffle()

    elif mode == 1:
        active_buttons = buttons_1
        if buttons_1[0].clicked:
            mode = 0
            with open('data/config.json', mode='w', encoding='utf') as f:
                json.dump(config, f)

    elif mode == 2:
        active_buttons = buttons_2
        if buttons_2[0].clicked:
            mode = 0

    ''' EVENT HANDLING '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and mode == 0:
                if timer.active:
                    finished = True
                    timer.active = False
                elif finished:
                    save_time(timer)
                    timer.reset()
                    finished = False
                    p_record_lbl = misc_font.render(
                        "PR: " + data['highscore'], 
                        0, (237, 224, 212)
                    )
                    new_shuffle()
                else:
                    ready = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and mode == 0:
                if not finished and ready:
                    ready = False
                    timer.active = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(mouse_pos)
            lmb_down = True
            for btn in active_buttons:
                if btn.is_over(mouse_pos):
                    btn.clicked = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            lmb_down = False
            for btn in buttons_0 + buttons_1 + buttons_2:
                btn.clicked = False

    ''' THING UPDATES '''
    if timer.active:
        timer.increment_ms(clock.get_time())
    draw_all(display)


pygame.quit()
