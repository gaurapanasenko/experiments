#ifndef GSTREAMERPLAYER_H
#define GSTREAMERPLAYER_H

#include <QQmlApplicationEngine>
#include <QQuickItem>
#include <gst/gst.h>

class GstreamerPlayer : public QQuickItem
{
    Q_OBJECT
    QML_ELEMENT
    Q_PROPERTY(QString url READ url WRITE setUrl RESET resetUrl NOTIFY urlChanged FINAL)
    Q_PROPERTY(States playerState READ state WRITE setState NOTIFY stateChanged FINAL)
public:
    enum States { None, Ready, Paused, Playing };
    Q_ENUM(States)
    GstreamerPlayer();
    ~GstreamerPlayer();
    static void initGlobal();
    static void setEngine(QQmlApplicationEngine *engine);

    QString url() const;
    void setUrl(const QString &newUrl);
    void resetUrl();

    States state() const;

    Q_INVOKABLE void play();
    Q_INVOKABLE int getPosition();

private:
    void setState(States newState);
    void updateUri();
    void init();
    void initItem();
    void initPipeline();
    void release();
    static void on_bus_message(GstBus *bus, GstMessage *msg, gpointer user_data);

signals:
    void stateChanged();

    void urlChanged();
    void restart();

public slots:
    void inited();

private slots:
    void restartSlot();

private:
    GstElement *m_pipeline, *m_uriHolder;
    QQuickItem *m_videoItem;
    QString m_url;
    States m_state;
    bool ready;
    quint64 busConnection;

    static QQmlApplicationEngine *myEngine;
};

#endif // GSTREAMERPLAYER_H
