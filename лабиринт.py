import play



w = play.screen.width/2
h = play.screen.height/2
wall_1 = play.new_box(color='black', x=0, y=-190, width=100, height=10)
wall_2 = play.new_box(color='black', x=-45, y=-140, width=10, height=100)
wall_3 = play.new_box(color='black', x=-100, y=-120, width=10, height=270)
wall_4 = play.new_box(color='black', x=-30, y=-250, width=130, height=10)
wall_5 = play.new_box(color='black', x=-30, y=-50, width=130, height=10)
wall_6 = play.new_box(color='black', x=200, y=50, width=130, height=10)
wall_7 = play.new_box(color='black', x=-200, y=50, width=130, height=10)
finish = play.new_text(words='Финиш', x=0, y=280)
player = play.new_circle(color='green', x=0, y=-280, radius=20,border_color='dark green', border_width=3)


frames = 48
step = 10
@play.when_program_starts



def start():
    player.start_physics(bounciness=0.2)
    wall_1.start_physics(can_move=False)
    wall_2.start_physics(can_move=False)
    wall_3.start_physics(can_move=False)
    wall_4.start_physics(can_move=False)
    wall_5.start_physics(can_move=False)
    wall_6.start_physics(can_move=True)
    wall_7.start_physics(can_move=True)
@play.repeat_forever
def do():
    if play.key_is_pressed('w'):
        player.y = player.y + 5
    if play.key_is_pressed('a'):
        player.x = player.x - 5
    if play.key_is_pressed('s'):
        player.y = player.y - 5
    if play.key_is_pressed('d'):
        player.x = player.x + 5


    if abs(player.y) >= h and player.y > 0:
        player.y = player.y - 5
    if abs(player.y) >= h and player.y < 0:
        player.y = player.y + 5
    if abs(player.x) >= w and player.x > 0:
        player.x = player.x - 5
    if abs(player.x) >= w and player.x < 0:
        player.x = player.x + 5


play.start_program()