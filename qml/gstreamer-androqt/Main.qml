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
    property string url: "http://elfiny.top/test.mp4"
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
            let players = Array.from(GstPlayerFactory.players)
            let cur = new Date().valueOf()
            let targPos = cur - root.timestamp
            let pos = players.map((i) => (targPos - i.getPosition()) + "ms")
            text1.text = pos.join(", ")
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
        onTriggered: play()
    }

    function play() {
        console.log("Starting play");
        let players = Array.from(GstPlayerFactory.players)
        players.map((i) => {i.url = root.url});
        players.map((i) => {i.play()});
        root.timestamp = new Date().valueOf()
    }

    Timer {
        running: true
        interval: 1000
        onTriggered: play()
    }
}
