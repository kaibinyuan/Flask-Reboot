#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb as mysql


class UserDB:
    def __init__(self):
        self.host = 'localhost'
        self.port = '3306'
        self.user = 'root'
        self.password = '123456'
        self.db = 'reboot'

        self.conn = mysql.connect(host=self.host,
                                  user=self.user,
                                  passwd=self.password,
                                  db=self.db, charset="utf8")
        self.conn.autocommit(True)
        self.curs = self.conn.cursor()

    def userlist(self, fields):
        curs = self.curs
        sql = "select %s from users" % ",".join(fields)
        curs.execute(sql)
        result = curs.fetchall()
        u_list = [dict((k, row[i]) for i, k in enumerate(fields)) for row in result]
        return u_list

    def getone(self, where):
        curs = self.curs
        fields = ["id", "name", "name_cn", "mobile", "email", "role", "status"]
        condition = '%s = "%s"' % (where.keys()[0], where.values()[0])
        sql = "select %s from users where %s" % (",".join(fields), condition)
        curs.execute(sql)
        result = curs.fetchone()
        u_dict = dict((k, result[i])for i, k in enumerate(fields))
        return u_dict

    def modfiy(self, fields):
        curs = self.curs
        conn = self.conn
        data = ",".join(["%s='%s'" % (k, v) for k, v in fields.items()])
        sql = "update users set %s where id=%s " % (data, fields["id"])
        curs.execute(sql)
        conn.commit()

    def adduser(self, fields):
        curs = self.curs
        conn = self.conn
        sql = "insert into users(%s)values('%s')" % (",".join(fields.keys()), "','".join(fields.values()))
        curs.execute(sql)
        conn.commit()

    def delete(self, uid):
        curs = self.curs
        conn = self.conn
        sql = "delete from users where id=%s" % uid
        curs.execute(sql)
        conn.commit()

    def checkuser(self, dict,fields):
        curs = self.curs
        sql = "select %s from users where %s='%s'" % (','.join(fields), dict.keys()[0], dict.values()[0])
        curs.execute(sql)
        result = curs.fetchone()
        #res = dict((k, result[i]) for i, k in enumerate(fields))
        if result:
            res = {}
            for i, k in enumerate(fields):
                res[k] = result[i]
            return res
        else:
            res = ""
            return res

    def modpasswd(self, dict):
        sql = "update users set password='%(password)s' where id=%(id)s" % dict
        curs = self.curs
        conn = self.conn
        curs.execute(sql)
        conn.commit()


if __name__ == "__main__":
    where = {"name": "kaibinyuan"}
    field = ["name", "passowrd", "email", "mobile"]
    db = UserDB()
    db.getone(where)
    db.userlist(field)

