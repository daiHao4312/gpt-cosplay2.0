import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QApplication, QInputDialog, QMessageBox, QLabel

import config
from dao import chatDao
from entity import chatModel
from module.gpt_api import openAI
from module.vits_api import vits, gptSoVits
from module.voice_recognition import voice_to_text
from setting.set_gpt import setGptConfig
from setting.set_vits import setVitsConfig


class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        # 设置窗口大小不可变
        self.setWindowFlag(QtCore.Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setupUi(self)
        self.chatTable = ''
        self.chatTableName = ''
        self.userChat = ''
        self.audioFlag = True
        self.chatHistoryListInit()
        self.chatListInit()
        self.initAudio()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(869, 528)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./images/鹤木阳渚.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        MainWindow.setWindowIcon(icon)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ChatList = QtWidgets.QListWidget(parent=self.centralwidget)
        self.ChatList.setGeometry(QtCore.QRect(70, 10, 561, 341))
        self.ChatList.setWordWrap(True)
        self.ChatList.setObjectName("ChatList")
        self.SeedBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.SeedBtn.setGeometry(QtCore.QRect(570, 370, 61, 31))
        self.SeedBtn.setObjectName("SeedBtn")

        self.SaidBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.SaidBtn.setStyleSheet("background-color: green; border-radius: 5px;")
        self.SaidBtn.setGeometry(QtCore.QRect(290, 450, 75, 24))
        self.SaidBtn.setObjectName("SaidBtn")

        self.ChatListClearBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.ChatListClearBtn.setGeometry(QtCore.QRect(570, 410, 71, 31))
        self.ChatListClearBtn.setObjectName("ChatListClearBtn")

        self.ChatInputText = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.ChatInputText.setGeometry(QtCore.QRect(70, 370, 491, 71))
        self.ChatInputText.setObjectName("ChatInputText")

        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(720, 10, 71, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.ChatHistoryList = QtWidgets.QListWidget(parent=self.centralwidget)
        self.ChatHistoryList.setGeometry(QtCore.QRect(670, 40, 171, 192))
        self.ChatHistoryList.setWordWrap(True)
        self.ChatHistoryList.setObjectName("ChatHistoryList")

        self.ChatHistoryBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.ChatHistoryBtn.setGeometry(QtCore.QRect(670, 250, 75, 24))
        self.ChatHistoryBtn.setObjectName("ChatHistoryBtn")

        self.ChatHistoryDelBtn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.ChatHistoryDelBtn.setGeometry(QtCore.QRect(770, 250, 75, 24))
        self.ChatHistoryDelBtn.setObjectName("ChatHistoryDelBtn")

        self.LuYingFlag = QtWidgets.QLabel(parent=self.centralwidget)
        self.LuYingFlag.setGeometry(QtCore.QRect(390, 450, 91, 21))
        self.LuYingFlag.setText("")
        self.LuYingFlag.setObjectName("LuYingFlag")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 869, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(parent=self.menubar)
        self.menu.setObjectName("menu")

        self.menu_2 = QtWidgets.QMenu(parent=self.menubar)
        self.menu_2.setObjectName("menu_2")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionvits = QtGui.QAction(parent=MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./images/语音识别.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionvits.setIcon(icon1)
        self.actionvits.setObjectName("actionvits")
        self.actiongpt = QtGui.QAction(parent=MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./images/机器人.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actiongpt.setIcon(icon2)
        self.actiongpt.setObjectName("actiongpt")
        self.action = QtGui.QAction(parent=MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("./images/作者.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.action.setIcon(icon3)
        self.action.setObjectName("action")
        self.actiongithub = QtGui.QAction(parent=MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("./images/github.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actiongithub.setIcon(icon4)
        self.actiongithub.setObjectName("actiongithub")
        self.menu.addAction(self.actionvits)
        self.menu.addAction(self.actiongpt)
        self.menu_2.addAction(self.action)
        self.menu_2.addAction(self.actiongithub)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 初始化设置
        self.initToSetupUi()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "gpt-cosplay_2.0"))
        self.SeedBtn.setText(_translate("MainWindow", "发送"))
        self.SaidBtn.setText(_translate("MainWindow", "语音"))
        self.ChatListClearBtn.setText(_translate("MainWindow", "清除对话"))
        self.label.setText(_translate("MainWindow", "历史记录"))
        self.ChatHistoryBtn.setText(_translate("MainWindow", "选定记录"))
        self.ChatHistoryDelBtn.setText(_translate("MainWindow", "删除记录"))
        self.menu.setTitle(_translate("MainWindow", "设置"))
        self.menu_2.setTitle(_translate("MainWindow", "帮助"))
        self.actionvits.setText(_translate("MainWindow", "vits设置"))
        self.actiongpt.setText(_translate("MainWindow", "gpt设置"))
        self.action.setText(_translate("MainWindow", "作者"))
        self.actiongithub.setText(_translate("MainWindow", "github"))

    def eventFilter(self, obj, event):
        if obj is self.ChatInputText and event.type() == QtCore.QEvent.Type.FocusIn:
            self.onTextEditFocusInEvent()
        return super().eventFilter(obj, event)

    def initToSetupUi(self):
        """
        初始化设置
        :return:
        """

        # 设置状态栏内容
        self.myLabel = QLabel()
        self.myLabel.setStyleSheet("color: #E3F6FE; font-size: 12px;")

        # 为发送按钮添加事件
        self.SeedBtn.clicked.connect(self.chatSeedAndBegin)

        # 为语音按钮添加事件
        self.SaidBtn.clicked.connect(self.voiceText)

        # 为清除对话按钮添加事件
        self.ChatListClearBtn.clicked.connect(self.chatEnd)

        # 为输入框添加鼠标聚焦事件
        self.ChatInputText.installEventFilter(self)

        # 为label添加样式表
        self.label.setStyleSheet("color: #A483E9;")

        # 为历史记录列表添加事件
        self.ChatHistoryList.itemClicked.connect(self.ChatHistoryList_list_item_clicked)

        # 为历史记录按钮添加事件
        self.ChatHistoryBtn.clicked.connect(self.chatListInit)

        # 为删除历史记录按钮添加事件
        self.ChatHistoryDelBtn.clicked.connect(self.ChatHistoryDelete)

        # 打开系统设置窗体
        self.menu.triggered[QAction].connect(self.openSetting)

        # 设置菜单
        self.menu_2.triggered[QAction].connect(self.openHelp)

        # 添加样式表
        self.addQss()

    def ChatHistoryList_list_item_clicked(self, item):
        """
        选择历史记录列表项
        :param item:
        :return:
        """
        if item is None:
            self.chatTable = ''
        else:
            print(item.text())
            self.chatTable = item.text()

    def statusbarChange(self):
        """
        状态栏内容初始化
        :return:
        """
        self.congfig_init = config.Config()
        self.myLabel.setText(f"vits模型：{self.congfig_init.vits_model}  gpt模型：{self.congfig_init.gpt_model}")
        self.statusbar.addWidget(self.myLabel)

    def onTextEditFocusInEvent(self):
        """
        输入框获得焦点时的操作
        :return:
        """
        # 在此处执行鼠标聚焦到输入框时的操作
        print("输入框获得焦点")
        self.statusbarChange()

    def chatListInit(self):
        """
        初始化对话列表
        :return:
        """

        self.statusbarChange()

        if self.chatTable == '':
            self.clearList()
        else:
            if self.chatTableName == self.chatTable:
                return
            else:
                # 结束对话
                if self.chatTableName != '':
                    openAI.end_chat()
                    self.userChat = ''

                self.clearList()
                self.chatTableName = ''
                result = chatDao.showChatData(self.chatTable)
                for item in result:
                    self.ChatList.addItem(item[1] + ':' + item[2])

    def chatHistoryListInit(self):
        """
        初始化历史记录列表
        :return:
        """
        result = chatDao.showAllTables()
        for item in result:
            self.ChatHistoryList.addItem(item[0])

    def clearList(self):
        """
        清空对话列表
        :return:
        """
        self.ChatList.clear()
        print('清空列表')

    def chatSeedAndBegin(self):
        """
        发送对话并创建对话表
        :return:
        """

        config_gpt_model = config.Config()
        # 获取输入框的内容
        self.userChat = self.ChatInputText.toPlainText()
        if self.userChat.strip() == "":
            QMessageBox.warning(self, "警告", "请输入对话内容！")
            return
        print('user:' + self.userChat)

        # 将用户输入添加到数据库中
        if self.chatTableName == '':
            text, ok = QInputDialog.getText(self, "请输入本次对话的标题", "标题:")
            if ok:
                print(text)
                self.chatTableName = text
                self.ChatInputText.clear()
                chat = chatModel.Chat(self.chatTableName, 'user', self.userChat)
                chatDao.createChatTable(chat)
                self.ChatHistoryList.clear()  # 清空历史记录列表
                self.chatHistoryListInit()  # 初始化历史记录列表

                if config_gpt_model.gpt_model == 'ChatGPT':
                    err = openAI.init_chat()  # 初始化openAI聊天模型
                    if err == 0:
                        QMessageBox.warning(self, "警告", "请填写key！")
                else:
                    QMessageBox.warning(self, "警告", "请先选择gpt模型！")
                    self.chatTableName = ''
                    return
            else:
                # 用户点击了取消按钮
                QMessageBox.information(self, "提示", "你取消了输入")
                return

        # 将用户输入添加到数据库中
        chatDao.addChatData(chatModel.Chat(self.chatTableName, 'user', self.userChat))
        # 将用户输入添加到对话列表中
        result_user = chatDao.showChatData(self.chatTableName)
        self.ChatList.clear()  # 清空对话列表
        for item in result_user:
            self.ChatList.addItem(item[1] + ':' + item[2])

        QApplication.processEvents()  # 刷新界面

        if config_gpt_model.gpt_model == 'ChatGPT':
            self.assistantToChatgpt()
        else:
            QMessageBox.warning(self, "警告", "请先选择gpt模型！")
            return

    def assistantToChatgpt(self):
        """
        调用openAI聊天模型
        :return:
        """
        # 调用openAI聊天模型
        assistantChat = openAI.chatgpt(self.userChat)

        # 将模型回复添加到数据库中
        chatDao.addChatData(chatModel.Chat(self.chatTableName, 'assistant', assistantChat))
        # 将模型回复添加到对话列表中
        result_assistant = chatDao.showChatData(self.chatTableName)
        self.ChatList.clear()  # 清空对话列表
        for item in result_assistant:
            self.ChatList.addItem(item[1] + ':' + item[2])

        self.ChatInputText.clear()  # 清空输入框
        try:
            config_vits_model_init = config.Config()
            if config_vits_model_init.vits_model == 'vits' or config_vits_model_init.vits_model == 'GPT-SoVITS':
                self.textToAudio(assistantChat)  # 文字转语音
                self.LuYingFlag.setText("等待中...")
            elif config_vits_model_init.vits_model == '无':
                self.LuYingFlag.setText("无vits模型")
                return
            else:
                self.LuYingFlag.setText("")
                QMessageBox.warning(self, "警告", "请先选择vits模型！")
                return
        except Exception as e:
            print(e)
            return

    def chatEnd(self):
        """
        结束对话
        :return:
        """
        if self.chatTableName == '':
            QMessageBox.warning(self, "警告", "没有对话删除！")
            return
        else:
            openAI.end_chat()
            self.ChatList.clear()  # 清空对话列表
            self.ChatInputText.clear()  # 清空输入框
            self.chatTableName = ''  # 清空对话表名
            self.chatTable = ''  # 清空对话表名
            self.userChat = ''  # 清空用户输入
            # print('对话结束')

    def ChatHistoryDelete(self):
        """
        删除历史记录
        :return:
        """
        if self.chatTable == '':
            QMessageBox.warning(self, "警告", "请选择要删除的历史记录！")
            return
        else:
            reply = QMessageBox.question(self, "提示", "确定要删除吗？",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                if chatDao.deleteChatTable(self.chatTable) < 0:
                    # QtWidgets.QMessageBox.information(None, "提示", "删除成功！")
                    print("删除成功！")
                    if self.chatTableName == '':
                        self.ChatList.clear()
                    elif self.chatTableName == self.chatTable:
                        self.ChatList.clear()
                        openAI.end_chat()
                        self.chatTableName = ''
                else:
                    QtWidgets.QMessageBox.warning(None, "警告", "删除失败！")
                self.ChatHistoryList.clear()
                self.chatHistoryListInit()

    def initAudio(self):
        """
        初始化语音转文字
        :return:
        """
        config_voice_wav_path = config.Config()
        self.audio_thread = voice_to_text.AudioRecorderThread(config_voice_wav_path.voice_wav_path)
        self.audio_thread.audio_finished.connect(self.finish_recording)

    def voiceText(self):
        """
        语音转文字
        :return:
        """
        if self.audioFlag:
            self.audio_thread.start()
            self.audioFlag = False
            self.LuYingFlag.setText("录音中")
            # 改变按钮颜色--绿色
            self.SaidBtn.setStyleSheet("background-color: red")
            self.SaidBtn.setText("停止")
        else:
            self.audio_thread.stop_recording()
            self.audioFlag = True
            self.LuYingFlag.setText("录音结束")
            # 改变按钮颜色--绿色
            self.SaidBtn.setStyleSheet("background-color: green")
            self.SaidBtn.setText("语音")

    def finish_recording(self):
        """
        结束录音
        :return:
        """
        self.audioFlag = True
        self.transcribe()
        self.LuYingFlag.setText("")

    def transcribe(self):
        """
        转写
        :return:
        """
        self.audio_thread.transcribe_audio()
        self.transcribed_text = self.audio_thread.get_transcribed_text()
        self.ChatInputText.setText(self.transcribed_text)

    def textToAudio(self, text):
        """
        文字转语音
        :return:
        """
        config_vits = config.Config()
        if config_vits.vits_model == 'vits':
            try:
                self.vits_thread = vits.VITSThread(text, config_vits.vits_id, config_vits.vits_lang,
                                                   config_vits.vits_length)
                self.vits_thread.start()
                self.vits_thread.transcription_complete.connect(self.on_transcription_complete)
                self.vits_thread.error_occurred.connect(self.handle_error)
            except Exception as e:
                QtWidgets.QMessageBox.warning(None, "警告", "文字转语音失败！")
                print(e)
                return

        elif config_vits.vits_model == "GPT-SoVITS":
            try:
                self.GptSoVitsThread = gptSoVits.GptSoVitsThread(text, config_vits.gptSoVits_id,
                                                                 config_vits.gptSoVits_lang,
                                                                 config_vits.gptSoVits_prompt_lang,
                                                                 config_vits.gptSoVits_preset)
                self.GptSoVitsThread.start()
                self.GptSoVitsThread.transcription_complete_gptsovits.connect(self.on_transcription_complete)
                self.GptSoVitsThread.error_occurred_gptsovits.connect(self.handle_error)
            except Exception as e:
                QtWidgets.QMessageBox.warning(None, "警告", "文字转语音失败！")
                print(e)
                return

        else:
            QMessageBox.warning(None, "警告", "请先选择vits模型！")
            return

    def on_transcription_complete(self):
        self.LuYingFlag.setText("")
        print("转写完成")

    def handle_error(self, error):
        """
        处理错误
        :param error:
        :return:
        """
        self.LuYingFlag.setText("")
        QtWidgets.QMessageBox.warning(None, "警告", error)

    def openSetting(self, m):
        '''
        打开系统设置窗体
        :return:
        '''
        if m.text() == 'vits设置':
            self.setVitsConfig = setVitsConfig.Ui_Form()
            self.setVitsConfig.show()

        elif m.text() == 'gpt设置':
            self.setGptConfig = setGptConfig.Ui_Form()
            self.setGptConfig.show()

    def openHelp(self, m):
        '''
        打开帮助窗体
        :return:
        '''
        if m.text() == '作者':
            # 博客地址
            QtGui.QDesktopServices.openUrl(QtCore.QUrl('http://daihao4312.cn'))
        elif m.text() == 'github':
            # github地址
            QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://github.com/daiHao4312/gpt-cosplay2.0'))

    def addQss(self):
        """
        添加样式表
        :return:
        """

        qss_file = './qss/mainStyle.qss'
        with open(qss_file, 'r') as f:
            self.setStyleSheet(f.read())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()

    sys.exit(app.exec())
