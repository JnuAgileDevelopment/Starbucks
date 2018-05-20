# coding:utf-8

import sys
import top_K
import draw
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtCore import Qt, QBasicTimer, QThread
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MyUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.mainWidget = QWidget()
        self.mainLayout = QGridLayout()

        self.createMenu()
        self.setFindTopKWidget()
        self.setTextView()

        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

        self.adjustSize()
        self.setWindowTitle('StarBucks')
        self.setWindowIcon(QIcon('bucklogo.jpg'))
        # self.setVisualButton()
        self.show()

    # 创建菜单
    def createMenu(self):
        menubar = self.menuBar()
        menu = menubar.addMenu("绘图(D)")
        menu.addAction(QAction("国家密度渐变图", self, triggered=self.countryMap))
        menu.addAction(QAction("按时区密度渐变图", self, triggered=self.timezoneMap))

        menu = menubar.addMenu("可视化(S)")
        menu.addAction(QAction("k增长时延", self))
        # menu.addAction(QAction("range_r查询", self, triggered=self.rangeR_search_item))


    # top-k的输入框，按钮的控件
    def setFindTopKWidget(self):
        longitudeLabel = QLabel()
        latitudeLabel = QLabel()
        kLabel = QLabel()
        keywordLable = QLabel()
        rLable = QLabel()

        longitudeLabel.setText("经度")
        latitudeLabel.setText("纬度")
        kLabel.setText("k")
        keywordLable.setText("关键字")
        rLable.setText("r")

        self.longitudeEdit = QLineEdit()
        self.latitudeEdit = QLineEdit()
        self.kEdit = QLineEdit()
        self.keywordEdit = QLineEdit()
        self.rEdit = QLineEdit()

        self.topKButton = QPushButton()
        self.topKButton.setText("topK查找")
        # self.topKButton.setEnabled(False)
        self.topKButton.clicked.connect(self.top_k_search)

        self.rangeRButton = QPushButton()
        self.rangeRButton.setText("rangeR查找")
        # self.rangeRButton.setEnabled(False)
        self.rangeRButton.clicked.connect(self.range_r_search)

        h_lgt_lat_Box = QHBoxLayout(self)
        h_lgt_lat_Box.addWidget(longitudeLabel)
        h_lgt_lat_Box.addWidget(self.longitudeEdit)
        h_lgt_lat_Box.addWidget(latitudeLabel)
        h_lgt_lat_Box.addWidget(self.latitudeEdit)

        h_topk_Box = QHBoxLayout(self)
        h_topk_Box.addWidget(kLabel)
        h_topk_Box.addWidget(self.kEdit)
        h_topk_Box.addWidget(keywordLable)
        h_topk_Box.addWidget(self.keywordEdit)
        h_topk_Box.addWidget(self.topKButton)

        h_ranger_Box = QHBoxLayout(self)
        h_ranger_Box.addWidget(rLable)
        h_ranger_Box.addWidget(self.rEdit)
        h_ranger_Box.addWidget(self.rangeRButton)

        vBox = QVBoxLayout(self)
        vBox.addLayout(h_lgt_lat_Box)
        vBox.addLayout(h_topk_Box)
        vBox.addLayout(h_ranger_Box)

        vWidget = QWidget()
        vWidget.setLayout(vBox)
        self.mainLayout.addWidget(vWidget)

    def setTextView(self):
        self.textEidt = QTextEdit()
        self.mainLayout.addWidget(self.textEidt)

    def setVisualButton(self):
        VsButton = QPushButton("查看增长变化图像")
        mapButton = QPushButton("查看地图")
 
        vsbtnbox = QHBoxLayout()
        vsbtnbox.addStretch(1)
        vsbtnbox.addWidget(VsButton)
        vsbtnbox.addWidget(mapButton)

        hWidget = QWidget()
        hWidget.setLayout(vsbtnbox)

        self.mainLayout.addWidget(hWidget, 2, 1)

    def countryMap(self):
        draw.draw_country_map()

    def timezoneMap(self):
        draw.draw_timezone_map('tz1')

    def longitudeMap(self):
        draw.draw_log_lat('Longitude', 'longitude')

    def latitudeMap(self):
        draw.draw_log_lat('Latitude', 'latitude')

    def top_k_search(self):
        try:
            lgt = float(self.longitudeEdit.text())
            if lgt < -180 or lgt > 180:
                raise OverflowError
        except (Exception, OverflowError, ValueError):
            QMessageBox.warning(self, "错误", "请输入正确的经度值(-180~180)", QMessageBox.Yes)
            return
        try:
            lat = float(self.latitudeEdit.text())
            if lat < -90 or lat > 90:
                raise OverflowError
        except (Exception, OverflowError, ValueError):
            QMessageBox.warning(self, "错误", "请输入正确的纬度值(-90~90)", QMessageBox.Yes)
            return
        try:
            k = int(self.kEdit.text())
            if k <= 0:
                raise OverflowError
        except (Exception, OverflowError, ValueError):
            QMessageBox.warning(self, "错误", "k必须为正整数", QMessageBox.Yes)
            return

        keyword = self.keywordEdit.text()
        if keyword == "":
            text = top_K.top_k_search(lgt, lat, k)
        else:
            text = top_K.top_k_keyword_search(lgt, lat, k, keyword)

        self.textEidt.setText(text)

    def range_r_search(self):
        try:
            lgt = float(self.longitudeEdit.text())
            if lgt < -180 or lgt > 180:
                raise OverflowError
        except (Exception, OverflowError, ValueError):
            QMessageBox.warning(self, "错误", "请输入正确的经度值(-180~180)", QMessageBox.Yes)
            return
        try:
            lat = float(self.latitudeEdit.text())
            if lat < -90 or lat > 90:
                raise OverflowError
        except (Exception, OverflowError, ValueError):
            QMessageBox.warning(self, "错误", "请输入正确的纬度值(-90~90)", QMessageBox.Yes)
            return
        try:
            r = float(self.rEdit.text())
            if r <= 0:
                raise OverflowError
        except (Exception, OverflowError, ValueError):
            QMessageBox.warning(self, "错误", "r必须为正数", QMessageBox.Yes)
            return

        text = top_K.range_r_search(lgt, lat, r)
        self.textEidt.setText(text)

    # 控制窗口显示在屏幕中心的方法
    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    # 关闭确认，关闭窗口出发QCloseEvent
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MyUI()
    sys.exit(app.exec_())