import QtQuick 2.12
import QtQuick.Window 2.12

Window {
    id: root
    width: 640
    height: 480
    visible: true
    title: qsTr("Hello World")

    Row {
        Rectangle {
            height: root.height
            width: root.width / 2
            color: "red"
            MultiPointTouchArea {
                anchors.fill: parent
                onPressed: {
                    parent.color = "green"
                }
            }
            Timer {
                interval: 1000
                running: true
                repeat: true
                onTriggered: parent.color = "red"
            }
        }
        Rectangle {
            height: root.height
            width: root.width / 2
            color: "red"
            MultiPointTouchArea {
                id: ma
                anchors.fill: parent
                onPressed: {
                    parent.color = "green"
                }
            }
            Timer {
                interval: 1000
                running: true
                repeat: true
                onTriggered: {
                    ma.mouseEnabled = !ma.mouseEnabled
                    parent.color = "red"
                }
            }
        }
    }
}
