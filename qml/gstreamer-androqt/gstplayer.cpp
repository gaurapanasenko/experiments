#include "gstplayer.h"
#include <QQmlComponent>
#include <QQmlProperty>
#include "gstplayerfactory.h"
#include <gst/video/video.h>

GstPlayer::GstPlayer(QJniObject javaPlayer, QObject *parent)
    : QObject{parent}
    , m_state(None)
    , m_pipeline(nullptr)
    , m_javaPlayer(javaPlayer)
{
    assert(m_javaPlayer.isValid());
    qDebug().nospace() << this << ": Creating object";
    resetUrl();
    init();
    connect(this, &GstPlayer::restart, this, &GstPlayer::restartSlot);
    connect(this, &GstPlayer::playSig, this, &GstPlayer::play);
    connect(this, &GstPlayer::pauseSig, this, &GstPlayer::pause);
    connect(this, &GstPlayer::surfaceInitSig, this, &GstPlayer::surfaceInit);
    connect(this, &GstPlayer::surfaceReleaseSig, this, &GstPlayer::surfaceRelease);
}

GstPlayer::~GstPlayer()
{
    qDebug().nospace() << this << ": Destructing object";
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
    qDebug().nospace() << "GstPlayer::initGlobal";
    qRegisterMetaType<ANativeWindow *>("ANativeWindow*");
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

void GstPlayer::surfaceInitJni(JNIEnv *env, jobject thiz, jobject surface)
{
    QJniObject qSurf(surface);
    assert(qSurf.isValid() && qSurf.callMethod<jboolean>("isValid"));
    ANativeWindow *window = ANativeWindow_fromSurface(env, surface);
    auto player = GstPlayerFactory::instance()->get(thiz);
    qDebug() << "Got window" << window << "for" << player;
    emit player->surfaceInitSig(window);
}

void GstPlayer::surfaceReleaseJni(JNIEnv *env, jobject thiz)
{
    emit GstPlayerFactory::instance()->get(thiz)->surfaceReleaseSig();
}

QString GstPlayer::url() const
{
    return m_url;
}

void GstPlayer::setUrl(const QString &newUrl)
{
    if (m_url == newUrl)
        return;
    qDebug().nospace() << this << ": Updating url to " << newUrl << " from " << m_url;
    m_url = newUrl;
    emit urlChanged();
    init();
    resetPipeline();
    updateUri();
}

void GstPlayer::resetUrl()
{
    setUrl("");
}

int GstPlayer::jniHash()
{
    return m_javaPlayer.callMethod<int>("hashCode");
}

GstPlayer::States GstPlayer::state() const
{
    return m_state;
}

void GstPlayer::play()
{
    setPlaying(true);
    init();
}

void GstPlayer::pause()
{
    setPlaying(false);
    init();
}

int GstPlayer::getPosition()
{
    gint64 pos = -1;
    if (m_pipeline && m_window && gst_element_query_position(m_pipeline, GST_FORMAT_TIME, &pos))
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
    if (!m_uriHolder)
        return;
    qDebug().nospace() << this << ": Updating URI " << m_url;
    QByteArray url = m_url.toLocal8Bit();
    const gchar *char_uri = url.data();
    g_object_set(m_uriHolder, "uri", char_uri, NULL);
}

void GstPlayer::init()
{
    initPipeline();
    linkSurface();
    processPlaying();
}

void GstPlayer::initPipeline()
{
    if (m_pipeline)
        return;

    qDebug().nospace() << this << ": Initing pipeline";

    auto str = "playbin";
    GError *error = NULL;
    GstElement *pipeline = gst_parse_launch(str, &error);
    if (error) {
        qWarning().nospace() << this << ": Failed to init pipeline: " << error->message;
        return;
    }
    if (pipeline == nullptr) {
        qWarning().nospace() << this << ": Failed to init pipeline";
        return;
    }
    gst_element_set_state(pipeline, GST_STATE_READY);
    GstElement *video_overlay = gst_bin_get_by_interface(GST_BIN(pipeline), GST_TYPE_VIDEO_OVERLAY);
    if (video_overlay == nullptr) {
        qWarning().nospace() << this << ": Failed get video sink from pipeline";
        gst_object_unref(pipeline);
        return;
    }
    // g_object_set(sink, "widget", m_videoItem, NULL);

    m_uriHolder = pipeline;
    m_pipeline = pipeline;
    m_videoSink = nullptr;
    m_videoOverlay = video_overlay;

    GstBus *bus = gst_element_get_bus(m_pipeline);
    gst_bus_add_signal_watch(bus);
    busConnection = g_signal_connect(bus, "message", G_CALLBACK(on_bus_message), this);
    gst_object_unref(bus);

    updateUri();

    linkSurface();

    gst_element_set_state(m_pipeline, GST_STATE_READY);
}

void GstPlayer::release()
{
    if (m_pipeline == nullptr)
        return;
    qDebug().nospace() << this << ": Releasing pipeline";
    gst_element_set_state(m_pipeline, GST_STATE_NULL);
    GstBus *bus = gst_element_get_bus(m_pipeline);
    g_signal_handler_disconnect(bus, busConnection);
    gst_object_unref(bus);
    gst_object_unref(m_pipeline);
    m_pipeline = nullptr;
    m_uriHolder = nullptr;
    m_videoSink = nullptr;
    m_videoOverlay = nullptr;
    m_state = None;
}

void GstPlayer::on_bus_message(GstBus *bus, GstMessage *msg, gpointer user_data)
{
    GstPlayer *player = static_cast<GstPlayer *>(user_data);
    GstElement *pipeline = player->m_pipeline;
    if (pipeline == nullptr)
        return;

    switch (GST_MESSAGE_TYPE(msg)) {
    case GST_MESSAGE_EOS:
        qDebug().nospace() << player << ": End of stream";
        emit player->restart();
        // gst_element_set_state(pipeline, GST_STATE_READY);
        break;
    case GST_MESSAGE_ERROR: {
        GError *err;
        gchar *debug;
        gst_message_parse_error(msg, &err, &debug);
        qDebug().nospace() << player << ": Error: " << err->message;
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
            auto old_name = gst_element_state_get_name(old_state),
                 new_name = gst_element_state_get_name(new_state),
                 pending_name = gst_element_state_get_name(pending_state);
            qDebug().nospace() << "Pipeline state changed to " << new_name << " from " << old_name
                               << " while " << pending_name;
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
                if (old_state == GST_STATE_READY) {
                    player->updateSizes();
                }
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
    qDebug().nospace() << this << ": Initing surface to " << window << " from " << m_window;
    if (m_window == window) {
        if (m_window != nullptr) {
            // Release new pointer
            ANativeWindow_release(window);
            // Update video sink
            if (m_videoOverlay != nullptr) {
                gst_video_overlay_expose(GST_VIDEO_OVERLAY(m_videoOverlay));
                gst_video_overlay_expose(GST_VIDEO_OVERLAY(m_videoOverlay));
            }
        }
        return;
    }
    m_window = window;
    linkSurface();
    //TODO: ready
    //TODO: surface init jni connect
}

void GstPlayer::surfaceRelease()
{
    if (m_window == nullptr)
        return;
    qDebug().nospace() << this << ": Releasing surface " << m_window;
    auto tmp = m_window;
    m_window = nullptr;
    linkSurface();
    ANativeWindow_release(tmp);
}

void GstPlayer::linkSurface()
{
    if (m_videoOverlay != nullptr) {
        qDebug().nospace() << this << ": Linking surface " << m_window << " to " << m_videoOverlay;
        gst_video_overlay_set_window_handle(GST_VIDEO_OVERLAY(m_videoOverlay), (guintptr) m_window);
        if (m_window == nullptr) {
            resetPipeline();
        } else {
            gst_video_overlay_expose(GST_VIDEO_OVERLAY(m_videoOverlay));
            gst_video_overlay_expose(GST_VIDEO_OVERLAY(m_videoOverlay));
        }
    }
}

void GstPlayer::resetPipeline()
{
    qDebug().nospace() << this << ": Reseting pipeline";
    if (m_pipeline)
        gst_element_set_state(m_pipeline, GST_STATE_READY);
}

void GstPlayer::processPlaying()
{
    if (playing())
        playPriv();
    else
        pausePriv();
}

void GstPlayer::playPriv()
{
    if (m_pipeline && m_videoOverlay && m_window) {
        qDebug().nospace() << this << ": Playing video";
        gst_element_set_state(m_pipeline, GST_STATE_PLAYING);
    }
}

void GstPlayer::pausePriv()
{
    if (m_pipeline && m_videoOverlay && m_window) {
        qDebug().nospace() << this << ": Pausing video";
        gst_element_set_state(m_pipeline, GST_STATE_PAUSED);
    }
}

void GstPlayer::updateSizes()
{
    /* Retrieve the Caps at the entrance of the video sink */
    GstElement *video_sink;
    g_object_get(m_pipeline, "video-sink", &video_sink, NULL);
    GstPad *video_sink_pad = gst_element_get_static_pad(video_sink, "sink");
    GstCaps *caps = gst_pad_get_current_caps(video_sink_pad);

    GstVideoInfo info;
    if (gst_video_info_from_caps(&info, caps)) {
        info.width = info.width * info.par_n / info.par_d;
        qDebug().nospace() << this << ": Media size is " << info.width << "x" << info.height;
        m_javaPlayer.callMethod<void>("onMediaSizeChanged", info.width, info.height);
    }

    gst_caps_unref(caps);
    gst_object_unref(video_sink_pad);
    gst_object_unref(video_sink);
}

void GstPlayer::restartSlot()
{
    release();
    init();
}

bool GstPlayer::playing() const
{
    return m_playing;
}

void GstPlayer::setPlaying(bool newPlaying)
{
    if (m_playing == newPlaying)
        return;
    m_playing = newPlaying;
    emit playingChanged();
}

void GstPlayer::resetPlaying()
{
    setPlaying({}); // TODO: Adapt to use your actual default value
}

Q_DECL_EXPORT jint JNICALL JNI_OnLoad(JavaVM *vm, void *reserved)
{
    QJniEnvironment env;
    auto methods = {
        Q_JNI_NATIVE_SCOPED_METHOD(initJni, GstPlayer),
        Q_JNI_NATIVE_SCOPED_METHOD(releaseJni, GstPlayer),
        Q_JNI_NATIVE_SCOPED_METHOD(playJni, GstPlayer),
        Q_JNI_NATIVE_SCOPED_METHOD(pauseJni, GstPlayer),
        Q_JNI_NATIVE_SCOPED_METHOD(surfaceInitJni, GstPlayer),
        Q_JNI_NATIVE_SCOPED_METHOD(surfaceReleaseJni, GstPlayer),
    };
    env.registerNativeMethods("top/elfiny/GstPlayer", methods);
    return JNI_VERSION_1_4;
}
