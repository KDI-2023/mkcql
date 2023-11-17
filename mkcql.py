import os
import json
from copy import deepcopy as dcp
from testdb.const import *

dirname = os.path.dirname(os.path.abspath(os.path.expanduser(__file__)))

data = json.loads(open(
    os.path.join(dirname, 'testdb/uuid_all.json'),
    'rb'
).read())

f = open('jlutag.cql', 'wb')


def w(s: str) -> None:
    s = str(s)+'\n\n'
    f.write(s.encode('utf8'))


created = list()

for i in data:
    a = dcp(data[i])
    if a[TYPE] == ARTWORK:
        src = a[ALIAS][0]
        src_cql = "(src:Obj:Artwork {name: '%s'})" % src
        if src not in created:
            created.append(src)
            w("CREATE %s" % src_cql)
        for j in a[LINK]:
            for k in a[LINK][j]:
                dst = data[k][ALIAS][0]
                dst_cql = "(dst:Obj:Character {name: '%s'})" % dst
                if src in ['魔法禁书目录', '某科学的超电磁炮']:
                    if dst not in created:
                        created.append(dst)
                        w("CREATE %s" % dst_cql)
                else:
                    w("CREATE %s" % dst_cql)

                w('''MATCH %s
MATCH %s WHERE NOT EXISTS {MATCH (src2:Artwork)<-[]-(dst:Character)}
CREATE (src)<-[:_IN]-(dst)''' % (src_cql, dst_cql))
