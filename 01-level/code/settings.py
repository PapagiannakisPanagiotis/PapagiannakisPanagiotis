# game setup
WIDTH = 1280
HEIGTH = 720
FPS = 60
TILESIZE = 64 # for every x we add 64 at the x axis
HITBOX_OFFSET = {
    'player': -26,
    'object': -40,
    'grass': -10,
    'invisible': 0}


# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = '../graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR ='#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# weapons
weapon_data = {
    'sword': {'cooldown': 800, 'damage': 15,'graphic':'../graphics/weapons/sword/full.png'},
    'lance': {'cooldown': 1200, 'damage': 15,'graphic':'../graphics/weapons/lance/full.png'},
    'axe': {'cooldown': 1000, 'damage': 20, 'graphic':'../graphics/weapons/axe/full.png'},
    'rapier':{'cooldown': 100, 'damage': 2, 'graphic':'../graphics/weapons/rapier/full.png'},
    'sai':{'cooldown': 600, 'damage': 10, 'graphic':'../graphics/weapons/sai/full.png'}}

# magic
magic_data = {
    'flame': {'strength': 5, 'cost': 20, 'graphic':'../graphics/particles/flame/fire.png'},
    'heal':{'strength':10, 'cost': 10, 'graphic': '../graphics/particles/heal/heal.png'}
}

# enemy
monster_data = {
    'squid': {'health': 100,'exp':200,'damage':150,'attack_type': 'slash', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 200, 'notice_radius': 200},
    'raccoon': {'health': 1000,'exp':500,'damage':400,'attack_type': 'claw',  'attack_sound':'../audio/attack/claw.wav','speed': 2, 'resistance': 2, 'attack_radius': 200, 'notice_radius': 300},
    'spirit': {'health': 20,'exp':80,'damage':700,'attack_type': 'thunder', 'attack_sound':'../audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 300},
    'bamboo': {'health': 200,'exp':50,'damage':80,'attack_type': 'leaf_attack', 'attack_sound':'../audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 350}}