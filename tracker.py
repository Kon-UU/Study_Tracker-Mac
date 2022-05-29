# Study Tracker
import platform
import time
from pynput import keyboard
import os

KERNAL_NAME = platform.system()

if KERNAL_NAME == "Windows":
    from win10toast import ToastNotifier

#Reference : pynput 예제 코드 https://github.com/moses-palmer/pynput/issues/20
# The key combination to check
COMBINATION_S = {keyboard.Key.cmd, keyboard.Key.alt, keyboard.KeyCode.from_char('“')}
COMBINATION_SK = {keyboard.Key.cmd, keyboard.Key.alt, keyboard.KeyCode.from_char('[')}

COMBINATION_E = {keyboard.Key.cmd, keyboard.Key.alt, keyboard.KeyCode.from_char('‘')}
COMBINATION_EK = {keyboard.Key.cmd, keyboard.Key.alt, keyboard.KeyCode.from_char(']')}
cur_state = 0
total_t = 0

# The currently active modifiers
current = set()

def on_press(key):
    global cur_state
    global total_t
    if cur_state == 0:
        if key in (COMBINATION_S):
            current.add(key)
            if all(k in current for k in (COMBINATION_S or COMBINATION_SK)):
                # print('Start Signal Received!')
                cur_state = 1

                print(get_time(), end=' ~ ', flush=True)
                global st
                st = time.time()
                notification("공부 시작")
    if cur_state == 1:
        if key in (COMBINATION_E):
            current.add(key)
            if all(k in current for k in (COMBINATION_E or COMBINATION_EK)):
                # print('Stop Signal Received!')
                cur_state = 0

                print(get_time(), end=' ', flush=True)
                ed = time.time()
                total_t += int(ed - st)
                print("공부 시간 :" ,get_length(int(ed - st)), "세션 총합 :", get_length(total_t))
                notification(str("공부 시간 : " + get_length(int(ed - st)) + " 세션 총합 : " + get_length(total_t)))

def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass

def get_time():
    h_value = time.localtime().tm_hour
    m_value = time.localtime().tm_min
    if h_value > 12:
        rt_value = f"오후 {h_value - 12}시 {m_value}분"
    else:
        rt_value = f"오전 {h_value}시 {m_value}분"
    return rt_value

def get_length(t):
    if t > 3600:
        rt_value = f"{int(t // 3600)}시간 {int((t % 3600) // 60)}분 {int(t % 60)}초"
    elif t > 60:
        rt_value = f"{int(t // 60)}분 {int(t % 60)}초"
    else:
        rt_value = f"{int(t % 60)}초"
    
    return rt_value

def notification(a):
    title = "Study Tracker"
    message = a
    if KERNAL_NAME == "Darwin":
        command = f'''
        osascript -e 'tell app "Finder" to display notification "{message}" with title "{title}"'
        '''
        os.system(command)
    elif KERNAL_NAME == "Windows":
        toaster = ToastNotifier()
        toaster.show_toast(f"{title}",
            f"{message}",
            duration=10)
    
        
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
