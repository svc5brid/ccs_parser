import xml.etree.ElementTree as ET
import os
from tkinter import filedialog, messagebox
import re

class CcsManager:
    def __init__(self, path: str) -> None:
        """Analyzer for ccs file

        Args:
            path (str): ccs file path

        Raises:
            FileNotFoundError: Raise if not found.
        """
        if not os.path.exists(path):
            raise FileNotFoundError("ファイルがないので無理です")
        tree = ET.parse(path)
        self.root = tree.getroot()
        self.check_fileformat()
        self.select_track()
        pass
    def get_groups(self) -> str:
        return [group for group in self.root.find("Sequence").find("Scene").find("Groups").findall("Group") if group.attrib["Category"] == "SingerSong"]
    def select_track(self):
        """chose and set track id
        """
        groups: list[ET.Element] = self.get_groups()
        self.trackid = ""
        while not self.trackid:
            print("トラックを選択してください。")
            ui = input("\n".join([f"[{str(v)}]"+i.attrib["Name"]+ "(" +  i.attrib["Id"] + ")" for v, i in enumerate(groups)]) + "\n>> ")
            if not re.match(r"\d+", ui):
                print("正しい値を入力してください。")
                continue
            try:
                self.trackid = groups[int(ui)].attrib["Id"]
            except IndexError:
                print("範囲外です")
                print("終了するにはCtrl+C")

    def check_fileformat(self):
        """Not implemented
        """
        notes = self.root.find("Sequence").find("Scene").find("Units").find("Unit").find("Song").find("Score").findall("Note")
        if notes:
            # なんとかしてくれ
            pass
            # input("ファイルフォーマットがよくないみたいです。")
            # exit()
    def find_unit(self) -> list[ET.Element]:
        unit = [unit for unit in self.root.find("Sequence").find("Scene").find("Units").findall("Unit") if unit.attrib["Group"] == self.trackid]

        if len(unit) != 1:
            raise Exception("みつかりませんでした。")
        return unit

    def output_lyrics(self, path_output: str):
        unit = self.find_unit()

        notes = unit[0].find("Song").find("Score").findall("Note")
        diff_m1 = {}
        with open(path_output, "w", encoding="utf-8") as f:
            for i in notes:
                if diff_m1.get("Clock"):
                    # ここで、長さとclockの関係を見て、続いているなら改行をしない
                    diff = float(i.get("Clock")) - float(diff_m1.get("Clock"))
                    duration = float(diff_m1.get("Duration"))
                    # print("----")
                    # print("1つ前ノートとの間隔", diff)
                    # print("1つ前ノートの長さ", duration)
                    # print("----")
                    if diff != duration:
                        # print("改行。")
                        f.write("\n")
                    pass
                    f.write(i.get("Lyric"))
                diff_m1 = i

allow_extensions = [
    ".ccs",
    # ".xml"
]

def main():
    path: str
    candidates = [dir for dir in os.listdir() if os.path.isfile(dir) and os.path.splitext(dir)[-1] in allow_extensions]
    if len(candidates) == 1:
        path = candidates[0]
    else:
        path = filedialog.askopenfilename( filetypes=[("cssファイル", "*.ccs"), ("*すべてのファイル" ,"*")])
        if not path:
            print("ファイルが選択されませんでした。")
            input("何かキーを押してきぃぃ！！！")
            exit()
    path_splitted = os.path.splitext(os.path.basename(path))
    file, _ = path_splitted[-2], path_splitted[-1]
    ccs_manager = CcsManager(path)
    ccs_manager.output_lyrics(file + ".txt")
    pass

if __name__ == "__main__":
    main()