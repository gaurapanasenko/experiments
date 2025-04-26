#include "gstplayerfactory.h"
#include <QThread>

GstPlayerFactory *GstPlayerFactory::m_instance = nullptr;

GstPlayerFactory::GstPlayerFactory(QObject *parent)
    : QObject{parent}
    , m_players{}
    , thread{new QThread(this)}
{
    m_instance = this;
    thread->start();
}

GstPlayerFactory::~GstPlayerFactory()
{
    m_instance = nullptr;
    const auto list = m_players.values();
    for (auto i : list) {
        i->deleteLater();
    }
    thread->quit();
    thread->wait();
}

GstPlayerFactory *GstPlayerFactory::instance(QObject *parent)
{
    if (m_instance == nullptr) {
        m_instance = new GstPlayerFactory(parent);
    }
    return m_instance;
}

GstPlayerFactory *GstPlayerFactory::create(QQmlEngine *qmlEngine, QJSEngine *)
{
    return instance(qmlEngine);
}

GstPlayer *GstPlayerFactory::get(jobject javaPlayer)
{
    QJniObject jPlayer(javaPlayer);
    int hash = jPlayer.callMethod<int>("hashCode");
    if (!m_players.contains(hash)) {
        qDebug() << "Creating new player:" << hash << ". New size:" << m_players.size() + 1;
        GstPlayer *player = new GstPlayer(jPlayer);
        player->moveToThread(thread);
        connect(player, &QObject::destroyed, this, &GstPlayerFactory::release);
        m_players[hash] = player;
        emit playersChanged();
        return player;
    }
    return m_players[hash];
}

QList<GstPlayer *> GstPlayerFactory::players()
{
    return m_players.values();
}

void GstPlayerFactory::release(QObject *player)
{
    int javaPlayer = qobject_cast<GstPlayer *>(player)->jniHash();
    if (!m_players.contains(javaPlayer)) {
        m_players.remove(javaPlayer);
    }
}
