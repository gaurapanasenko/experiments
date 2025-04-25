#include "gstplayer.h"
#include <QQmlComponent>
#include <QQmlProperty>
#include "gstplayerfactory.h"

GstPlayer::GstPlayer(QJniObject javaPlayer, QObject *parent)
    : QObject{parent}
    , m_pipeline(nullptr)
    , m_javaPlayer(javaPlayer)
    , m_state(None)
{
    assert(m_javaPlayer.isValid());
    resetUrl();
    init();
    connect(this, &GstPlayer::restart, this, &GstPlayer::restartSlot);
    connect(this, &GstPlayer::playSig, this, &GstPlayer::play);
    connect(this, &GstPlayer::pauseSig, this, &GstPlayer::pause);
    ready = true;
}

GstPlayer::~GstPlayer()
{
    release();
}

static void set_rank_factory(const gchar *name, guint rank)
{
    GstRegistry *registry = NULL;
    GstElementFactory *factory = NULL;

    registry = gst_registry_get();
    if (!registry)
        return;

    factory = gst_element_factory_find(name);
    if (!factory)
        return;

    gst_plugin_feature_set_rank(GST_PLUGIN_FEATURE(factory), rank);

    gst_registry_add_feature(registry, GST_PLUGIN_FEATURE(factory));
    return;
}

void GstPlayer::initGlobal()
{
    set_rank_factory("vaapidecodebin", 257);
    set_rank_factory("androidmedia", 257);
    set_rank_factory("amc", 257);
}

void GstPlayer::initJni(JNIEnv *env, jobject thiz)
{
    GstPlayerFactory::instance()->get(thiz);
}

void GstPlayer::releaseJni(JNIEnv *env, jobject thiz)
{
    GstPlayerFactory::instance()->get(thiz)->deleteLater();
}

void GstPlayer::playJni(JNIEnv *env, jobject thiz)
{
    emit GstPlayerFactory::instance()->get(thiz)->playSig();
}

void GstPlayer::pauseJni(JNIEnv *env, jobject thiz)
{
    emit GstPlayerFactory::instance()->get(thiz)->pauseSig();
}

QString GstPlayer::url() const
{
    return m_url;
}

void GstPlayer::setUrl(const QString &newUrl)
{
    if (m_url == newUrl)
        return;
    m_url = newUrl;
    emit urlChanged();
    init();
    if (m_pipeline && ready)
        gst_element_set_state(m_pipeline, GST_STATE_READY);
    updateUri();
}

void GstPlayer::resetUrl()
{
    setUrl("");
}

jobject GstPlayer::object()
{
    return m_javaPlayer.object();
}

GstPlayer::States GstPlayer::state() const
{
    return m_state;
}

void GstPlayer::play()
{
    init();
    if (m_pipeline && ready) {
        gst_element_set_state(m_pipeline, GST_STATE_PLAYING);
    }
}

void GstPlayer::pause()
{
    init();
    if (m_pipeline && ready) {
        gst_element_set_state(m_pipeline, GST_STATE_PAUSED);
    }
}

int GstPlayer::getPosition()
{
    gint64 pos = -1;
    if (m_pipeline && ready && gst_element_query_position(m_pipeline, GST_FORMAT_TIME, &pos))
        return pos / 1000000;
    return -1;
}

void GstPlayer::setState(States newState)
{
    if (m_state == newState)
        return;
    m_state = newState;
    emit stateChanged();
}

void GstPlayer::updateUri()
{
    init();
    if (!m_uriHolder || !ready)
        return;
    QByteArray url = m_url.toLocal8Bit();
    const gchar *char_uri = url.data();
    g_object_set(m_uriHolder, "uri", char_uri, NULL);
    qDebug() << "Set new URI" << url;
}

void GstPlayer::init()
{
    initPipeline();
}

