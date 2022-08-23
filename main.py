import sys

from PyQt5 import QtCore, QtGui, QtWidgets


def override(f):
    return f


class MainWindow(QtWidgets.QWidget):  # 主窗口 继承自QWidgets
    def __init__(self):
        super(MainWindow, self).__init__()

        # 状态量
        self.start_pos = None
        self.width = 600
        self.height = 540

        # 组件
        self.figLabel = QtWidgets.QLabel(self)  # 创建一个QLabel用于展示立绘图
        self.pixmap = QtGui.QPixmap(r'resource/sakana.png')  # 用QPixmap加载本地png图片

        self.menu = QtWidgets.QMenu()  # 实例化一个QMenu对象
        self.exit_menu = self.menu.addAction('退出')  # 往QMenu添加一个文本为“退出”的action 存放在exit变量里
        self.draggable_menu = self.menu.addAction('移动')
        self.draggable_menu.setCheckable(True)

        self.initUI()

    def initUI(self):
        self.resize(self.width, self.height)  # 将窗口大小缩放成800x720分辨率
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置主窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 设置主窗口无边框
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)  # 设置主窗口置顶显示

        self.updatePixmap("sakana.png")

    def updatePixmap(self, image_name):
        self.pixmap = QtGui.QPixmap(rf'resource/{image_name}')
        pixmap = self.pixmap.scaled(self.width, self.height, QtCore.Qt.IgnoreAspectRatio,
                                    QtCore.Qt.SmoothTransformation)  # 抗锯齿缩放至800x720
        self.figLabel.setPixmap(pixmap)  # 用setPixmap将立绘展示到QLabel上
        self.figLabel.setGeometry(0, 0, self.width, self.height)  # 将QLabel覆盖到graph上面

    @override
    def mousePressEvent(self, QEvent):  # 响应鼠标点击
        self.start_pos = QEvent.pos()  # 记录第一下鼠标点击的坐标

    @override
    def mouseMoveEvent(self, QEvent):  # 响应鼠标移动
        if self.draggable_menu.isChecked():
            self.move(self.pos() + QEvent.pos() - self.start_pos)  # 移动至当前坐标加上鼠标移动偏移量

    @override
    def contextMenuEvent(self, QEvent):  # 响应鼠标右键菜单事件
        action = self.menu.exec_(self.mapToGlobal(QEvent.pos()))  # 将QEvent.pos()映射为屏幕全局坐标 然后在此坐标弹出菜单
        if action == self.exit_menu:
            self.close()  # 判断用户点击哪个action 如果是exit就调用self.close()退出


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # Qt主进程后台管理
    mainWindow = MainWindow()  # 实例化主窗口
    mainWindow.show()  # 显示主窗口
    sys.exit(app.exec_())  # 启动Qt主进程循环直到收到退出信号
