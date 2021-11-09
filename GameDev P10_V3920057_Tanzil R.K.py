# Line 2-7 = Import data yg diperlukan
from math import pi, sin, cos #untuk memuat library math dengan menginisialisasi variabel pi, sin, dan cos
from direct.showbase.ShowBase import ShowBase #untuk memuat sebagian besar modul panda3d dan menyebabkan window 3D muncul
from direct.task import Task #untuk memuat manajemen task dengan diinisialisasi menjadi Task
from direct.actor.Actor import Actor #untuk memuat kelas aktor yang berisi metode untuk membuat, memanipulasi, dan memainkan animasi karakter 3D
from direct.interval.IntervalGlobal import Sequence #untuk mengontrol interval 
from panda3d.core import Point3 #untuk mengatur koordinat aktor

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Line 14 = Menonaktifkan fungsi mouse sebagai penggerak kamera
        self.disableMouse()

        # Line 14 = Mengload model environtment
        self.scene = self.loader.loadModel("models/environment")
        # Line 19 = Atur ulang model yang akan dirender
        self.scene.reparentTo(self.render)
        # Line 21-22 = Transformasi skala dan posisi model environtment
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # Line 25 = Tambahkan prosedur spinCameraTask ke taskMgr/task manager
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # Line 28-31 = Mengload dan mengatur skala aktor panda
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        # Line 33 = Loop animasinya agar bisa bergerak
        self.pandaActor.loop("walk")

        # Line 37-48 = Tambahkan 4 interval agar aktor panda bisa bergerak maju mundur
        posInterval1 = self.pandaActor.posInterval(13,
                                                   Point3(0, -10, 0),
                                                   startPos=Point3(0, 10, 0))
        posInterval2 = self.pandaActor.posInterval(13,
                                                   Point3(0, 10, 0),
                                                   startPos=Point3(0, -10, 0))
        hprInterval1 = self.pandaActor.hprInterval(3,
                                                   Point3(180, 0, 0),
                                                   startHpr=Point3(0, 0, 0))
        hprInterval2 = self.pandaActor.hprInterval(3,
                                                   Point3(0, 0, 0),
                                                   startHpr=Point3(180, 0, 0))

        # Line 50-53 = Buat dan mainkan urutan (Sequence) sesuai koordinat intervalnya
        self.pandaPace = Sequence(posInterval1, hprInterval1,
                                  posInterval2, hprInterval2,
                                  name="pandaPace")
        self.pandaPace.loop()

    # Line 56-61 = Pembuatan fungsi spinCamera untuk pemutaran angle dari kamera
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

app = MyApp() #inisialisasi class MyApp untuk dijalankan aplikasinya

# Line 66-69 = Pengaturan suara
mySound = app.loader.loadSfx("game-music.ogg") #memanggil musik yang digunakan
mySound.play() #musik dimulai
mySound.setLoop(True) #loop musik
mySound.setVolume(10) #atur suara menjadi 10

app.run() #main loop untuk menjalankan frame window