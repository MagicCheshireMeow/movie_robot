import os
from enum import Enum


class DiscType(Enum):
    """原盘类型"""
    BluRay = 'Blu-ray'
    DVD = 'DVD'
    BluRayDisc = 'Blu-ray Disc'


"""文件后缀"""
EXT_TYPE = {
    'info': ['.nfo', '.txt', '.cue'],
    'subtitle': ['.ass', '.srt', '.smi', '.ssa', '.sub', '.vtt', '.idx'],
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.tif'],
    'video': ['.mp4', '.mkv', '.avi', '.wmv', '.mpg', '.mpeg', '.mov', '.rm', '.rmvb', '.ram', '.flv', '.ts',
              '.iso', '.m2ts', '.bdmv'],
    'audio': ['.mka', '.mp3', '.m3u', '.flac']
}


class FileProbe:
    """文件信息探测"""

    @staticmethod
    def get_disc_type(path):
        """
        获取一个路径的光盘类型
        :param path:
        :return:
        """
        ext = os.path.splitext(path)[-1]
        if ext.lower() == '.iso':
            return DiscType.DVD
        bdmv = os.path.join(path, 'BDMV')
        type = None
        if os.path.exists(bdmv):
            type = DiscType.BluRay
        dvd = os.path.join(path, 'VIDEO_TS')
        if os.path.exists(dvd):
            type = DiscType.DVD
        bd = os.path.join(path, 'BDROM')
        if os.path.exists(bd):
            type = DiscType.BluRayDisc
        if os.path.exists(os.path.join(path, 'DISK1')) or os.path.exists(os.path.join(path, 'DISKA')):
            type = DiscType.BluRay
        return type

    @staticmethod
    def get_file_type(filepath):
        """
        获取一个文件的格式类型，基于后缀判断
        :param filepath:
        :return: info、subtitle、image、video、audio
        """
        if not EXT_TYPE:
            return 'unknown'
        ext = os.path.splitext(filepath)[-1].lower()
        for key in EXT_TYPE.keys():
            if ext in EXT_TYPE[key]:
                return key
        return 'unknown'

    @staticmethod
    def find_max_size_video_file(path):
        """
        找到目录内最大的视频文件
        :param path:
        :return:
        """
        if os.path.isfile(path):
            return path
        max_size = 0
        max_filepath = None
        for path, dir_list, file_list in os.walk(path):
            for file_name in file_list:
                filepath = os.path.join(path, file_name)
                if FileProbe.get_file_type(filepath) != 'video':
                    continue
                file_size = os.path.getsize(filepath)
                if file_size > max_size:
                    max_filepath = filepath
                    max_size = file_size
        return max_filepath
