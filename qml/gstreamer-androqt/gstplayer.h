#ifndef GSTPLAYER_H
#define GSTPLAYER_H

#include <QQmlApplicationEngine>
#include <QQuickItem>
#include <QtCore/private/qandroidextras_p.h>
#include <android/native_window.h>
#include <android/native_window_jni.h>
#include <gst/gst.h>

Q_DECLARE_OPAQUE_POINTER(ANativeWindow *)

class GstPlayer : public QObject
{
    Q_OBJECT
    QML_ELEMENT
    QML_UNCREATABLE("This class constructed by GstPlayerFactory")
    Q_PROPERTY(QString url READ url WRITE setUrl RESET resetUrl NOTIFY urlChanged FINAL)
    Q_PROPERTY(States playerState READ state NOTIFY stateChanged FINAL)
    Q_PROPERTY(
        bool playing READ playing WRITE setPlaying RESET resetPlaying NOTIFY playingChanged FINAL)
public:
    enum States { None, Ready, Paused, Playing };
    Q_ENUM(States)
    GstPlayer(QJniObject javaPlayer, QObject *parent = nullptr);
    ~GstPlayer();
    static void initGlobal();
    static void initJni(JNIEnv *env, jobject thiz);
    Q_DECLARE_JNI_NATIVE_METHOD_IN_CURRENT_SCOPE(initJni)
    static void releaseJni(JNIEnv *env, jobject thiz);
    Q_DECLARE_JNI_NATIVE_METHOD_IN_CURRENT_SCOPE(releaseJni)
    static void playJni(JNIEnv *env, jobject thiz);
    Q_DECLARE_JNI_NATIVE_METHOD_IN_CURRENT_SCOPE(playJni)
    static void pauseJni(JNIEnv *env, jobject thiz);
    Q_DECLARE_JNI_NATIVE_METHOD_IN_CURRENT_SCOPE(pauseJni)
    static void surfaceInitJni(JNIEnv *env, jobject thiz, jobject surface);
    Q_DECLARE_JNI_NATIVE_METHOD_IN_CURRENT_SCOPE(surfaceInitJni)
    static void surfaceReleaseJni(JNIEnv *env, jobject thiz);
    Q_DECLARE_JNI_NATIVE_METHOD_IN_CURRENT_SCOPE(surfaceReleaseJni)

    QString url() const;
    void setUrl(const QString &newUrl);
    void resetUrl();

    States state() const;

    int jniHash();

    Q_INVOKABLE void play();
    Q_INVOKABLE void pause();
    Q_INVOKABLE int getPosition();

    bool playing() const;
    void setPlaying(bool newPlaying);
    void resetPlaying();

private:
    void setState(States newState);
    void updateUri();
    void init();
    void initPipeline();
    void release();
    static void on_bus_message(GstBus *bus, GstMessage *msg, gpointer user_data);
    void surfaceInit(ANativeWindow *window);
    void surfaceRelease();
    void linkSurface();
    void resetPipeline();
    void processPlaying();
    void playPriv();
    void pausePriv();
    void updateSizes();

signals:
    void stateChanged();
    void urlChanged();
    void restart();
    void playSig();
    void pauseSig();
    void surfaceInitSig(ANativeWindow *window);
    void surfaceReleaseSig();
    void linked();

    void playingChanged();

private slots:
    void restartSlot();

private:
    QString m_url = "";
    States m_state = None;
    GstElement *m_pipeline = nullptr, *m_uriHolder = nullptr, *m_videoSink = nullptr,
               *m_videoOverlay = nullptr;
    QJniObject m_javaPlayer{};
    ANativeWindow *m_window = nullptr;
    quint64 busConnection = 0;
    bool m_playing = false;
};

#endif // GSTPLAYER_H