void GstPlayer::initPipeline()
{
    if (m_pipeline || !ready)
        return;

    bool error = false;

    // GstElement *glupload = gst_element_factory_make("glupload", NULL);
    // if (!glupload) {
    //     qWarning() << "Can't create glupload";
    //     return;
    // }
    GstElement *sink = gst_element_factory_make("qml6glsink", NULL);
    if (!sink) {
        qWarning() << "Can't create qml6glsink";
        // gst_object_unref(glupload);
        return;
    }
    // g_object_set(sink, "widget", m_videoItem, NULL);

    // GstElement *bin = gst_bin_new(NULL);
    // if (!bin) {
    //     qWarning() << "Can't create bin";
    //     gst_object_unref(glupload);
    //     gst_object_unref(sink);
    //     return;
    // }
    // gst_bin_add_many(GST_BIN(bin), glupload, sink, NULL);
    // if (!gst_element_link(glupload, sink)) {
    //     qWarning() << "Failed to link glupload and glimagesink";
    //     gst_object_unref(bin);
    //     return;
    // }

    // {
    //     GstPad *pad = gst_element_get_static_pad(sink, "sink");
    //     gst_element_add_pad(sink, gst_ghost_pad_new("sink", pad));
    //     gst_object_unref(pad);
    // }

    GstElement *pipeline = gst_element_factory_make("playbin", NULL);
    if (!pipeline) {
        qWarning() << "Failed to create playbin";
        gst_object_unref(sink);
        return;
    }
    g_object_set(pipeline, "video-sink", sink, NULL);

    // auto str = "playbin name=source video-sink=\"glupload ! qml6glsink name=videosink \"";
    // GstElement *pipeline = gst_parse_launch(str, nullptr);
    // GstElement *uridecodebin = gst_bin_get_by_name(GST_BIN(pipeline), "source");
    // GstElement *midbin;
    // g_object_get(uridecodebin, "video-sink", &midbin, NULL);
    // GstElement *sink = gst_bin_get_by_name(GST_BIN(midbin), "videosink");
    // g_object_set(sink, "widget", m_videoItem, NULL);

    m_uriHolder = pipeline;
    m_pipeline = pipeline;

    GstBus *bus = gst_element_get_bus(m_pipeline);
    gst_bus_add_signal_watch(bus);
    busConnection = g_signal_connect(bus, "message", G_CALLBACK(on_bus_message), this);
    gst_object_unref(bus);

    updateUri();

    gst_element_set_state(m_pipeline, GST_STATE_PAUSED);
}

void GstPlayer::release()
{
    if (m_pipeline != nullptr) {
        gst_element_set_state(m_pipeline, GST_STATE_NULL);
        GstBus *bus = gst_element_get_bus(m_pipeline);
        g_signal_handler_disconnect(bus, busConnection);
        gst_object_unref(bus);
        gst_object_unref(m_pipeline);
        m_pipeline = nullptr;
        m_uriHolder = nullptr;
        m_state = None;
    }
}

void GstPlayer::on_bus_message(GstBus *bus, GstMessage *msg, gpointer user_data)
{
    GstPlayer *player = static_cast<GstPlayer *>(user_data);
    GstElement *pipeline = player->m_pipeline;
    if (pipeline == nullptr)
        return;

    switch (GST_MESSAGE_TYPE(msg)) {
    case GST_MESSAGE_EOS:
        g_print("End of stream\n");
        emit player->restart();
        // gst_element_set_state(pipeline, GST_STATE_READY);
        break;
    case GST_MESSAGE_ERROR: {
        GError *err;
        gchar *debug;
        gst_message_parse_error(msg, &err, &debug);
        g_printerr("Error: %s\n", err->message);
        g_error_free(err);
        g_free(debug);
        gst_element_set_state(pipeline, GST_STATE_NULL);
        player->release();
        break;
    case GST_MESSAGE_STATE_CHANGED:
        /* We are only interested in state-changed messages from the pipeline */
        if (GST_MESSAGE_SRC(msg) == GST_OBJECT(pipeline)) {
            GstState old_state, new_state, pending_state;
            gst_message_parse_state_changed(msg, &old_state, &new_state, &pending_state);
            g_print("Pipeline state changed from %s to %s while %s:\n",
                    gst_element_state_get_name(old_state),
                    gst_element_state_get_name(new_state),
                    gst_element_state_get_name(pending_state));
            switch (new_state) {
            case GST_STATE_NULL:
                player->setState(None);
                break;
            case GST_STATE_READY:
                player->setState(Ready);
                gst_element_set_state(pipeline, GST_STATE_PAUSED);
                break;
            case GST_STATE_PAUSED:
                player->setState(Paused);
                break;
            case GST_STATE_PLAYING:
                player->setState(Playing);
                break;
            default:
                player->setState(None);
                break;
            }
        }
        break;
    }

    default:
        break;
    }
}

void GstPlayer::surfaceInit(ANativeWindow *window)
{
    if (m_window != nullptr) {
        ANativeWindow_release(m_window);
        if (m_window == window) {
            if (video_sink) {
                gst_video_overlay_expose(GST_VIDEO_OVERLAY(video_sink));
                gst_video_overlay_expose(GST_VIDEO_OVERLAY(video_sink));
            }
            return;
        }
    }
    m_window = window;
    ready = true;
    //TODO: check init completed
    //TODO: ready
    //TODO: surface release
    //TODO: surface init jni connect
}

void GstPlayer::inited()
{
    qInfo() << "Inited GstreamerPlayer!";
    ready = true;
    initPipeline();
    updateUri();
}

void GstPlayer::restartSlot()
{
    release();
    init();
    init();
}

Q_DECL_EXPORT jint JNICALL JNI_OnLoad(JavaVM *vm, void *reserved)
{
    QJniEnvironment env;
    auto methods = {
        Q_JNI_NATIVE_SCOPED_METHOD(initJni, GstPlayer),
        Q_JNI_NATIVE_SCOPED_METHOD(releaseJni, GstPlayer),
        Q_JNI_NATIVE_SCOPED_METHOD(playJni, GstPlayer),
        Q_JNI_NATIVE_SCOPED_METHOD(pauseJni, GstPlayer),
    };
    env.registerNativeMethods("top/elfiny/GstPlayer", methods);
}
