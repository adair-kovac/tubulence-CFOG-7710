import yaml
from utils.path_util import get_project_root
from pathlib import Path


class Config:

    def __init__(self):
        with open(get_project_root() / "calculations" / "calculations_config.yaml") as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)
        self.config = config
        dirs = [self.get_figure_output_dir(), self.get_data_output_dir()]
        for directory in dirs:
            directory.mkdir(parents=True, exist_ok=True)

    def is_enabled(self, calculation):
        return self.config["calculations"][calculation]["enabled"]

    def get_figure_output_dir(self):
        return self.get_output_root_dir() / self.config["output_dirs"]["figures"]

    def get_data_output_dir(self):
        return self.get_output_root_dir() / self.config["output_dirs"]["data"]

    def get_output_root_dir(self):
        return get_project_root() / self.config["output_dirs"]["root"]

    def get_sonic_data_dir(self):
        return Path(self.config["sonic_data_dir"])
