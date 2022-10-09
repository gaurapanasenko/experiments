import QtQuick 2.15
import QtQuick.Window 2.15

Window {
    width: 1280
    height: 720
    visible: true
    title: qsTr("Hello World")

    Scene {
        anchors.fill: parent
        /*PropertyAnimation on myX {
            loops: Animation.Infinite
            from: 360
            to: 0
            duration: 4000
        }*/


        SequentialAnimation on backSizeCoef {
            loops: Animation.Infinite
            PropertyAnimation {
                from: 0.5
                to: 2
                duration: 2000
                easing.type: Easing.InOutQuad
            }
            PropertyAnimation {
                from: 2
                to: 0.5
                duration: 2000
                easing.type: Easing.InOutQuad
            }
        }

    }
}
