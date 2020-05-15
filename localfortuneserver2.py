#!/usr/bin/env python


import random

from PyQt4 import QtCore, QtGui, QtNetwork


class Server(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Server, self).__init__(parent)

        statusLabel = QtGui.QLabel()
        quitButton = QtGui.QPushButton("Quit")
        quitButton.setAutoDefault(False)

        self.fortunes = (
            "You've been leading a dog's life. Stay off the furniture.",
            "You've got to think about tomorrow.",
            "You will be surprised by a loud noise.",
            "You will feel hungry again in another hour.",
            "You might have mail.",
            "You cannot kill time without injuring eternity.",
            "Computers are not intelligent. They only think they are.",
        )

        self.server = QtNetwork.QLocalServer()
        if not self.server.listen('fortune'):
            QtGui.QMessageBox.critical(self, "Fortune Server",
                    "Unable to start the server: %s." % self.server.errorString())
            self.close()
            return

        statusLabel.setText("The server is running.\nRun the Fortune Client "
                "example now.")

        quitButton.clicked.connect(self.close)
        self.server.newConnection.connect(self.sendFortune)

        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(quitButton)
        buttonLayout.addStretch(1)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(statusLabel)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

        self.setWindowTitle("Fortune Server")

    def sendFortune(self):
        block = QtCore.QByteArray()
        out = QtCore.QDataStream(block, QtCore.QIODevice.WriteOnly)
        out.setVersion(QtCore.QDataStream.Qt_4_0)
        out.writeUInt16(0)
        out.writeQString(random.choice(self.fortunes))
        out.device().seek(0)
        out.writeUInt16(block.size() - 2)

        clientConnection = self.server.nextPendingConnection()
        clientConnection.disconnected.connect(clientConnection.deleteLater)
        clientConnection.write(block)
        clientConnection.flush()
        clientConnection.disconnectFromServer()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    server = Server()
    server.show()
    sys.exit(app.exec_())