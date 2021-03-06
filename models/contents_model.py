from sqlalchemy import Column, String, Integer, SMALLINT

from models.db import Base
from models.db import session_factory

class Contents(Base):
    __tablename__ = 'contents'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, default='')
    unique_id = Column(String, nullable=False, default='')
    tags = Column(String, nullable=False, default='')
    type = Column(SMALLINT, nullable=False, default=0)
    thumb_url = Column(String, nullable=False, default='')
    torrent_url = Column(String, nullable=False, default='')
    torrent_path = Column(String, nullable=False, default='')
    entry_point = Column(String, nullable=False, default='')
    detail_url = Column(String, nullable=False, default='')
    pick_up_status = Column(SMALLINT, nullable=False, default=0)
    pick_up_time = Column(Integer, nullable=False, default=0)
    is_archive = Column(Integer, nullable=False, default=0)
    archive_priority = Column(Integer, nullable=False, default=0)
    list_url_hash = Column(String, nullable=False, default='')
    detail_url_hash = Column(String, nullable=False, default='')
    is_scraped = Column(Integer, nullable=False, default=0)

    def __init__(self):
        pass

    def add_contents(self, name, unique_id, tags, types, thumb_url, torrent_url, torrent_path, entry_point, detail_url, pick_up_status, pick_up_time, is_archive, archive_priority, list_url_hash, detail_url_hash, is_scraped):
        session = session_factory()

        self.name = name
        self.unique_id = unique_id
        self.tags = tags
        self.type = types
        self.thumb_url = thumb_url
        self.torrent_url = torrent_url
        self.torrent_path = torrent_path
        self.entry_point = ''
        #self.entry_point = entry_point
        self.detail_url = detail_url
        self.pick_up_status = pick_up_status
        self.pick_up_time = pick_up_time
        self.is_archive = is_archive
        self.archive_priority = archive_priority
        #self.list_url_hash = 'list_url_hash'
        self.list_url_hash = ''
        self.detail_url_hash = detail_url_hash
        self.is_scraped = is_scraped

        session.add(self)
        session.commit()
        session.close()

    @staticmethod
    def is_page_scraped(url_hash=None, types=None):
        session = session_factory()
        res = session.query(Contents).filter(Contents.list_url_hash == url_hash, Contents.type == types).count()
        session.close()
        return res

    @staticmethod
    def get_content_by_detail_url_hash(url_hash=None, types=None):
        session = session_factory()
        res = session.query(Contents).filter(Contents.detail_url_hash == url_hash, Contents.type == types).first()
        session.close()
        return res

    @staticmethod
    def update_content_by_pk(pk=None, data=None):
        session = session_factory()
        res = session.query(Contents).filter(Contents.id == pk).update(data)
        session.commit()
        session.close()
        return res

    @staticmethod
    def get_total_not_scraped_by_type(types=None, is_scraped=None):
        session = session_factory()
        res = session.query(Contents).filter(Contents.type == types, Contents.is_scraped == is_scraped).count()
        session.close()
        return res

    @staticmethod
    def get_total_torrent_not_download(types=None, is_scraped=None):
        session = session_factory()
        res = session.query(Contents).filter(Contents.type == types, Contents.is_scraped == is_scraped, Contents.torrent_url != '').count()
        session.close()
        return res

    @staticmethod
    def get_contents_not_scraped_by_type(offset=None, page_size=None, types=None, is_scraped=None):
        session = session_factory()
        res = session.query(Contents).filter(Contents.type==types, Contents.is_scraped==is_scraped).offset(offset).limit(page_size).all()
        session.close()
        return res

    @staticmethod
    def get_content_not_scraped_torrent_url_is_empty(offset=None, page_size=None, types=None, is_scraped=None):
        session = session_factory()
        res = session.query(Contents).filter(Contents.type==types, Contents.is_scraped==is_scraped, Contents.torrent_url=='').offset(offset).limit(page_size).all()
        session.close()
        return res

    @staticmethod
    def get_content_torrent_not_download(offset=None, page_size=None, types=None, is_scraped=None):
        session = session_factory()
        res = session.query(Contents).filter(Contents.type == types, Contents.is_scraped == is_scraped, Contents.torrent_url != '').offset(offset).limit(page_size).all()
        session.close()
        return res
