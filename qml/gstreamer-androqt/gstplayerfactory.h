#ifndef GSTPLAYERFACTORY_H
#define GSTPLAYERFACTORY_H

#include <QHash>
#include <QObject>
#include <QQmlEngine>
#include <QtCore/private/qandroidextras_p.h>
#include "gstplayer.h"

class GstPlayerFactory : public QObject
{
    Q_OBJECT
    QML_ELEMENT
private:
    explicit GstPlayerFactory(QObject *parent = nullptr);
    ~GstPlayerFactory();

public:
    static GstPlayerFactory *instance(QObject *parent = nullptr);
    GstPlayer *get(jobject javaPlayer);

private:
    void release(QObject *player);

    static GstPlayerFactory *m_instance;
    QHash<jobject, GstPlayer *> m_players = {};
    QThread *thread = nullptr;
};

#endif // GSTPLAYERFACTORY_H
