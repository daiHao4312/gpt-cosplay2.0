import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox

import config
from module.vits_api import vits


class Ui_Form(QWidget):

    def __init__(self):
        super(Ui_Form, self).__init__()
        # 设置窗口大小不可变
        self.setWindowFlag(QtCore.Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setupUi(self)
        self.vitsConfigInit()
        self.config_vits_init = config.Config()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(881, 510)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./images/语音识别.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Form.setWindowIcon(icon)

        self.groupBox_2 = QtWidgets.QGroupBox(parent=Form)
        self.groupBox_2.setGeometry(QtCore.QRect(70, 250, 741, 131))
        self.groupBox_2.setObjectName("groupBox_2")
        self.vitsTextBtn = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.vitsTextBtn.setGeometry(QtCore.QRect(270, 100, 75, 24))
        self.vitsTextBtn.setObjectName("vitsTextBtn")

        self.label_6 = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(40, 20, 61, 16))
        self.label_6.setObjectName("label_6")
        self.vitsTextInput = QtWidgets.QTextEdit(parent=self.groupBox_2)
        self.vitsTextInput.setGeometry(QtCore.QRect(100, 20, 561, 71))
        self.vitsTextInput.setObjectName("vitsTextInput")
        self.tipAudio = QtWidgets.QLabel(parent=self.groupBox_2)
        self.tipAudio.setGeometry(QtCore.QRect(530, 100, 71, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tipAudio.setFont(font)
        self.tipAudio.setText("")
        self.tipAudio.setObjectName("tipAudio")
        self.vitsTextClear = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.vitsTextClear.setGeometry(QtCore.QRect(400, 100, 75, 24))
        self.vitsTextClear.setObjectName("vitsTextClear")

        self.tabWidget = QtWidgets.QTabWidget(parent=Form)
        self.tabWidget.setGeometry(QtCore.QRect(70, 20, 741, 211))
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label = QtWidgets.QLabel(parent=self.tab)
        self.label.setGeometry(QtCore.QRect(80, 70, 61, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.tab)
        self.label_2.setGeometry(QtCore.QRect(90, 20, 51, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.tab)
        self.label_3.setGeometry(QtCore.QRect(490, 20, 41, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(parent=self.tab)
        self.label_4.setGeometry(QtCore.QRect(300, 20, 41, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(parent=self.tab)
        self.label_5.setGeometry(QtCore.QRect(60, 120, 81, 16))
        self.label_5.setObjectName("label_5")
        self.vitsIdInput = QtWidgets.QLineEdit(parent=self.tab)
        self.vitsIdInput.setGeometry(QtCore.QRect(140, 20, 113, 20))
        self.vitsIdInput.setObjectName("vitsIdInput")
        self.vitsLangInput = QtWidgets.QLineEdit(parent=self.tab)
        self.vitsLangInput.setGeometry(QtCore.QRect(340, 20, 113, 20))
        self.vitsLangInput.setObjectName("vitsLangInput")
        self.vitsLengthInput = QtWidgets.QLineEdit(parent=self.tab)
        self.vitsLengthInput.setGeometry(QtCore.QRect(530, 20, 113, 20))
        self.vitsLengthInput.setObjectName("vitsLengthInput")
        self.vitsApiInput = QtWidgets.QLineEdit(parent=self.tab)
        self.vitsApiInput.setGeometry(QtCore.QRect(140, 70, 501, 20))
        self.vitsApiInput.setObjectName("vitsApiInput")
        self.vitsWavPathInput = QtWidgets.QLineEdit(parent=self.tab)
        self.vitsWavPathInput.setGeometry(QtCore.QRect(140, 120, 501, 20))
        self.vitsWavPathInput.setObjectName("vitsWavPathInput")
        self.vitsModifyBtn = QtWidgets.QPushButton(parent=self.tab)
        self.vitsModifyBtn.setGeometry(QtCore.QRect(260, 150, 75, 24))
        self.vitsModifyBtn.setObjectName("vitsModifyBtn")

        self.vitsRestoreDefaultValuesBtn = QtWidgets.QPushButton(parent=self.tab)
        self.vitsRestoreDefaultValuesBtn.setGeometry(QtCore.QRect(420, 150, 75, 24))
        self.vitsRestoreDefaultValuesBtn.setObjectName("vitsRestoreDefaultValuesBtn")

        self.tabWidget.addTab(self.tab, "")
        self.tab2 = QtWidgets.QWidget()
        self.tab2.setObjectName("tab2")
        self.tabWidget.addTab(self.tab2, "")
        self.label_8 = QtWidgets.QLabel(parent=Form)
        self.label_8.setGeometry(QtCore.QRect(250, 410, 61, 16))
        self.label_8.setObjectName("label_8")
        self.vitsModelBtn = QtWidgets.QPushButton(parent=Form)
        self.vitsModelBtn.setGeometry(QtCore.QRect(520, 410, 75, 24))
        self.vitsModelBtn.setObjectName("vitsModelBtn")
        self.vitsModelComboBox = QtWidgets.QComboBox(parent=Form)
        self.vitsModelComboBox.setGeometry(QtCore.QRect(330, 410, 161, 22))
        self.vitsModelComboBox.setObjectName("vitsModelComboBox")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # 初始化设置
        self.initToSetupUi()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "VITS设置"))
        self.groupBox_2.setTitle(_translate("Form", "试听"))
        self.vitsTextBtn.setText(_translate("Form", "确认"))
        self.label_6.setText(_translate("Form", "输入文本："))
        self.vitsTextClear.setText(_translate("Form", "清空"))
        self.label.setText(_translate("Form", "vits的api："))
        self.label_2.setText(_translate("Form", "角色ID："))
        self.label_3.setText(_translate("Form", "语速："))
        self.label_4.setText(_translate("Form", "语言："))
        self.label_5.setText(_translate("Form", "音频保存地址："))
        self.vitsModifyBtn.setText(_translate("Form", "确认修改"))
        self.vitsRestoreDefaultValuesBtn.setText(_translate("Form", "恢复默认值"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "vits"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), _translate("Form", "待开发"))
        self.label_8.setText(_translate("Form", "选择模型："))
        self.vitsModelBtn.setText(_translate("Form", "完成"))

    # 设置背景图片
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("./images/爱莉希雅2.jpg")
        painter.drawPixmap(self.rect(), pixmap)

    def initToSetupUi(self):
        """
        初始化设置
        :return:
        """
        # 绑定试听按钮
        self.vitsTextBtn.clicked.connect(self.showVits)

        # 绑定清空按钮
        self.vitsTextClear.clicked.connect(self.TextClear)

        # 绑定确认修改按钮
        self.vitsModifyBtn.clicked.connect(self.vitsConfigChange)

        # 绑定恢复默认值按钮
        self.vitsRestoreDefaultValuesBtn.clicked.connect(self.RestoreDefaultValues)

        # 绑定完成按钮
        self.vitsModelBtn.clicked.connect(self.setVitsModel)

        # 添加样式表
        self.addQss()

    def vitsConfigInit(self):
        """
        初始化vits配置
        :return:
        """
        self.config_vits_init = config.Config()
        self.vitsIdInput.setText(self.config_vits_init.vits_id)
        self.vitsLangInput.setText(self.config_vits_init.vits_lang)
        self.vitsLengthInput.setText(self.config_vits_init.vits_length)
        self.vitsApiInput.setText(self.config_vits_init.vits_api_url)
        self.vitsWavPathInput.setText(self.config_vits_init.vits_wav_path)

        self.vitsModelComboBox.clear()
        for i in range(self.tabWidget.count()):
            tab_name = self.tabWidget.tabText(i)
            self.vitsModelComboBox.addItem(tab_name)
        self.vitsModelComboBox.addItem("无")
        self.vitsModelComboBox.setCurrentText(self.config_vits_init.vits_model)

    def RestoreDefaultValues(self):
        """
        恢复默认值
        :return:
        """
        reply = QMessageBox.question(
            None, "提示", "确定要恢复默认值吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.No:
            return
        else:
            self.vitsIdInput.setText("225")
            self.vitsLangInput.setText("zh")
            self.vitsLengthInput.setText("1.4")
            self.vitsApiInput.setText("http://127.0.0.1:23456/voice/vits")
            self.vitsWavPathInput.setText("./module/vits_api/vits_wav/vits_voice.wav")

    def vitsConfigChange(self):
        """
        修改vits配置
        :return:
        """

        # 提示框
        reply = QMessageBox.question(
            None, "提示", "确定要修改吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            config.set_vits_config_change(
                self.vitsIdInput.text(),
                self.vitsLangInput.text(),
                self.vitsLengthInput.text(),
                self.vitsApiInput.text(),
                self.vitsWavPathInput.text()
            )

            self.vitsConfigInit()
        else:
            return

    def showVits(self):
        """
        试听vits
        :return:
        """
        vitsText = self.vitsTextInput.toPlainText()
        if vitsText.strip() == "":
            QMessageBox.warning(None, "警告", "请输入文本！")
            return
        self.config_vits_init = config.Config()
        if self.config_vits_init.vits_model == "vits":
            self.vits_thread = vits.VITSThread(vitsText, self.config_vits_init.vits_id, self.config_vits_init.vits_lang,
                                               self.config_vits_init.vits_length)
            self.vits_thread.start()
            self.vits_thread.transcription_complete.connect(self.on_transcription_complete)
            self.tipAudio.setText("等待中···")
        elif self.config_vits_init.vits_model == "无":
            QMessageBox.warning(None, "警告", "当前没有选择vits模型！")
            return
        else:
            QMessageBox.warning(None, "警告", "请先选择vits模型！")
            return

        self.vitsModelComboBox.setCurrentText(self.config_vits_init.vits_model)

    def on_transcription_complete(self):
        self.tipAudio.setText("")
        self.vitsTextInput.clear()
        print("转写完成")

    def TextClear(self):
        """
        清空文本
        :return:
        """
        self.vitsTextInput.clear()

    def setVitsModel(self):
        """
        设置vits模型
        :return:
        """

        # 获取当前选择的模型
        current_tab_index = self.vitsModelComboBox.currentIndex()
        if current_tab_index == (self.vitsModelComboBox.count() - 1):
            current_tab_name = "无"
        else:
            current_tab_name = self.tabWidget.tabText(current_tab_index)
        try:
            print(current_tab_name)
            config.vits_model_change(current_tab_name)
            QMessageBox.information(None, "提示", "修改成功！")
        except Exception as e:
            QMessageBox.warning(None, "警告", "修改失败！")
            print(e)

    def addQss(self):
        """
        添加样式表
        :return:
        """

        qss_file = './qss/setVitsStyle.qss'
        with open(qss_file, 'r') as f:
            self.setStyleSheet(f.read())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Ui_Form()
    ui.show()

    sys.exit(app.exec())
