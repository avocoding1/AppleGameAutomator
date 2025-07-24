import pyautogui
import copy
import event

NUM_ROWS = 10
NUM_COLS = 17

class Apple:
    def __init__(self, num, x, y, wid, hei):
        self.num = num
        self.x = x
        self.y = y
        self.endx = x + wid
        self.endy = y + hei

def build_prefix_sum(grid):
    rows, cols = len(grid), len(grid[0])
    prefix = [[0] * (cols + 1) for _ in range(rows + 1)]

    for y in range(1, rows + 1):
        for x in range(1, cols + 1):
            prefix[y][x] = (
                grid[y - 1][x - 1].num
                + prefix[y - 1][x]
                + prefix[y][x - 1]
                - prefix[y - 1][x - 1]
            )
    return prefix

def calc_sum(prefix, x, y, w, h):
    x1, y1 = x, y
    x2, y2 = x + w - 1, y + h - 1
    return (
        prefix[y2 + 1][x2 + 1]
        - prefix[y1][x2 + 1]
        - prefix[y2 + 1][x1]
        + prefix[y1][x1]
    )

apple_list = []

for num in range(1, 10):
    positions = pyautogui.locateAllOnScreen(f'images/{num}.png', confidence=0.95)
    for pos in positions:
        apple_list.append(Apple(num, pos.left, pos.top, pos.width, pos.height))

i = 0
while i < len(apple_list):
    j = i + 1
    while j < len(apple_list):
        if abs(apple_list[i].x - apple_list[j].x) < 10 and abs(apple_list[i].y - apple_list[j].y) < 10:
            del apple_list[j]
        else:
            j += 1
    i += 1

apple_list.sort(key=lambda a: (a.y, a.x))

grid = []
y_threshold = 20
x_threshold = 20

current_row = []
previous_y = apple_list[0].y

for apple in apple_list:
    if abs(apple.y - previous_y) >= y_threshold:
        grid.append(current_row)
        current_row = []
        previous_y = apple.y
    current_row.append(apple)

grid.append(current_row)

for row in grid:
    row.sort(key=lambda a: a.x)

'''
print("\n사과 배치:")
for i, row in enumerate(grid):
    print(f"Row {i}: ", [f"숫자 {apple.num} ({apple.x}, {apple.y})" for apple in row])
'''

def search_for_10_and_drag():
    global no_more_valid_10s, done
    prefix = build_prefix_sum(grid)
    sum_10_rect = []
    for y in range(NUM_ROWS):
        for x in range(NUM_COLS):
            for w in range(1, NUM_COLS - x + 1):
                for h in range(1, NUM_ROWS - y + 1):
                    current_sum = calc_sum(prefix, x, y, w, h)
                    if current_sum == 10:
                        # 저장하는 리스트: [제거 면적, x, y, w, h, 미래 후보 개수(초기 0)]
                        sum_10_rect.append([w * h, x, y, w, h, 0])
                    elif current_sum > 10:
                        break

    for idx, rect in enumerate(sum_10_rect):
        possible_rects = 0
        temp_grid = copy.deepcopy(grid)
        rx, ry, rw, rh = rect[1], rect[2], rect[3], rect[4]
        for i in range(ry, ry + rh):
            for j in range(rx, rx + rw):
                temp_grid[i][j].num = 0
        temp_prefix = build_prefix_sum(temp_grid)
        for y in range(NUM_ROWS):
            for x in range(NUM_COLS):
                for w in range(1, NUM_COLS - x + 1):
                    for h in range(1, NUM_ROWS - y + 1):
                        temp_sum = calc_sum(temp_prefix, x, y, w, h)
                        if temp_sum == 10:
                            possible_rects += 1
                        elif temp_sum > 10:
                            break
        sum_10_rect[idx][5] = possible_rects

    if len(sum_10_rect) == 0:
        done = True

    valid_candidates = []
    for rect in sum_10_rect:
        area, x, y, w, h, future = rect
        zeros = 0
        if grid[y][x].num == 0:
            zeros += 1
        if grid[y][x + w - 1].num == 0:
            zeros += 1
        if grid[y + h - 1][x].num == 0:
            zeros += 1
        if grid[y + h - 1][x + w - 1].num == 0:
            zeros += 1
        if grid[y][x].num and grid[y + h - 1][x + w - 1] != 0 or grid[y][x + w - 1].num and grid[y + h - 1][x] != 0:
            zeros = 0
        if zeros < 2:
            valid_candidates.append(rect)
    
    if len(valid_candidates) > 0:
        sum_10_rect = valid_candidates
    elif len(valid_candidates) == 0:
        raise event.TaskDone

    sum_10_rect.sort(key=lambda x: (x[5] / x[0]), reverse=True)

    best_candidate = sum_10_rect[0]
    worst_candidate = sum_10_rect[-1]
    #print(f"Best candidate ratio (future/area): {best_candidate[5] / best_candidate[0]:.2f} (future: {best_candidate[5]}, area: {best_candidate[0]})")
    #print(f"Worst candidate ratio: {worst_candidate[5] / worst_candidate[0]:.2f} (future: {worst_candidate[5]}, area: {worst_candidate[0]})")

    start_apple = grid[best_candidate[2]][best_candidate[1]]
    end_apple = grid[best_candidate[2] + best_candidate[4] - 1][best_candidate[1] + best_candidate[3] - 1]

    pyautogui.moveTo(start_apple.x - 15, start_apple.y - 15)
    pyautogui.mouseDown()
    pyautogui.moveTo(end_apple.endx + 17, end_apple.endy + 17, duration=0.01)
    pyautogui.moveTo(end_apple.endx + 18, end_apple.endy + 18, duration=0.01)
    pyautogui.mouseUp()
    _, x, y, w, h, _ = best_candidate
    
    for i in range(y, y + h):
        for j in range(x, x + w):
            grid[i][j].num = 0

while True:
    search_for_10_and_drag()