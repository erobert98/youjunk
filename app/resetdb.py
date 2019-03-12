from app.models import *
from app import db

def reset():
    A = Article.query.all()
    for a in A:
        db.session.delete(a)
        db.session.commit()

    V = Video.query.all()
    for v in V:
        db.session.delete(v)
        db.session.commit()

    W = Website.query.all()
    for w in W:
        db.session.delete(w)
        db.session.commit()

    C = Channel.query.all()
    for c in C:
        db.session.delete(c)
        db.session.commit()