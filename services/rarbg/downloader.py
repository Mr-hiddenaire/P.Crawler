from config import base as base_config
import os
import time
from services.rarbg import base as rarbg_base_service

class Downloader:
    def __init__(self, torrent_url=None):
        self.torrent_url = torrent_url
        self.torrent_valid_extensions = ['.torrent']

    def download(self):
        download_torrent_tmp_path = base_config.STATISTICS_PATH + '/' + 'torrent/tmp'
        download_torrent_path = base_config.STATISTICS_PATH + '/' + 'torrent'

        if os.path.exists(download_torrent_tmp_path) is not True:
            os.makedirs(download_torrent_tmp_path)

        if os.path.isdir(download_torrent_tmp_path) is False:
            raise FileNotFoundError('Download torrent tmp directory does not exists')

        if os.path.isdir(download_torrent_path) is False:
            raise FileNotFoundError('Download torrent directory does not exists')

        """ driver initialization """
        driver = rarbg_base_service.break_defence(url=self.torrent_url, is_success_landing_page='download')
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_torrent_tmp_path}}
        driver.execute("send_command", params)
        driver.get(self.torrent_url)

        """ wait to download finished """
        time.sleep(8)
        driver.close()

        torrent_filename_list = os.listdir(download_torrent_tmp_path)

        if len(torrent_filename_list) <= 0:
            return None
        else:
            original_torrent_filename = torrent_filename_list[0]
            filename, extension = os.path.splitext(original_torrent_filename)

            if extension in self.torrent_valid_extensions:
                os.rename(download_torrent_tmp_path + '/' + original_torrent_filename, download_torrent_path + '/' + original_torrent_filename)
                return original_torrent_filename
            else:
                return None