from os import mkdir
#from queue import Queue
from threading import Thread
from zipfile import ZipFile
from pyray import *
from raylib import *
from time import sleep
from enum import Enum
import requests
from pathlib import Path

class ProgramState(Enum):
    MAIN = 1,
    DOWNLOAD = 2,
    UPLOAD = 3,
    DOWNLOADING = 4,
    UPLOADING = 5

class WorkerState(Enum):
    IDLE = 1,
    DOWNLOADING = 2,
    UPDATING = 3

# control variables
downloadPressed = False
uploadPressed = False
downloading = False
uploading = False
vscodedownloadfolder = ffi.new("char[32]")
pointer = ffi.addressof(vscodedownloadfolder)
# = ffi.new("char[32]", b" "*32)
#vscodedownloadfolder = ffi.new("char *", allocate)
#vscodedownloadfolder = ""

#queue = Queue()
#progressQueue = Queue()

'''
def download():
    while True:
        #global downloadPressed
        #if downloadPressed:
        #    print("download")
        #    downloadPressed = False
        sleep(0.1)

def upload():
    while True:
        #global uploadPressed
        #if uploadPressed:
        #    print("upload")
        #    uploadPressed = False
        sleep(0.1)

downloadthread = Thread(target=download, daemon=True)
downloadthread.start()
downloadthread = Thread(target=upload, daemon=True)
downloadthread.start()
'''

class Worker(Thread):
    VSCODE_URL = "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-archive"
    
    def __init__(self):
        Thread.__init__(self)

    def download_file(url: str, output_file: Path):
        # NOTE the stream=True parameter below
        with requests.get(url, stream=True) as r:
            if r.status_code != 200:
                print("problem downloading")
            r.raise_for_status()
            #with open(output_file, 'wb') as f:
            with output_file.open('wb') as f:
                for chunk in r.iter_content(chunk_size=4096): 
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    #if chunk: 
                    f.write(chunk)

    def mkdir(dirname):
        Path(dirname).mkdir(parents=True, exist_ok=False)

    def unzip(filename: Path, dirname: Path):
        with ZipFile(filename) as f:
            f.extractall(dirname)

    def makeDataDirectories(dirname):
        datadir = Path(dirname).joinpath("data")
        tmpdir = datadir.joinpath("tmp")
        mkdir(datadir)
        mkdir(tmpdir)

    def downloadsDirectory():
        homedirectory = Path.home()
        downloads = homedirectory.joinpath("Downloads")
        return downloads

    def download(self):
        #global vscodedownloadfolder        
        print("downloading")
        print(ffi.string(vscodedownloadfolder))

    def upload(self):
        print("uploading")

    def run(self):
        global programState
        while True:
            if programState == ProgramState.DOWNLOADING:
                self.download()
                programState = ProgramState.MAIN
            elif programState == ProgramState.UPLOADING:
                self.upload()
                programState = ProgramState.MAIN
            sleep(0.1)       

programState = ProgramState.MAIN
worker = Worker()
worker.daemon = True
worker.start()

init_window(800, 550, "VSCode Portable Downloader")
set_target_fps(20)

defaultfont = get_font_default()
headingfont = load_font("fonts/WhiteRabbit.otf")
font = load_font_ex("fonts/OfficeCodePro-Regular.ttf",48, None, 0)
fontsmall = load_font_ex("fonts/SourceCodePro-Regular.ttf",16, None, 0)
nicefont = load_font_ex("fonts/inter/InterVariable.ttf", 36, None, 0)
#defaultfont = get_font_default()
gui_set_style(BUTTON, TEXT_ALIGNMENT_VERTICAL, TEXT_ALIGN_BOTTOM)



while not window_should_close():
    begin_drawing()
    clear_background(WHITE)
    
    match programState:
        case ProgramState.MAIN:
            draw_text_ex(headingfont, "VSCode Portable Downloader", (50, 50), 36, 0, PURPLE)
            gui_set_font(font)   
            gui_set_style(DEFAULT, TEXT_SIZE, 48)
         
            if gui_button(Rectangle(100, 150, 600,100), "Download VSCode Portable"):
                programState = ProgramState.DOWNLOAD
            if gui_button(Rectangle(100, 300, 600,100), "Update VSCode Portable"):
                 programState = ProgramState.UPLOAD
        case ProgramState.DOWNLOAD:
            gui_set_font(headingfont)
            gui_set_style(DEFAULT, TEXT_SIZE, 48)
            draw_text_ex(headingfont, "Download VSCode Portable", (50, 50), 36, 0, PURPLE)

            gui_set_font(nicefont)
            gui_set_style(DEFAULT, TEXT_SIZE, 36)
            gui_label(Rectangle(50, 100, 300, 200), "Folder Name")

            gui_set_font(nicefont)
            gui_set_style(DEFAULT, TEXT_SIZE, 36)            
            
            gui_text_box(Rectangle(300,150,400,100), ffi.cast("char *", pointer), 20, True)

            gui_set_font(font)
            gui_set_style(DEFAULT, TEXT_SIZE, 48)
            if gui_button(Rectangle(50, 350, 650,100), "Download"):
                programState = ProgramState.DOWNLOADING

        case ProgramState.UPLOAD:
            pass
    end_drawing()
close_window()

