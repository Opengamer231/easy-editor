from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QFileDialog
import os
from PIL import Image, ImageOps, ImageFilter
from PyQt5.QtGui import QPixmap

workdir = ''

class ImageProcessor():
    def __init__(self):
        self.filename = None
        self.image = None
        self.dir = None
        self.save_dir = 'Modified/'
    
    def loadImage(self, filename):
        self.filename = filename
        self.dir = workdir
        image_path = os.path.join(self.dir, self.filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        pixmapimage = QPixmap(path) 
        label_width, label_height = img_view.width(), img_view.height() 
        scaled_pixmap = pixmapimage.scaled(label_width, label_height, Qt.KeepAspectRatio) 
        img_view.setPixmap(scaled_pixmap) 
        img_view.setVisible(True)

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_bw(self):
        self.image = ImageOps.grayscale(self.image)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)        

    def do_left(self):
        self.image = self.image.rotate(270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)        

    def do_right(self):
        self.image = self.image.rotate(90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_mirror(self):
        self.image = ImageOps.mirror(self.image)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)        
            
    def do_sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path) 

    def do_blur(self):
        self.image = self.image.filter(ImageFilter.BoxBlur(0.25))
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)        



workimage = ImageProcessor()        

def showChosenImage():
    if img_folder.currentRow() >= 0:
        filename = img_folder.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, filename)
        workimage.showImage(image_path)



def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
                break    
    return result

def showFilenameList():
    chooseWorkdir()
    extensions = ['.png','.jpg','.jpeg','.gif','.bmp']
    files = os.listdir(workdir)
    files = filter(files, extensions)
    img_folder.clear()
    img_folder.addItems(files)


app = QApplication([])
window = QWidget()
window.resize(700, 500)


img_view = QLabel('Картинка')
img_folder = QListWidget()
btn_folder = QPushButton('Папка')
btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_mirror = QPushButton('Зеркало')
btn_sharpen = QPushButton('Резкость')
btn_bw = QPushButton('Ч/Б')
btn_blur = QPushButton('Размытие')

main_line = QHBoxLayout()
h_line = QHBoxLayout()
v_line1 = QVBoxLayout()
v_line2 = QVBoxLayout()

h_line.addWidget(btn_left)
h_line.addWidget(btn_right)
h_line.addWidget(btn_mirror)
h_line.addWidget(btn_sharpen)
h_line.addWidget(btn_bw)
h_line.addWidget(btn_blur)

v_line1.addWidget(btn_folder)
v_line1.addWidget(img_folder)

v_line2.addWidget(img_view)

v_line2.addLayout(h_line)

main_line.addLayout(v_line1)
main_line.addLayout(v_line2)

window.setLayout(main_line)

btn_folder.clicked.connect(showFilenameList)
img_folder.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_mirror.clicked.connect(workimage.do_mirror)
btn_sharpen.clicked.connect(workimage.do_sharpen)
btn_blur.clicked.connect(workimage.do_blur)

window.show()
app.exec_()