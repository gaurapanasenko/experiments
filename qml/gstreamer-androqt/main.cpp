#include <QFile>
#include <QGuiApplication>
#include <QProcessEnvironment>
#include <QQmlApplicationEngine>
#include <QQuickItem>
#include <QQuickWindow>
#include <QRunnable>
#include "gstplayer.h"
#include "gstplayerfactory.h"
#include <gst/gst.h>

int main_qt(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);
    GstPlayerFactory::instance(&app);
    GstPlayer::initGlobal();

    QJniEnvironment env;
    QJniObject activity = QJniObject(QNativeInterface::QAndroidApplication::context());
    activity.callMethod<void>("initPlayers");

    QQmlApplicationEngine engine;
    QObject::connect(
        &engine,
        &QQmlApplicationEngine::objectCreationFailed,
        &app,
        []() { QCoreApplication::exit(-1); },
        Qt::QueuedConnection);
    engine.loadFromModule("gstreamer", "Main");
    return app.exec();
}

int main(int argc, char *argv[])
{
    qputenv("GST_DEBUG_FILE",
            "/data/data/org.qtproject.example.appgstreamer_multiplay/cache/gst.log");
    gst_debug_set_default_threshold(GST_LEVEL_DEBUG);
    gst_init(&argc, &argv);
    int ret = main_qt(argc, argv);
    gst_deinit();
    return ret;
}
