# keyevent指的是android对应的keycode，
# 比如home键的keycode = 3，back键的keycode = 4 KEYCODE_ENTER=66; KEYCODE_DEL = 67

# class Config:
# Android按键事件
KEY = {
    'BACK_KEYEVENT': '4',
    'HOME_KEYEVENT': '3',
    'KEYCODE_ENTER': '66'
}

# 在终端中输入adb shell input swipe 540 1300 540 500 100   从坐标点（540，1300）用100ms滑动到（540，500）坐标点。

# 1. 处于首页
# 2. 点击搜索按钮
# 3. 输入搜索的内容
# 3. 点击搜一搜
# 3. 点击公众号
# 3. 点击 ‘真正的公众号’
# 4. 随机找一篇文章点进去
# 5. 点击叉叉
# 6. 点击返回
# 6. 点击返回
# 6. 点击返回  现在你处于首页了
max_width = 300

# HOME_SEARCH_BUTTON = {
#     'x': [460, 550],
#     'y': [40, 110]
# }

# # FIXED
# TOP_BACK_BUTTON_POS = {
#     'x': [10, 50],
#     'y': [50, 100]
# }

# # FIXED
# TOP_DEL_BUTTON_POS = {
#     'x': [595, 605],
#     'y': [65, 85]
# }

# # FIXED
# SOU_YI_SOU = {
#     'x': [20, 280],
#     'y': [130, 200]
# }

# # FIXED
# GZH_TAB = {
#     'x': [110, 190],
#     'y': [140, 180]
# }

# # FIXED
# GZH_ENTRY = {
#     'x': [20, 280],
#     'y': [260, 400]
# }

# # FIXED
# ENTER_INTO_ARTICLE = {
#     'x': [50, 550],
#     'y': [580, 700]
# }


HOME_SEARCH_BUTTON = {
    'x': [500, 510],
    'y': [70, 75]
}

# FIXED
TOP_BACK_BUTTON_POS = {
    'x': [20, 25],
    'y': [70, 80]
}

# FIXED
TOP_DEL_BUTTON_POS = {
    'x': [595, 605],
    'y': [65, 85]
}

# FIXED
SOU_YI_SOU = {
    'x': [140, 150],
    'y': [200, 205]
}

# FIXED
GZH_TAB = {
    'x': [160, 165],
    'y': [160, 170]
}

# FIXED
GZH_ENTRY = {
    'x': [200, 210],
    'y': [350, 360]
}

# FIXED
ENTER_INTO_ARTICLE = {
    'x': [340, 350],
    'y': [758, 762]
}

MORE_BUTTON = {
    'x': [585, 857],
    'y': [80, 85]
}

REFRESH_BUTTON = {
    'x': [220, 230],
    'y': [930, 940]
}
