# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'duplicates_dlg.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QHeaderView, QLabel, QSizePolicy,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_DuplicatesDlg(object):
    def setupUi(self, DuplicatesDlg):
        if not DuplicatesDlg.objectName():
            DuplicatesDlg.setObjectName(u"DuplicatesDlg")
        DuplicatesDlg.resize(700, 500)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DuplicatesDlg.sizePolicy().hasHeightForWidth())
        DuplicatesDlg.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(DuplicatesDlg)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.label = QLabel(DuplicatesDlg)
        self.label.setObjectName(u"label")
        self.label.setMouseTracking(False)

        self.verticalLayout.addWidget(self.label)

        self.duplicates_dlg_tree = QTreeWidget(DuplicatesDlg)
        self.duplicates_dlg_tree.setObjectName(u"duplicates_dlg_tree")
        font = QFont()
        font.setPointSize(10)
        self.duplicates_dlg_tree.setFont(font)
        self.duplicates_dlg_tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.duplicates_dlg_tree.setAlternatingRowColors(True)
        self.duplicates_dlg_tree.setSortingEnabled(True)
        self.duplicates_dlg_tree.setWordWrap(True)
        self.duplicates_dlg_tree.setExpandsOnDoubleClick(False)
        self.duplicates_dlg_tree.header().setProperty(u"showSortIndicator", True)

        self.verticalLayout.addWidget(self.duplicates_dlg_tree)

        self.buttonBox = QDialogButtonBox(DuplicatesDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setMouseTracking(False)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Apply|QDialogButtonBox.Cancel)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(DuplicatesDlg)
        self.buttonBox.accepted.connect(DuplicatesDlg.accept)
        self.buttonBox.rejected.connect(DuplicatesDlg.reject)

        QMetaObject.connectSlotsByName(DuplicatesDlg)
    # setupUi

    def retranslateUi(self, DuplicatesDlg):
        DuplicatesDlg.setWindowTitle(QCoreApplication.translate("DuplicatesDlg", u"\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u043f\u043e\u0438\u0441\u043a\u0430 \u0434\u0443\u0431\u043b\u0438\u043a\u0430\u0442\u043e\u0432", None))
        self.label.setText(QCoreApplication.translate("DuplicatesDlg", u"\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b \u043f\u043e\u0438\u0441\u043a\u0430 \u0434\u0443\u0431\u043b\u0438\u043a\u0430\u0442\u043e\u0432. \u041e\u0442\u043c\u0435\u0442\u044c\u0435 \u0442\u0435, \u0447\u0442\u043e \u0445\u043e\u0442\u0438\u0442\u0435 \u0443\u0434\u0430\u043b\u0438\u0442\u044c.", None))
        ___qtreewidgetitem = self.duplicates_dlg_tree.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("DuplicatesDlg", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("DuplicatesDlg", u"\u0418\u0441\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c/#", None));
    # retranslateUi

