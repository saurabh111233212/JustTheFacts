from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB

db = SQLAlchemy()

fact_entity = db.Table('fact_entity',
                       db.Column('entity_id', db.Integer, db.ForeignKey('entity.id'), primary_key=True),
                       db.Column('fact_id', db.Integer, db.ForeignKey('fact.id'), primary_key=True))


class Entity(db.Model):
    __table_name__ = 'entity'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class Fact(db.Model):
    __tablename__ = 'fact'
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'))
    text = db.Column(db.Text)
    entities = db.relationship('Entity', secondary=fact_entity, backref='facts')
    created_timestamp = db.Column(db.DateTime)

class Source(db.Model):
    __tablename__ = 'source'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    created_timestamp = db.Column(db.DateTime, server_default=db.func.now())
    published_timestamp = db.Column(db.DateTime)
    info = db.Column(JSONB, nullable=True)
