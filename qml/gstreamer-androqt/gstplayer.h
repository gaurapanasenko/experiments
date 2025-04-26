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
    Q_PROPERTY(QString url READ url WRITE setUrl RESET resetUrl NOTIFY urlChanged FINAL)
    Q_PROPERTY(States playerState READ state WRITE setState NOTIFY stateChanged FINAL)
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

    jobject object();

    Q_INVOKABLE void play();
    Q_INVOKABLE void pause();
    Q_INVOKABLE int getPosition();

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

signals:
    void stateChanged();
    void urlChanged();
    void restart();
    void playSig();
    void pauseSig();
    void surfaceInitSig(ANativeWindow *window);
    void surfaceReleaseSig();

private slots:
    void restartSlot();

private:
    QString m_url = "";
    States m_state = None;
    GstElement *m_pipeline = nullptr, *m_uriHolder = nullptr, *m_videoSink = nullptr;
    QJniObject m_javaPlayer{};
    ANativeWindow *m_window = nullptr;
    quint64 busConnection = 0;
};

#endif // GSTPLAYER_H
