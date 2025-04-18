#include <QFile>
#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQuickItem>
#include <QQuickWindow>
#include <QRunnable>
#include <gst/gst.h>
#include <stdlib.h>

class SetPlaying : public QRunnable
{
public:
    SetPlaying(GstElement *);
    ~SetPlaying();

    void run();

private:
    GstElement *pipeline_;
};

SetPlaying::SetPlaying(GstElement *pipeline)
{
    this->pipeline_ = pipeline ? static_cast<GstElement *>(gst_object_ref(pipeline)) : NULL;
}

SetPlaying::~SetPlaying()
{
    if (this->pipeline_)
        gst_object_unref(this->pipeline_);
}

void SetPlaying::run()
{
    if (this->pipeline_)
        gst_element_set_state(this->pipeline_, GST_STATE_PLAYING);
}

int main(int argc, char *argv[])
{
    int ret;

    gst_init(&argc, &argv);

    QGuiApplication app(argc, argv);

    Q_INIT_RESOURCE(gstqml6_shaders);

    GstElement *pipeline = gst_pipeline_new(NULL);
    GstElement *src = gst_element_factory_make("videotestsrc", NULL);
    GstElement *glupload = gst_element_factory_make("glupload", NULL);
    /* the plugin must be loaded before loading the qml file to register the
     * GstGLVideoItem qml item */
    GstElement *sink = gst_element_factory_make("qml6glsink", NULL);

    g_assert(src && glupload && sink);

    gst_bin_add_many(GST_BIN(pipeline), src, glupload, sink, NULL);
    gst_element_link_many(src, glupload, sink, NULL);

    QQmlApplicationEngine engine;
    QObject::connect(
        &engine,
        &QQmlApplicationEngine::objectCreationFailed,
        &app,
        []() { QCoreApplication::exit(-1); },
        Qt::QueuedConnection);
    engine.loadFromModule("gstreamer-test", "Main");

    QQuickItem *videoItem;
    QQuickWindow *rootObject;

    /* find and set the videoItem on the sink */
    auto objs = engine.rootObjects();
    rootObject = static_cast<QQuickWindow *>(objs.first());
    videoItem = rootObject->findChild<QQuickItem *>("videoItem");
    g_assert(videoItem);
    g_object_set(sink, "widget", videoItem, NULL);

    rootObject->scheduleRenderJob(new SetPlaying(pipeline), QQuickWindow::BeforeSynchronizingStage);

    ret = app.exec();

    gst_element_set_state(pipeline, GST_STATE_NULL);
    gst_object_unref(pipeline);

    gst_deinit();

    return ret;
}
