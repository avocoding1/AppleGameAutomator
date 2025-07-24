import customtkinter
import CTkMessagebox
import os
import sys
from event import *

'''
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.asbpath(".")

    return os.path.join(base_path, relative_path)
'''

class App:
    def __init__(self):
        self.window = customtkinter.CTk()
        self.window.geometry("500x180+0+540")
        self.window.resizable(False, False)
        self.window.title("사과 게임 자동화 프로그램 v1.0 (by avocoding)")

        self.description = customtkinter.CTkLabel(self.window, text="사과 게임(フルーツボックス) 자동화 프로그램 v1.0입니다.")
        self.description.place(x=20, y=10)

        self.keys = customtkinter.CTkLabel(self.window, text="[매크로 실행 방법]\n- 게임 시작 버튼을 눌러 사과들이 모두 보이게 설정한 후, 아래 버튼 또는 F8을 누르면,\n잠시 후 매크로가 시작됩니다.", justify="left")
        self.keys.place(x=20, y=40)

        self.button = customtkinter.CTkButton(self.window, text="매크로 실행하기", command=self.run, width=460, height=40)
        self.button.place(x=20, y=110)

        self.window.bind("<F8>", self.run)

        self.window.mainloop()

    def run(self, event=None):
        try:
            import run
        except TaskDone:
            CTkMessagebox.CTkMessagebox(self.window, title="알림", message="제거할 수 있는 사과를 모두 제거하였습니다.", icon="check")
        except:
            CTkMessagebox.CTkMessagebox(self.window, title="애러", message="실행 중 오류가 발생했습니다. 사과와 숫자들이 화면에 정확히 띄워져 있는지 확인해 주세요.", icon="cancel")

if __name__ == "__main__":
    app = App()