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

GstPlayer *GstPlayerFactory::get(jobject javaPlayer)
{
    if (!m_players.contains(javaPlayer)) {
        qDebug() << "Creating new player: " << javaPlayer;
        GstPlayer *player = new GstPlayer(javaPlayer);
        player->moveToThread(thread);
        connect(player, &QObject::destroyed, this, &GstPlayerFactory::release);
        m_players[javaPlayer] = player;
        return player;
    }
    return m_players[javaPlayer];
}

void GstPlayerFactory::release(QObject *player)
{
    jobject javaPlayer = qobject_cast<GstPlayer *>(player)->object();
    if (!m_players.contains(javaPlayer)) {
        m_players.remove(javaPlayer);
    }
}
