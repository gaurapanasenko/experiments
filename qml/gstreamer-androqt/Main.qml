import QtQuick
import gstreamer 1.0

Window {
    id:root
    width: 640
    height: 480
    visible: true
    // visibility: Window.FullScreen
    title: qsTr("Hello World")
    // property string url: "https://gstreamer.freedesktop.org/data/media/sintel_trailer-480p.webm"
    // property string url: "qrc:/test.mp4"
    property string url: "http://elfiny.top/file_example_MP4_1920_18MG.mp4"
    //http://elfiny.top/test.mp4
    property var timestamp: new Date().valueOf()

    Item {
        id: readyCounter
        property int count: 0
        onCountChanged: {
            if (count == 2) {
                player1.play()
                player2.play()
                root.timestamp = new Date().valueOf()
                readyCounter.destroy()
            }
        }
    }

    Timer {
        interval: 500
        running: true
        repeat: true
        onTriggered: {
            let cur = new Date().valueOf()
            let targPos = cur - root.timestamp
            let pos1 = player1.getPosition()
            let pos2 = player1.getPosition()
            let diff1 = targPos - pos1
            let diff2 = targPos - pos2
            text1.text = diff1 + "ms ," + diff2 + "ms"
        }
    }

    Row {
        anchors.fill: parent
        GstreamerPlayer {
            id: player1
            url: root.url
            height: parent.height
            width: parent.width / 2
            // visible: playerState === GstreamerPlayer.Playing
            transform: Matrix4x4 {
                matrix: Qt.matrix4x4( -1, 0, 0, player1.width, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)
            }
            Connections {
                target: player1
                function onPlayerStateChanged() {
                    if (player1.playerState === GstreamerPlayer.Paused) {
                        readyCounter.count++
                        destroy();
                    }
                }
            }
        }
        GstreamerPlayer {
            id: player2
            url: root.url
            height: parent.height
            width: parent.width / 2
            // visible: playerState === GstreamerPlayer.Playing
            Connections {
                target: player2
                function onPlayerStateChanged() {
                    if (player2.playerState === GstreamerPlayer.Paused) {
                        readyCounter.count++
                        destroy();
                    }
                }
            }
        }
    }

    Text {
        id: text1
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        font.pixelSize: 40
    }

    Timer {
        running: true
        interval: 15000
        repeat: true
        onTriggered: {
            player1.play()
            player2.play()
            root.timestamp = new Date().valueOf()
        }
    }
}
