import platform
import typing as t

import psutil
import torch
from loguru import logger
from PyQt5 import QtCore


class UserSpecsDetector:
    """Reads and saves hardware specifications of the used system in storage folder"""

    def __init__(self, app: QtCore.QCoreApplication) -> None:
        """Set list of accepted gpus and calls all methods"""

        logger.info('Init User Specs Detector')
        self.app = app
        self.user_specs = {}

        self._get_system()
        self._get_cpu()
        self._get_memory()
        self._get_gpu_name()
        self._get_primary_screen_dimensions()

    @staticmethod
    @logger.catch()
    def _get_size(_bytes: float, suffix: str = 'B') -> float or None:
        """Adequate unit conversion"""
        factor = 1024
        for unit in ['', 'K', 'M', 'G', 'T', 'P']:
            if _bytes < factor:
                return f'{_bytes:.2f}{unit}{suffix}'
            _bytes /= factor
        return None

    @logger.catch()
    def _get_system(self) -> None:
        """Reads operating system related specifications"""
        uname = platform.uname()
        self.user_specs.setdefault('System', uname.system)
        self.user_specs.setdefault('Node_Name', uname.node)
        self.user_specs.setdefault('Release', uname.release)
        self.user_specs.setdefault('Version', uname.version)
        self.user_specs.setdefault('Machine', uname.machine)
        self.user_specs.setdefault('CPU', uname.processor)
        logger.debug(f'System: {uname.system}')
        logger.debug(f'Node_Name: {uname.node}')
        logger.debug(f'Release: {uname.release}')
        logger.debug(f'Version: {uname.version}')
        logger.debug(f'Machine: {uname.machine}')
        logger.debug(f'CPU: {uname.processor}')

    @logger.catch()
    def _get_cpu(self) -> None:
        """Reads physical cores and total cores(with threads)"""
        self.user_specs.setdefault('CPU_Physical_Cores', psutil.cpu_count(logical=False))
        self.user_specs.setdefault('CPU_Cores_Total', psutil.cpu_count(logical=True))
        logger.debug(f'CPU_Physical_Cores: {psutil.cpu_count(logical=False)}')
        logger.debug(f'CPU_Cores_Total: {psutil.cpu_count(logical=True)}')

    @logger.catch()
    def _get_memory(self) -> None:
        """Reads memory"""
        svmem = psutil.virtual_memory()
        self.user_specs.setdefault('Memory', self._get_size(svmem.total))
        logger.debug(f'Memory: {self._get_size(svmem.total)}')

    @logger.catch()
    def _get_gpu_name(self) -> None:
        """Reads gpu model and checks model requirements"""
        try:
            gpu_model = torch.cuda.get_device_name(torch.cuda.current_device()).lower()
            self.user_specs.setdefault('GPU', gpu_model)
            logger.debug(f'GPU: {gpu_model}')
        except Exception as error:
            self.user_specs.setdefault('GPU', None)
            logger.warning(f'GPU drivers not found \n{error}')

    @logger.catch()
    def _get_primary_screen_dimensions(self) -> None:
        screen = self.app.primaryScreen()
        self.user_specs.setdefault('Primary_Screen', str(screen.name()))
        self.user_specs.setdefault(
            'Primary_Screen_Total_Size',
            (int(QtCore.QSize.width(screen.size())), int(QtCore.QSize.height(screen.size()))),
        )
        self.user_specs.setdefault(
            'Primary_Screen_Available_Size',
            (int(QtCore.QRect.width(screen.availableGeometry())), int(QtCore.QRect.height(screen.availableGeometry()))),
        )
        logger.debug(f'Primary Screen: {screen.name()}')
        logger.debug(
            f'Primary_Screen_Total_Size: '
            f'{int(QtCore.QSize.width(screen.size())), int(QtCore.QSize.height(screen.size()))}'
        )
        logger.debug(
            f'Primary_Screen_Available_Size: '
            f'{int(QtCore.QRect.width(screen.availableGeometry()))},'
            f'{int(QtCore.QRect.height(screen.availableGeometry()))}'
        )

    def get(self, key: str, optional: t.Any or None = None) -> t.Any or None:
        """Checks key in data base and returns value, if missing adds key to data base with optional value"""
        value = optional
        try:
            value = self.user_specs.get(key, optional)
        except Exception as error:
            logger.warning(f'Key {key} not found in user specifications \n{error}')
        return value
