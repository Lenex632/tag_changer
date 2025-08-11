# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTabWidget,
    QTextEdit, QToolButton, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(800, 600))
        MainWindow.setMaximumSize(QSize(800, 600))
        icon = QIcon()
        if QIcon.hasThemeIcon(QIcon.ThemeIcon.MediaTape):
            icon = QIcon.fromTheme(QIcon.ThemeIcon.MediaTape)
        else:
            icon.addFile(u".", QSize(), QIcon.Mode.Normal, QIcon.State.Off)

        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.main_tab = QWidget()
        self.main_tab.setObjectName(u"main_tab")
        self.verticalLayout_4 = QVBoxLayout(self.main_tab)
        self.verticalLayout_4.setSpacing(10)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_9)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.target_dir_field = QLineEdit(self.main_tab)
        self.target_dir_field.setObjectName(u"target_dir_field")
        self.target_dir_field.setTabletTracking(False)
        self.target_dir_field.setAutoFillBackground(False)
        self.target_dir_field.setClearButtonEnabled(False)

        self.gridLayout.addWidget(self.target_dir_field, 1, 0, 1, 1)

        self.label = QLabel(self.main_tab)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.target_dir_button = QToolButton(self.main_tab)
        self.target_dir_button.setObjectName(u"target_dir_button")

        self.gridLayout.addWidget(self.target_dir_button, 1, 1, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(10, 10, 10, 10)
        self.label_2 = QLabel(self.main_tab)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.artist_dir_field = QTextEdit(self.main_tab)
        self.artist_dir_field.setObjectName(u"artist_dir_field")

        self.gridLayout_2.addWidget(self.artist_dir_field, 1, 0, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout_2)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(10, 10, 10, 10)
        self.library_field = QComboBox(self.main_tab)
        self.library_field.setObjectName(u"library_field")

        self.gridLayout_3.addWidget(self.library_field, 1, 0, 1, 1)

        self.add_lib_button = QPushButton(self.main_tab)
        self.add_lib_button.setObjectName(u"add_lib_button")

        self.gridLayout_3.addWidget(self.add_lib_button, 1, 1, 1, 1)

        self.remove_lib_button = QPushButton(self.main_tab)
        self.remove_lib_button.setObjectName(u"remove_lib_button")

        self.gridLayout_3.addWidget(self.remove_lib_button, 1, 2, 1, 1)

        self.update_lib_checkbox = QCheckBox(self.main_tab)
        self.update_lib_checkbox.setObjectName(u"update_lib_checkbox")

        self.gridLayout_3.addWidget(self.update_lib_checkbox, 2, 0, 1, 3)

        self.label_4 = QLabel(self.main_tab)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 3)

        self.gridLayout_3.setColumnStretch(0, 2)
        self.gridLayout_3.setColumnStretch(1, 1)
        self.gridLayout_3.setColumnStretch(2, 1)

        self.verticalLayout_4.addLayout(self.gridLayout_3)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_8)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(10, 10, 10, 10)
        self.reset_button = QPushButton(self.main_tab)
        self.reset_button.setObjectName(u"reset_button")

        self.gridLayout_5.addWidget(self.reset_button, 0, 1, 1, 1)

        self.save_button = QPushButton(self.main_tab)
        self.save_button.setObjectName(u"save_button")

        self.gridLayout_5.addWidget(self.save_button, 0, 2, 1, 1)

        self.readme_button = QPushButton(self.main_tab)
        self.readme_button.setObjectName(u"readme_button")

        self.gridLayout_5.addWidget(self.readme_button, 0, 0, 1, 1)

        self.start_button = QPushButton(self.main_tab)
        self.start_button.setObjectName(u"start_button")

        self.gridLayout_5.addWidget(self.start_button, 0, 3, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout_5)

        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(1, 1)
        self.verticalLayout_4.setStretch(2, 2)
        self.verticalLayout_4.setStretch(3, 1)
        self.verticalLayout_4.setStretch(4, 1)
        self.tabWidget.addTab(self.main_tab, "")
        self.add_tab = QWidget()
        self.add_tab.setObjectName(u"add_tab")
        self.verticalLayout_2 = QVBoxLayout(self.add_tab)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_5)

        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(10, 10, 10, 10)
        self.to_dir_field = QLineEdit(self.add_tab)
        self.to_dir_field.setObjectName(u"to_dir_field")
        self.to_dir_field.setTabletTracking(False)
        self.to_dir_field.setAutoFillBackground(False)
        self.to_dir_field.setClearButtonEnabled(False)

        self.gridLayout_7.addWidget(self.to_dir_field, 1, 0, 1, 1)

        self.to_dir_button = QToolButton(self.add_tab)
        self.to_dir_button.setObjectName(u"to_dir_button")

        self.gridLayout_7.addWidget(self.to_dir_button, 1, 1, 1, 1)

        self.label_6 = QLabel(self.add_tab)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_7.addWidget(self.label_6, 0, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_7)

        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(10, 10, 10, 10)
        self.from_dir_field = QLineEdit(self.add_tab)
        self.from_dir_field.setObjectName(u"from_dir_field")
        self.from_dir_field.setTabletTracking(False)
        self.from_dir_field.setAutoFillBackground(False)
        self.from_dir_field.setClearButtonEnabled(False)

        self.gridLayout_8.addWidget(self.from_dir_field, 1, 0, 1, 1)

        self.label_7 = QLabel(self.add_tab)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_8.addWidget(self.label_7, 0, 0, 1, 1)

        self.from_dir_button = QToolButton(self.add_tab)
        self.from_dir_button.setObjectName(u"from_dir_button")

        self.gridLayout_8.addWidget(self.from_dir_button, 1, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_8)

        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(10, 10, 10, 10)
        self.add_lib_field = QComboBox(self.add_tab)
        self.add_lib_field.setObjectName(u"add_lib_field")

        self.gridLayout_6.addWidget(self.add_lib_field, 1, 0, 1, 1)

        self.label_5 = QLabel(self.add_tab)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_6.addWidget(self.label_5, 0, 0, 1, 2)

        self.gridLayout_6.setColumnStretch(0, 2)
        self.gridLayout_6.setColumnStretch(1, 1)

        self.verticalLayout_2.addLayout(self.gridLayout_6)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(10, 10, 10, 10)
        self.save_button_2 = QPushButton(self.add_tab)
        self.save_button_2.setObjectName(u"save_button_2")

        self.gridLayout_9.addWidget(self.save_button_2, 0, 2, 1, 1)

        self.start_button_2 = QPushButton(self.add_tab)
        self.start_button_2.setObjectName(u"start_button_2")

        self.gridLayout_9.addWidget(self.start_button_2, 0, 3, 1, 1)

        self.readme_button_2 = QPushButton(self.add_tab)
        self.readme_button_2.setObjectName(u"readme_button_2")

        self.gridLayout_9.addWidget(self.readme_button_2, 0, 0, 1, 1)

        self.reset_button_2 = QPushButton(self.add_tab)
        self.reset_button_2.setObjectName(u"reset_button_2")

        self.gridLayout_9.addWidget(self.reset_button_2, 0, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_9)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 1)
        self.verticalLayout_2.setStretch(4, 2)
        self.tabWidget.addTab(self.add_tab, "")
        self.duplicates_tab = QWidget()
        self.duplicates_tab.setObjectName(u"duplicates_tab")
        self.verticalLayout = QVBoxLayout(self.duplicates_tab)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.gridLayout_13 = QGridLayout()
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(10, 10, 10, 10)
        self.target_dir_button_3 = QToolButton(self.duplicates_tab)
        self.target_dir_button_3.setObjectName(u"target_dir_button_3")

        self.gridLayout_13.addWidget(self.target_dir_button_3, 1, 1, 1, 1)

        self.label_9 = QLabel(self.duplicates_tab)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_13.addWidget(self.label_9, 0, 0, 1, 1)

        self.duplicates_dir_field = QLineEdit(self.duplicates_tab)
        self.duplicates_dir_field.setObjectName(u"duplicates_dir_field")
        self.duplicates_dir_field.setTabletTracking(False)
        self.duplicates_dir_field.setAutoFillBackground(False)
        self.duplicates_dir_field.setClearButtonEnabled(False)

        self.gridLayout_13.addWidget(self.duplicates_dir_field, 1, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_13)

        self.gridLayout_12 = QGridLayout()
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(10, 10, 10, 10)
        self.label_8 = QLabel(self.duplicates_tab)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_12.addWidget(self.label_8, 0, 0, 1, 2)

        self.duplicates_lib_field = QComboBox(self.duplicates_tab)
        self.duplicates_lib_field.setObjectName(u"duplicates_lib_field")

        self.gridLayout_12.addWidget(self.duplicates_lib_field, 1, 0, 1, 1)

        self.gridLayout_12.setColumnStretch(0, 2)
        self.gridLayout_12.setColumnStretch(1, 1)

        self.verticalLayout.addLayout(self.gridLayout_12)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_7)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(10, 10, 10, 10)
        self.save_button_3 = QPushButton(self.duplicates_tab)
        self.save_button_3.setObjectName(u"save_button_3")

        self.gridLayout_10.addWidget(self.save_button_3, 0, 2, 1, 1)

        self.start_button_3 = QPushButton(self.duplicates_tab)
        self.start_button_3.setObjectName(u"start_button_3")

        self.gridLayout_10.addWidget(self.start_button_3, 0, 3, 1, 1)

        self.readme_button_3 = QPushButton(self.duplicates_tab)
        self.readme_button_3.setObjectName(u"readme_button_3")
        self.readme_button_3.setCheckable(False)
        self.readme_button_3.setChecked(False)
        self.readme_button_3.setAutoDefault(False)
        self.readme_button_3.setFlat(False)

        self.gridLayout_10.addWidget(self.readme_button_3, 0, 0, 1, 1)

        self.reset_button_3 = QPushButton(self.duplicates_tab)
        self.reset_button_3.setObjectName(u"reset_button_3")

        self.gridLayout_10.addWidget(self.reset_button_3, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_10)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(4, 2)
        self.tabWidget.addTab(self.duplicates_tab, "")
        self.sync_tab = QWidget()
        self.sync_tab.setObjectName(u"sync_tab")
        self.verticalLayout_3 = QVBoxLayout(self.sync_tab)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_6 = QSpacerItem(20, 63, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_6)

        self.gridLayout_14 = QGridLayout()
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(10, 10, 10, 10)
        self.label_10 = QLabel(self.sync_tab)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_14.addWidget(self.label_10, 0, 0, 1, 1)

        self.sync_dir_field_1 = QLineEdit(self.sync_tab)
        self.sync_dir_field_1.setObjectName(u"sync_dir_field_1")
        self.sync_dir_field_1.setTabletTracking(False)
        self.sync_dir_field_1.setAutoFillBackground(False)
        self.sync_dir_field_1.setClearButtonEnabled(False)

        self.gridLayout_14.addWidget(self.sync_dir_field_1, 1, 0, 1, 1)

        self.sync_dir_button_1 = QToolButton(self.sync_tab)
        self.sync_dir_button_1.setObjectName(u"sync_dir_button_1")

        self.gridLayout_14.addWidget(self.sync_dir_button_1, 1, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_14)

        self.gridLayout_15 = QGridLayout()
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(10, 10, 10, 10)
        self.sync_dir_field_2 = QLineEdit(self.sync_tab)
        self.sync_dir_field_2.setObjectName(u"sync_dir_field_2")
        self.sync_dir_field_2.setTabletTracking(False)
        self.sync_dir_field_2.setAutoFillBackground(False)
        self.sync_dir_field_2.setClearButtonEnabled(False)

        self.gridLayout_15.addWidget(self.sync_dir_field_2, 1, 0, 1, 1)

        self.label_11 = QLabel(self.sync_tab)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_15.addWidget(self.label_11, 0, 0, 1, 1)

        self.sync_dir_button_2 = QToolButton(self.sync_tab)
        self.sync_dir_button_2.setObjectName(u"sync_dir_button_2")

        self.gridLayout_15.addWidget(self.sync_dir_button_2, 1, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_15)

        self.gridLayout_16 = QGridLayout()
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(10, 10, 10, 10)
        self.label_14 = QLabel(self.sync_tab)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_16.addWidget(self.label_14, 2, 0, 1, 1)

        self.label_13 = QLabel(self.sync_tab)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_16.addWidget(self.label_13, 1, 0, 1, 1)

        self.label_12 = QLabel(self.sync_tab)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_16.addWidget(self.label_12, 0, 0, 1, 2)

        self.sync_lib_field_1 = QComboBox(self.sync_tab)
        self.sync_lib_field_1.setObjectName(u"sync_lib_field_1")

        self.gridLayout_16.addWidget(self.sync_lib_field_1, 1, 1, 1, 1)

        self.sync_lib_field_2 = QComboBox(self.sync_tab)
        self.sync_lib_field_2.setObjectName(u"sync_lib_field_2")

        self.gridLayout_16.addWidget(self.sync_lib_field_2, 2, 1, 1, 1)

        self.gridLayout_16.setColumnStretch(0, 1)
        self.gridLayout_16.setColumnStretch(1, 2)

        self.verticalLayout_3.addLayout(self.gridLayout_16)

        self.verticalSpacer = QSpacerItem(20, 129, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(10, 10, 10, 10)
        self.save_button_4 = QPushButton(self.sync_tab)
        self.save_button_4.setObjectName(u"save_button_4")

        self.gridLayout_11.addWidget(self.save_button_4, 0, 2, 1, 1)

        self.start_button_4 = QPushButton(self.sync_tab)
        self.start_button_4.setObjectName(u"start_button_4")

        self.gridLayout_11.addWidget(self.start_button_4, 0, 3, 1, 1)

        self.readme_button_4 = QPushButton(self.sync_tab)
        self.readme_button_4.setObjectName(u"readme_button_4")

        self.gridLayout_11.addWidget(self.readme_button_4, 0, 0, 1, 1)

        self.reset_button_4 = QPushButton(self.sync_tab)
        self.reset_button_4.setObjectName(u"reset_button_4")

        self.gridLayout_11.addWidget(self.reset_button_4, 0, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_11)

        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 1)
        self.verticalLayout_3.setStretch(2, 1)
        self.verticalLayout_3.setStretch(3, 2)
        self.verticalLayout_3.setStretch(4, 1)
        self.tabWidget.addTab(self.sync_tab, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.treeWidget = QTreeWidget(self.tab_5)
        __qtreewidgetitem = QTreeWidgetItem(self.treeWidget)
        QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem)
        __qtreewidgetitem1 = QTreeWidgetItem(self.treeWidget)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(self.treeWidget)
        QTreeWidgetItem(self.treeWidget)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setGeometry(QRect(410, 70, 256, 192))
        self.tabWidget_2 = QTabWidget(self.tab_5)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tabWidget_2.setGeometry(QRect(590, 290, 127, 191))
        self.tabWidget_2.setAutoFillBackground(False)
        self.tabWidget_2.setTabPosition(QTabWidget.North)
        self.tabWidget_2.setTabShape(QTabWidget.Rounded)
        self.tabWidget_2.setUsesScrollButtons(False)
        self.tabWidget_2.setDocumentMode(False)
        self.tabWidget_2.setTabsClosable(False)
        self.tabWidget_2.setMovable(False)
        self.tabWidget_2.setTabBarAutoHide(False)
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.tabWidget_2.addTab(self.tab_6, "")
        self.tab_7 = QWidget()
        self.tab_7.setObjectName(u"tab_7")
        self.tabWidget_2.addTab(self.tab_7, "")
        self.listWidget = QListWidget(self.tab_5)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(100, 150, 256, 192))
        self.listWidget.setDragEnabled(True)
        self.listWidget.setDragDropOverwriteMode(True)
        self.listWidget.setAlternatingRowColors(True)
        self.tabWidget.addTab(self.tab_5, "")

        self.verticalLayout_5.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 23))
        self.menubar.setDefaultUp(False)
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        self.statusBar.setMinimumSize(QSize(800, 22))
        self.statusBar.setMaximumSize(QSize(800, 22))
        self.statusBar.setSizeGripEnabled(False)
        MainWindow.setStatusBar(self.statusBar)
        QWidget.setTabOrder(self.tabWidget, self.target_dir_field)
        QWidget.setTabOrder(self.target_dir_field, self.artist_dir_field)
        QWidget.setTabOrder(self.artist_dir_field, self.library_field)
        QWidget.setTabOrder(self.library_field, self.update_lib_checkbox)
        QWidget.setTabOrder(self.update_lib_checkbox, self.reset_button)
        QWidget.setTabOrder(self.reset_button, self.save_button)
        QWidget.setTabOrder(self.save_button, self.start_button)
        QWidget.setTabOrder(self.start_button, self.add_lib_button)
        QWidget.setTabOrder(self.add_lib_button, self.remove_lib_button)
        QWidget.setTabOrder(self.remove_lib_button, self.readme_button)
        QWidget.setTabOrder(self.readme_button, self.to_dir_field)
        QWidget.setTabOrder(self.to_dir_field, self.add_lib_field)
        QWidget.setTabOrder(self.add_lib_field, self.to_dir_button)
        QWidget.setTabOrder(self.to_dir_button, self.from_dir_field)
        QWidget.setTabOrder(self.from_dir_field, self.from_dir_button)
        QWidget.setTabOrder(self.from_dir_button, self.save_button_2)
        QWidget.setTabOrder(self.save_button_2, self.start_button_2)
        QWidget.setTabOrder(self.start_button_2, self.readme_button_2)
        QWidget.setTabOrder(self.readme_button_2, self.reset_button_2)
        QWidget.setTabOrder(self.reset_button_2, self.duplicates_dir_field)
        QWidget.setTabOrder(self.duplicates_dir_field, self.target_dir_button_3)
        QWidget.setTabOrder(self.target_dir_button_3, self.duplicates_lib_field)
        QWidget.setTabOrder(self.duplicates_lib_field, self.save_button_3)
        QWidget.setTabOrder(self.save_button_3, self.start_button_3)
        QWidget.setTabOrder(self.start_button_3, self.readme_button_3)
        QWidget.setTabOrder(self.readme_button_3, self.reset_button_3)
        QWidget.setTabOrder(self.reset_button_3, self.sync_dir_field_1)
        QWidget.setTabOrder(self.sync_dir_field_1, self.sync_dir_button_1)
        QWidget.setTabOrder(self.sync_dir_button_1, self.sync_dir_field_2)
        QWidget.setTabOrder(self.sync_dir_field_2, self.sync_dir_button_2)
        QWidget.setTabOrder(self.sync_dir_button_2, self.sync_lib_field_1)
        QWidget.setTabOrder(self.sync_lib_field_1, self.sync_lib_field_2)
        QWidget.setTabOrder(self.sync_lib_field_2, self.save_button_4)
        QWidget.setTabOrder(self.save_button_4, self.start_button_4)
        QWidget.setTabOrder(self.start_button_4, self.readme_button_4)
        QWidget.setTabOrder(self.readme_button_4, self.reset_button_4)
        QWidget.setTabOrder(self.reset_button_4, self.treeWidget)
        QWidget.setTabOrder(self.treeWidget, self.tabWidget_2)
        QWidget.setTabOrder(self.tabWidget_2, self.listWidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.readme_button_3.setDefault(False)
        self.tabWidget_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Tag Changer", None))
        self.target_dir_field.setPlaceholderText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0423\u043a\u0430\u0436\u0438\u0442\u0435 \u043f\u0443\u0442\u044c \u043a \u0438\u0441\u0445\u043e\u0434\u043d\u043e\u0439 \u043f\u0430\u043f\u043a\u0435", None))
        self.target_dir_button.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u0423\u043a\u0430\u0436\u0438\u0442\u0435 \u043f\u0430\u043f\u043a\u0438 \u0441 \u0438\u0441\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044f\u043c\u0438 \u0434\u043b\u044f \u0423\u0440\u043e\u0432\u043d\u044f 2 (\u043a\u0430\u0436\u0434\u044b\u0439 \u0441 \u043d\u043e\u0432\u043e\u0439 \u0441\u0442\u0440\u043e\u043a\u0438)", None))
        self.add_lib_button.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.remove_lib_button.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.update_lib_checkbox.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c \u0431\u0430\u0437\u0443 \u0434\u0430\u043d\u043d\u044b\u0445 \u043e\u0441\u043d\u043e\u0432\u044b\u0432\u0430\u044f\u0441\u044c \u043d\u0430 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u0430\u043d\u043d\u044b\u0445 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0443, \u043b\u0438\u0431\u043e \u0441\u043e\u0437\u0434\u0430\u0439\u0442\u0435 \u0435\u0451", None))
        self.reset_button.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0431\u0440\u043e\u0441\u0438\u0442\u044c \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.save_button.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.readme_button.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c Readme", None))
        self.start_button.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0443\u0441\u043a ->", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.main_tab), QCoreApplication.translate("MainWindow", u"\u0418\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435 \u0442\u0435\u0433\u043e\u0432", None))
        self.to_dir_field.setPlaceholderText("")
        self.to_dir_button.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u0423\u043a\u0430\u0436\u0438\u0442\u0435 \u043f\u0430\u043f\u043a\u0443, \u0432 \u043a\u043e\u0442\u043e\u0440\u0443\u044e \u0445\u043e\u0442\u0438\u0442\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u0441\u0442\u0438\u0442\u044c \u043d\u043e\u0432\u044b\u0439 \u0444\u0430\u0439\u043b\u044b", None))
        self.from_dir_field.setPlaceholderText("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u0423\u043a\u0430\u0436\u0438\u0442\u0435 \u043f\u0430\u043f\u043a\u0443, \u0438\u0437 \u043a\u043e\u0442\u043e\u0440\u043e\u0439 \u0445\u043e\u0442\u0438\u0442\u0435 \u0437\u0430\u0431\u0440\u0430\u0442\u044c \u043d\u043e\u0432\u044b\u0435 \u0444\u0430\u0439\u043b\u044b", None))
        self.from_dir_button.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0443, \u0432 \u043a\u043e\u0442\u043e\u0440\u0443\u044e \u0434\u043e\u0431\u0430\u0432\u044f\u0442\u0441\u044f \u043d\u043e\u0432\u044b\u0435 \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u044b", None))
        self.save_button_2.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.start_button_2.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0443\u0441\u043a ->", None))
        self.readme_button_2.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c Readme", None))
        self.reset_button_2.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0431\u0440\u043e\u0441\u0438\u0442\u044c \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.add_tab), QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435", None))
        self.target_dir_button_3.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u0423\u043a\u0430\u0436\u0438\u0442\u0435 \u043f\u0430\u043f\u043a\u0443, \u0441\u0432\u044f\u0437\u0430\u043d\u043d\u0443\u044e \u0441 \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u043e\u0439", None))
        self.duplicates_dir_field.setPlaceholderText("")
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0443, \u0432 \u043a\u043e\u0442\u043e\u0440\u043e\u0439 \u0445\u043e\u0442\u0438\u0442\u0435 \u043d\u0430\u0439\u0442\u0438 \u0434\u0443\u0431\u043b\u0438\u043a\u0430\u0442\u044b", None))
        self.save_button_3.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.start_button_3.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0443\u0441\u043a ->", None))
        self.readme_button_3.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c Readme", None))
        self.reset_button_3.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0431\u0440\u043e\u0441\u0438\u0442\u044c \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.duplicates_tab), QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0438\u0441\u043a \u0434\u0443\u0431\u043b\u0438\u043a\u0430\u0442\u043e\u0432", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u0423\u043a\u0430\u0436\u0438\u0442\u0435 \u043f\u0443\u0442\u044c \u043a \u043f\u0430\u043f\u043a\u0435 1", None))
        self.sync_dir_field_1.setPlaceholderText("")
        self.sync_dir_button_1.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.sync_dir_field_2.setPlaceholderText("")
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u0423\u043a\u0430\u0436\u0438\u0442\u0435 \u043f\u0443\u0442\u044c \u043a \u043f\u0430\u043f\u043a\u0435 2", None))
        self.sync_dir_button_2.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"\u0411\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0430 \u043f\u0430\u043f\u043a\u0438 2", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\u0411\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0430 \u043f\u0430\u043f\u043a\u0438 1", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0438 \u0434\u043b\u044f \u0441\u0438\u043d\u0445\u0440\u043e\u043d\u0438\u0437\u0430\u0446\u0438\u0438", None))
        self.sync_lib_field_2.setPlaceholderText("")
        self.save_button_4.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.start_button_4.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0443\u0441\u043a ->", None))
        self.readme_button_4.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c Readme", None))
        self.reset_button_4.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0431\u0440\u043e\u0441\u0438\u0442\u044c \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.sync_tab), QCoreApplication.translate("MainWindow", u"\u0421\u0438\u043d\u0445\u0440\u043e\u043d\u0438\u0437\u0430\u0446\u0438\u044f", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"1", None));

        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.treeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u04421", None));
        ___qtreewidgetitem2 = ___qtreewidgetitem1.child(0)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u0434\u043e\u0447\u0435\u0440\u043d\u0438\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u044211", None));
        ___qtreewidgetitem3 = ___qtreewidgetitem1.child(1)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u0434\u043e\u0447\u0435\u0440\u043d\u0438\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u044212", None));
        ___qtreewidgetitem4 = ___qtreewidgetitem1.child(2)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u0434\u043e\u0447\u0435\u0440\u043d\u0438\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u044213", None));
        ___qtreewidgetitem5 = self.treeWidget.topLevelItem(1)
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u04422", None));
        ___qtreewidgetitem6 = ___qtreewidgetitem5.child(0)
        ___qtreewidgetitem6.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u0434\u043e\u0447\u0435\u0440\u043d\u0438\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u044221", None));
        ___qtreewidgetitem7 = ___qtreewidgetitem5.child(1)
        ___qtreewidgetitem7.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u0434\u043e\u0447\u0435\u0440\u043d\u0438\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u044222", None));
        ___qtreewidgetitem8 = self.treeWidget.topLevelItem(2)
        ___qtreewidgetitem8.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u04423", None));
        ___qtreewidgetitem9 = self.treeWidget.topLevelItem(3)
        ___qtreewidgetitem9.setText(0, QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u04424", None));
        self.treeWidget.setSortingEnabled(__sortingEnabled)

        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_7), QCoreApplication.translate("MainWindow", u"Tab 2", None))

        __sortingEnabled1 = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442", None));
        ___qlistwidgetitem1 = self.listWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442 1", None));
        ___qlistwidgetitem2 = self.listWidget.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u041d\u043e\u0432\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442 2", None));
        self.listWidget.setSortingEnabled(__sortingEnabled1)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"test", None))
    # retranslateUi

