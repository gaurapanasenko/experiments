import QtQuick 2.0
import QtMultimedia 5.15

Item {
    property bool trigger: true
    property alias mediaPlayer1: mediaPlayer1
    property alias mediaPlayer2: mediaPlayer2
    property var currentMediaPlayer: trigger ? mediaPlayer1 : mediaPlayer2
    property var nextMediaPlayer: trigger ? mediaPlayer2 : mediaPlayer1
    function next() {
        trigger = !trigger
    }

    VideoOutput {
        id: vo1
        anchors.fill: parent
        source: mediaPlayer1
        visible: trigger
    }

    VideoOutput {
        id: vo2
        anchors.fill: parent
        source: mediaPlayer2
        visible: !trigger
    }

    MediaPlayer {
       id: mediaPlayer1
       onErrorStringChanged: {
           console.log(errorString);
       }
       onPlaybackStateChanged: {
           console.log(playbackState, MediaPlayer.StoppedState)
           if (playbackState == MediaPlayer.StoppedState) {
               mediaPlayer2.play()
               next()
           }
       }
    }
    MediaPlayer {
       id: mediaPlayer2
    }
}
