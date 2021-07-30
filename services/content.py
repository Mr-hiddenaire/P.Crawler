from models.contents_model import Contents

class ContentService:
    def __init__(self):
        pass

    @staticmethod
    def add_contents(name, unique_id, tags, types, thumb_url, torrent_url, pick_up_status, pick_up_time, is_archive, archive_priority, url_hash, is_scraped):
        Contents.add_contents(Contents(name, unique_id, tags, types, thumb_url, torrent_url, pick_up_status, pick_up_time, is_archive, archive_priority, url_hash, is_scraped))