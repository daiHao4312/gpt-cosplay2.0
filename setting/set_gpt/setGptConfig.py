import os
import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox

import config


class Ui_Form(QWidget):

    def __init__(self):
        super(Ui_Form, self).__init__()
        # 设置窗口大小不可变
        self.setWindowFlag(QtCore.Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setupUi(self)
        self.gptConfigInit()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(738, 381)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./images/机器人.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Form.setWindowIcon(icon)
        self.tabWidget = QtWidgets.QTabWidget(parent=Form)
        self.tabWidget.setGeometry(QtCore.QRect(50, 20, 641, 261))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label = QtWidgets.QLabel(parent=self.tab)
        self.label.setGeometry(QtCore.QRect(20, 20, 81, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.tab)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 81, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.tab)
        self.label_3.setGeometry(QtCore.QRect(20, 130, 81, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(parent=self.tab)
        self.label_4.setGeometry(QtCore.QRect(330, 20, 71, 16))
        self.label_4.setObjectName("label_4")
        self.openaiKeyInput = QtWidgets.QLineEdit(parent=self.tab)
        self.openaiKeyInput.setGeometry(QtCore.QRect(110, 80, 501, 20))
        self.openaiKeyInput.setObjectName("openaiKeyInput")
        self.openaiUrlInput = QtWidgets.QLineEdit(parent=self.tab)
        self.openaiUrlInput.setGeometry(QtCore.QRect(110, 130, 501, 20))
        self.openaiUrlInput.setObjectName("openaiUrlInput")
        self.rolesInput = QtWidgets.QLineEdit(parent=self.tab)
        self.rolesInput.setGeometry(QtCore.QRect(410, 20, 201, 20))
        self.rolesInput.setObjectName("rolesInput")
        self.chatgptModifyBtn = QtWidgets.QPushButton(parent=self.tab)
        self.chatgptModifyBtn.setGeometry(QtCore.QRect(190, 180, 75, 24))
        self.chatgptModifyBtn.setObjectName("chatgptModifyBtn")

        # 修改gpt配置
        self.chatgptModifyBtn.clicked.connect(self.gptConfigChange)

        self.chatgptRestoreDefaultValuesBtn = QtWidgets.QPushButton(parent=self.tab)
        self.chatgptRestoreDefaultValuesBtn.setGeometry(QtCore.QRect(360, 180, 75, 24))
        self.chatgptRestoreDefaultValuesBtn.setObjectName("chatgptRestoreDefaultValuesBtn")

        # 恢复默认值
        self.chatgptRestoreDefaultValuesBtn.clicked.connect(self.RestoreDefaultValues)

        self.promptsComboBox = QtWidgets.QComboBox(parent=self.tab)
        self.promptsComboBox.setGeometry(QtCore.QRect(110, 20, 171, 22))
        self.promptsComboBox.setObjectName("promptsComboBox")
        self.tabWidget.addTab(self.tab, "")
        self.tab2 = QtWidgets.QWidget()
        self.tab2.setObjectName("tab2")
        self.tabWidget.addTab(self.tab2, "")
        self.label_5 = QtWidgets.QLabel(parent=Form)
        self.label_5.setGeometry(QtCore.QRect(200, 310, 81, 16))
        self.label_5.setObjectName("label_5")
        self.gptModelComboBox = QtWidgets.QComboBox(parent=Form)
        self.gptModelComboBox.setGeometry(QtCore.QRect(290, 310, 141, 22))
        self.gptModelComboBox.setObjectName("gptModelComboBox")
        self.gptModelChangeBtn = QtWidgets.QPushButton(parent=Form)
        self.gptModelChangeBtn.setGeometry(QtCore.QRect(450, 310, 75, 24))
        self.gptModelChangeBtn.setObjectName("gptModelChangeBtn")

        # 设置gpt模型
        self.gptModelChangeBtn.clicked.connect(self.setGptModel)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # 设置样式表
        self.addQss()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "GPT设置"))
        self.label.setText(_translate("Form", "选择prompts："))
        self.label_2.setText(_translate("Form", "openai的key："))
        self.label_3.setText(_translate("Form", "openai的url："))
        self.label_4.setText(_translate("Form", "扮演的角色："))
        self.openaiKeyInput.setPlaceholderText(_translate("Form", "sk-"))
        self.openaiUrlInput.setPlaceholderText(_translate("Form", "https://"))
        self.chatgptModifyBtn.setText(_translate("Form", "确定修改"))
        self.chatgptRestoreDefaultValuesBtn.setText(_translate("Form", "恢复默认值"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "ChatGPT"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), _translate("Form", "待开发"))
        self.label_5.setText(_translate("Form", "gpt模型选择："))
        self.gptModelChangeBtn.setText(_translate("Form", "完成"))

    # 设置背景图片
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("./images/卡芙卡.jpg")
        painter.drawPixmap(self.rect(), pixmap)


    def addQss(self):
        """
        添加样式表
        :return:
        """

        qss_file = './qss/setGptStyle.qss'
        with open(qss_file, 'r') as f:
            self.setStyleSheet(f.read())


    def gptConfigInit(self):
        """
        初始化gpt配置
        :return:
        """
        # 获取gpt_prompts下的所有文件名称
        folder_gpt_prompts_path = r"./module/gpt_api/gpt_prompts"  # 文件夹路径
        # 获取文件夹中的所有文件名
        file_names = os.listdir(folder_gpt_prompts_path)
        # 将文件名添加到下拉列表中
        self.promptsComboBox.clear()
        self.promptsComboBox.addItems(file_names)

        self.config_gpt_init = config.Config()
        self.openaiKeyInput.setText(self.config_gpt_init.openai_api_key)
        self.openaiUrlInput.setText(self.config_gpt_init.openai_api_url)
        self.rolesInput.setText(self.config_gpt_init.cosplay_role)
        self.promptsComboBox.setCurrentText(self.config_gpt_init.prompts_path.split("/")[-1])

        # 获取gpt模型
        self.gptModelComboBox.clear()
        for i in range(self.tabWidget.count()):
            tab_name = self.tabWidget.tabText(i)
            self.gptModelComboBox.addItem(tab_name)
        self.gptModelComboBox.setCurrentText(self.config_gpt_init.gpt_model)

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
            self.openaiKeyInput.setText("sk-FcRwry8b7CxfTvLrmx2n0BQuvOAiCAmXDvPBiCZbCUVHrLPB")
            self.openaiUrlInput.setText("http://api.chatanywhere.cn")
            self.rolesInput.setText("爱莉希雅")
            self.promptsComboBox.setCurrentText("爱莉希雅.txt")


    def gptConfigChange(self):
        """
        修改gpt配置
        :return:
        """

        reply = QMessageBox.question(
            None, "提示", "确定要修改吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.No:
            return
        else:
            openai_api_key_input = self.openaiKeyInput.text()
            openai_api_url_input = self.openaiUrlInput.text()
            cosplay_role_input = self.rolesInput.text()
            prompts_path_input = r"./module/gpt_api/gpt_prompts/" + self.promptsComboBox.currentText()

            config.set_gpt_config_change(openai_api_key_input, openai_api_url_input, cosplay_role_input, prompts_path_input)
            self.gptConfigInit()


    def setGptModel(self):
        """
        设置gpt模型
        :return:
        """

        # 获取当前选择的模型
        current_tab_index = self.gptModelComboBox.currentIndex()
        current_tab_name = self.tabWidget.tabText(current_tab_index)
        try:
            config.gpt_model_change(current_tab_name)
            QMessageBox.information(None, "提示", "修改成功！")
        except Exception as e:
            QMessageBox.warning(None, "警告", "修改失败！")
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Ui_Form()
    ui.show()

    sys.exit(app.exec())
