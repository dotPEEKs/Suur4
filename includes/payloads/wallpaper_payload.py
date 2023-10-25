import os
import sys
import time

from Suura import to_nt_path
import multiprocessing
from Suura import get_assets_data
from Suura.includes.util import SetBackground
class WallPaperPayload:
    def __init__(self):
        self.main_data_path = to_nt_path("data/images/wallpapers")
        print(get_assets_data(self.main_data_path),os.path.exists(get_assets_data(self.main_data_path)))
        print(os.path.dirname(__file__),os.path.exists(__file__))
        self.daemon = False
        self.data = [get_assets_data(self.main_data_path,x) for x in os.listdir(get_assets_data(self.main_data_path))]
        self.opt = False
    def change_it(self):
        while self.opt:
            for backgrounds in self.data:
                if not os.path.exists(backgrounds):
                    del self.data[self.data.index(backgrounds)]
                handler = SetBackground(backgrounds)
                handler.set_bg()
                time.sleep(3)
            time.sleep(0.5)
    def start(self):
        self.opt = True
        self.thr = multiprocessing.Process(target=self.change_it)
        self.thr.start()
    def daemoned_thread(self,value: bool):
        """
        daemonlu thread yani programın çöktüğünde veya kapanırsa eğer daemon true olarak 
        ayarlandıysa programın tamamen kapanmasına engel olmayacak default:değer false 
        ise program şarkının bitmesini bekleyecektir yani hiçbir zaman 
        """
        if isinstance(value,bool):  
            self.daemon = value
    def stop(self):
        self.opt = False
if __name__ == "__main__":
    
    print(__name__)
    t = WallPaperPayload()
    t.start()