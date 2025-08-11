# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sync_dlg.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QHeaderView, QLabel, QSizePolicy,
    QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_SyncDlg(object):
    def setupUi(self, SyncDlg):
        if not SyncDlg.objectName():
            SyncDlg.setObjectName(u"SyncDlg")
        SyncDlg.resize(759, 500)
        self.gridLayout = QGridLayout(SyncDlg)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(SyncDlg)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)

        self.sync_dlg_tree_1 = QTreeWidget(SyncDlg)
        self.sync_dlg_tree_1.setObjectName(u"sync_dlg_tree_1")
        self.sync_dlg_tree_1.setAlternatingRowColors(True)
        self.sync_dlg_tree_1.setUniformRowHeights(True)
        self.sync_dlg_tree_1.setSortingEnabled(True)
        self.sync_dlg_tree_1.setWordWrap(True)
        self.sync_dlg_tree_1.setExpandsOnDoubleClick(False)
        self.sync_dlg_tree_1.setColumnCount(3)
        self.sync_dlg_tree_1.header().setProperty(u"showSortIndicator", True)

        self.gridLayout.addWidget(self.sync_dlg_tree_1, 1, 0, 1, 1)

        self.sync_dlg_tree_2 = QTreeWidget(SyncDlg)
        self.sync_dlg_tree_2.setObjectName(u"sync_dlg_tree_2")
        self.sync_dlg_tree_2.setAlternatingRowColors(True)
        self.sync_dlg_tree_2.setUniformRowHeights(True)
        self.sync_dlg_tree_2.setSortingEnabled(True)
        self.sync_dlg_tree_2.setWordWrap(True)
        self.sync_dlg_tree_2.setExpandsOnDoubleClick(False)
        self.sync_dlg_tree_2.setColumnCount(3)
        self.sync_dlg_tree_2.header().setProperty(u"showSortIndicator", True)

        self.gridLayout.addWidget(self.sync_dlg_tree_2, 1, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(SyncDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Apply|QDialogButtonBox.Cancel)

        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)


        self.retranslateUi(SyncDlg)
        self.buttonBox.accepted.connect(SyncDlg.accept)
        self.buttonBox.rejected.connect(SyncDlg.reject)

        QMetaObject.connectSlotsByName(SyncDlg)
    # setupUi

    def retranslateUi(self, SyncDlg):
        SyncDlg.setWindowTitle(QCoreApplication.translate("SyncDlg", u"\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u043f\u043e\u0438\u0441\u043a\u0430 \u0434\u043b\u044f \u0441\u0438\u043d\u0445\u0440\u043e\u043d\u0438\u0437\u0430\u0446\u0438\u0438", None))
        self.label.setText(QCoreApplication.translate("SyncDlg", u"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u043a\u0430\u043a\u0438\u0435 \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u044b \u0441\u0438\u043d\u0445\u0440\u043e\u043d\u0438\u0437\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0434\u043b\u044f \u043e\u0431\u0435\u0438\u0445 \u043f\u0430\u043f\u043a\u0430\u0445. \u041d\u0435\u043e\u0442\u043c\u0435\u0447\u0435\u043d\u043d\u044b\u0435 \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u044b \u0431\u0443\u0434\u0443\u0442 \u0443\u0434\u0430\u043b\u0435\u043d\u044b.", None))
        ___qtreewidgetitem = self.sync_dlg_tree_1.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("SyncDlg", u"\u041f\u0443\u0442\u044c", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("SyncDlg", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("SyncDlg", u"\u0418\u0441\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c", None));
        ___qtreewidgetitem1 = self.sync_dlg_tree_2.headerItem()
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("SyncDlg", u"\u041f\u0443\u0442\u044c", None));
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("SyncDlg", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("SyncDlg", u"\u0418\u0441\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c", None));
    # retranslateUi

