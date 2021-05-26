import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.VirtualKeyboard 2.2
import QtMultimedia 5.15

Window {
    id: window
    width: 640
    height: 480
    visible: true
    title: qsTr("Hello World")

    MediaQueue {
        anchors.fill: parent
        id: md
        mediaPlayer1.source: "file:///home/gaura/ibx/2021-05-23 19-44-36.mp4"
        mediaPlayer2.source: "file:///home/gaura/ibx/2021-04-24 01-30-55.mp4"
    }

    MouseArea {
         id: playArea
         anchors.fill: parent
         onPressed:  {
             console.log("Starting")
             md.currentMediaPlayer.play()
         }
     }
}
