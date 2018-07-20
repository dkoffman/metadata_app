from sqlalchemy import Column, Integer, Text, String, ForeignKey
from sqlalchemy.orm import relationship

from ffmeta.models.db import Base


class Variable(Base):
    __tablename__ = "variable"

    # Define table fields
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    label = Column(Text)
    old_name = Column(Text)
    data_type = Column(Text)
    type = Column(Text)
    warning = Column(Integer)
    group_id = Column(Text)
    group_subid = Column(Text)
    data_source = Column(Text)
    respondent = Column(Text)
    wave = Column(Text)
    wave2 = Column(Text)
    scope = Column(Text)
    section = Column(Text)
    leaf = Column(Text)
    measures = Column(Text)
    probe = Column(Text)
    qText = Column(Text)
    survey = Column(Text)
    survey2 = Column(Text)

    fp_fchild = Column(Integer)
    fp_mother = Column(Integer)
    fp_father = Column(Integer)
    fp_PCG = Column(Integer)
    fp_partner = Column(Integer)
    fp_other = Column(Integer)

    focal_person = Column(Text)

    responses = relationship('Response', backref='variable')
    topics = relationship('Topic', backref='variable')

    def __init__(self, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

    def __repr__(self):
        return "<Variable %r>" % self.name

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "label": self.label,
            "old_name": self.old_name,
            "data_type": self.data_type,
            "warning": self.warning,
            "group_id": self.group_id,
            "group_subid": self.group_subid,
            "data_source": self.data_source,
            "respondent": self.respondent,
            "wave": self.wave,
            "scope": self.scope,
            "section": self.section,
            "leaf": self.leaf
        }

    def focal_people(self):
        """Return a list of focal person/people for this variable"""
        attr_to_str = {
            'fp_fchild': 'Focal Child',
            'fp_mother': 'Mother',
            'fp_father': 'Father',
            'fp_PCG': 'Primary Caregiver',
            'fp_partner': 'Partner',
            'fp_other': 'Other'
        }

        return [attr_to_str[attr] for attr in attr_to_str if getattr(self, attr) == 1]

    def focal_people_string(self):
        """A string representation of focal person/people, suitable for display in templates"""
        fp = self.focal_people()
        return ', '.join(fp) if fp else 'None'


class Topic(Base):
    __tablename__ = "topic"

    id = Column(Integer, primary_key=True)
    name = Column(Text, ForeignKey("variable.name"))
    topic = Column(Text)

    umbrella = relationship('Umbrella', backref='topic_obj', uselist=False)

    def __init__(self, name, topic):
        self.name = name
        self.topic = topic

    def __repr__(self):
        return "<Topic %r>" % self.topic

    def __str__(self):
        return self.topic


class Umbrella(Base):
    __tablename__ = "umbrella"

    id = Column(Integer, primary_key=True)
    topic = Column(Text, ForeignKey("topic.topic"))
    umbrella = Column(Text)

    def __init__(self, topic, umbrella):
        self.topic = topic
        self.umbrella = umbrella

    def __repr__(self):
        return "<Umbrella %r>" % self.umbrella

    def __str__(self):
        return self.umbrella


class Response(Base):
    __tablename__ = "response"

    id = Column(Integer, primary_key=True)
    name = Column(Text, ForeignKey("variable.name"))
    label = Column(Text)
    value = Column(Integer)

    def __init__(self, name, label, value):
        self.name = name
        self.label = label
        self.value = value

    def __repr__(self):
        return "<Response %r>" % self.label


class Group(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True)
    group_id = Column(Text)
    count = Column(Integer)

    def __init__(self, group_id, count):
        self.group_id = group_id
        self.count = count

    def __repr__(self):
        return "<Group %r>" % self.group_id