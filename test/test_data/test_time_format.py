import unittest
from utils.path_util import get_project_root
from data import time_format
import pandas as pd
import datetime


class TestTimeFormatter(unittest.TestCase):
    test_dir = get_project_root() / "test" / "test_data"

    def test_get_time_parsing_args_for_visibility_data(self):
        kwargs = time_format.get_time_parsing_args_for_visibility_data()
        test_file = self.test_dir / "mock_vis_time_data.csv"
        df = pd.read_csv(test_file, sep="\t", **kwargs)
        expected = datetime.datetime(2018, 9, 13, second=9)
        self.assertEquals(expected, df.iloc[0]["time"])


if __name__ == '__main__':
    unittest.main()
