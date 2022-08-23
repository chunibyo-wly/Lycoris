import sys
from math import sin, pi, atan2

from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia


def override(f):
    return f


class PixLabel(QtWidgets.QLabel):
    def __init__(self, parent):
        super(PixLabel, self).__init__(parent)
        self.start_pixmap = None
        self.start_pos = None

    def mousePressEvent(self, QEvent):
        self.start_pos = QEvent.pos()
        self.start_pixmap = self.pixmap()

    def mouseMoveEvent(self, QEvent):
        self.move(self.pos() + QEvent.pos() - self.start_pos)


class MainWindow(QtWidgets.QWidget):  # 主窗口 继承自QWidgets
    def __init__(self):
        super(MainWindow, self).__init__()

        # 状态量
        self.start_pos = None
        self.width = 600
        self.height = 540

        # 组件
        self.figLabel = PixLabel(self)  # 创建一个QLabel用于展示立绘图
        self.pixmap = QtGui.QPixmap(self.getResource("sakana.png"))  # 用QPixmap加载本地png图片

        self.menu = QtWidgets.QMenu()  # 实例化一个QMenu对象
        self.draggable_menu = self.menu.addAction('位置移动')
        self.draggable_menu.setCheckable(True)
        self.exit_menu = self.menu.addAction('退出')  # 往QMenu添加一个文本为“退出”的action 存放在exit变量里

        self.player = None
        self.animation = None

        self.initUI()

    def initUI(self):
        self.resize(self.width * 3, self.height * 3)  # 将窗口大小缩放成800x720分辨率
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置主窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 设置主窗口无边框
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)  # 设置主窗口置顶显示

        self.figLabel.setGeometry(self.width, self.height, self.width, self.height)

        self.updatePixmap("sakana.png")
        self.updateAudioFile("sakana.wav")
        self.initAnimation()

    def updatePixmap(self, image_name):
        self.pixmap = QtGui.QPixmap(self.getResource(image_name))
        pixmap = self.pixmap.scaled(self.width, self.height, QtCore.Qt.IgnoreAspectRatio,
                                    QtCore.Qt.SmoothTransformation)  # 抗锯齿缩放至800x720
        self.figLabel.setPixmap(pixmap)  # 用setPixmap将立绘展示到QLabel上

    def updateAudioFile(self, audio_name):
        url = QtCore.QUrl.fromLocalFile(self.getResource(audio_name))
        content = QtMultimedia.QMediaContent(url)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)

    def initAnimation(self):
        self.animation = QtCore.QPropertyAnimation(self.figLabel, b'geometry', self)  # 给hairLabel创建一个动画 类型为geometry
        self.animation.setEndValue(QtCore.QRect(self.width, self.height, self.width, self.height))  # 动画结束位置为假发初始位置
        easingCurve = QtCore.QEasingCurve()
        easingCurve.setCustomType(self.springCurve)
        self.animation.setEasingCurve(easingCurve)

    @staticmethod
    def springCurve(x):
        factor = 0.05
        return 2 ** (-10 * x) * sin((x - factor / 4) * (2 * pi) / factor) + 1

    @staticmethod
    def getResource(file_path):
        return QtCore.QDir.current().absoluteFilePath(rf'resource/{file_path}')

    @override
    def mousePressEvent(self, QEvent):
        self.start_pos = QEvent.pos()

    @override
    def mouseMoveEvent(self, QEvent):
        if self.draggable_menu.isChecked():
            self.move(self.pos() + QEvent.pos() - self.start_pos)

    @override
    def mouseReleaseEvent(self, QEvent):
        if QEvent.button() == QtCore.Qt.LeftButton and not self.draggable_menu.isChecked():
            self.player.stop()
            self.player.play()

            self.animation.setDuration(self.player.duration())
            self.animation.start()

    @override
    def contextMenuEvent(self, QEvent):
        action = self.menu.exec_(self.mapToGlobal(QEvent.pos()))
        if action == self.exit_menu:
            self.close()
        elif action == self.draggable_menu:
            if self.draggable_menu.isChecked():
                self.figLabel.setDisabled(True)
            else:
                self.figLabel.setDisabled(False)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # Qt主进程后台管理
    mainWindow = MainWindow()  # 实例化主窗口
    mainWindow.show()  # 显示主窗口
    sys.exit(app.exec_())  # 启动Qt主进程循环直到收到退出信号
