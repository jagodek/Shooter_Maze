from game_params import win_width, map_width, win_height, map_height


# returns location on screen based on location of player and location of self
def location_on_screen(x_player, y_player, x_self, y_self):
    if x_player < win_width / 2:
        x = x_self
    elif x_player > map_width - win_width / 2:
        x = win_width - (map_width - x_self)
    else:
        x = win_width / 2 - (x_player - x_self)

    if y_player < win_height / 2:
        y = y_self
    elif y_player > map_height - win_height / 2:
        y = win_height - (map_height - y_self)
    else:
        y = win_height / 2 - (y_player - y_self)
    return x, y


# location on map based on location of player and self position on screen
def location_on_map(x_player, y_player, x_self, y_self):
    if x_player < win_width / 2:
        x = x_self
    elif x_player > map_width - win_width / 2:
        x = x_self + map_width - win_width
    else:
        x = x_self - win_width / 2 + x_player

    if y_player < win_height / 2:
        y = y_self
    elif y_player > map_height - win_height / 2:
        y = y_self + map_height - win_height
    else:
        y = y_self - win_height / 2 + y_player

    return x, y
