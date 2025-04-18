import QtQuick
import org.freedesktop.gstreamer.Qt6GLVideoItem 1.0

Window {
    id:root
    width: 640
    height: 480
    visible: true
    title: qsTr("Hello World")
    //property string url: "file:///home/gaura/drv/gatabase/test.mp4"
    property string url: "qrc:/test.mp4"
    // property string url: "http://elfiny.top/test.mp4"
    //http://elfiny.top/test.mp4

    GstGLQt6VideoItem {
        id: video
        objectName: "videoItem"
        anchors.centerIn: parent
        width: parent.width
        height: parent.height
    }


    Timer {
        running: true
        interval: 15000
        repeat: true
        onTriggered: {
            hidetimer.start()
        }
    }

    MouseArea {
        id: playArea
        anchors.fill: parent
        onPressed: {
            hidetimer.start()
        }
    }
}
