from sqlalchemy import Column, Integer, String, DateTime, DefaultClause

from .database import Base


class Comic(Base):
    __tablename__ = 'comic'

    id = Column(Integer, primary_key=True)
    month = Column(String)
    num = Column(Integer, nullable=False)
    link = Column(String)
    year = Column(String)
    news = Column(String)
    safe_title = Column(String, nullable=False)
    transcript = Column(String)
    alt = Column(String)
    img = Column(String)
    title = Column(String)
    day = Column(String)
    served_last = Column(DateTime)
    served_count = Column(Integer, server_default=DefaultClause('0'))

    def __repr__(self):
        return ("<Comic(month='{:s}, num='{:d}', link='{:s}', year='{:s}', "
                "news='{:s}', safe_title='{:s}', transcript='{:s}', "
                "alt='{:s}', img='{:s}', title='{:s}', day='{:s}',"
                "served_last='{:s}', served_count='{:d}')>"
                .format(self.month, self.num, self.link, self.year,
                        self.news, self.safe_title, self.transcript,
                        self.alt, self.img, self.title, self.day,
                        self.served_last, self.served_count))


""" Example json response:
{
   "month":"1",
   "num":1,
   "link":"",
   "year":"2006",
   "news":"",
   "safe_title":"Barrel - Part 1",
   "transcript":"[[A boy sits in a barrel which is floating in an ocean.]]\nBoy: I wonder where I'll float next?\n[[The barrel drifts into the distance. Nothing else can be seen.]]\n{{Alt: Don't we all.}}",
   "alt":"Don't we all.",
   "img":"http:\/\/imgs.xkcd.com\/comics\/barrel_cropped_(1).jpg",
   "title":"Barrel - Part 1",
   "day":"1"
}
"""
