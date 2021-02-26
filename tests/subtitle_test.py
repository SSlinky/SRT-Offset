import subtitle
import unittest

from datetime import datetime, timedelta


class Test_SubtitleItem(unittest.TestCase):
    # region Setup and Tear Down

    @classmethod
    def setUpClass(cls):
        id = '1'
        ts = '00:00:57,040 --> 00:02:00,044'
        tx = "We're going to Braavos!"
        cls.sub_item = subtitle.Item(id, ts, tx)
        cls.expected_start = datetime(1, 1, 1, 0, 0, 57, 40000)
        cls.expected_end = datetime(1, 1, 1, 0, 2, 0, 44000)
        cls.expected_ts = ts
        cls.expected_text = tx

    @classmethod
    def tearDownClass(cls):
        pass

    # endregion

    # region Private Member Tests

    def test_get_times(self):
        # Arrange
        err = 'Failed to convert {} time'
        item = Test_SubtitleItem.sub_item
        expected_start = Test_SubtitleItem.expected_start
        expected_end = Test_SubtitleItem.expected_end

        # Assert
        self.assertEqual(item.start, expected_start, err.format('start'))
        self.assertEqual(item.end, expected_end, err.format('end'))

    # endregion

    # region Positive Tests

    def test_parse_time(self):
        # Arrange
        item = Test_SubtitleItem.sub_item
        time_text = '00:00:57,040'
        expected = datetime(1, 1, 1, 0, 0, 57, 40000)

        # Act
        test_result = item.parse_time(time_text)

        # Assert
        self.assertEqual(test_result, expected)

    def test_offset_time_seconds(self):
        # Arrange
        item = Test_SubtitleItem.sub_item
        start = datetime(1, 1, 1, 0, 0, second=10)
        expected = datetime(1, 1, 1, 0, 0, second=11)

        # Act
        test_result = item.offset_time_seconds(start, 1)

        # Assert
        self.assertEqual(test_result, expected)

    def test_format_time(self):
        # Arrange
        item = Test_SubtitleItem.sub_item
        time_value = datetime(1, 1, 1, 13, 45, 16, 401000)
        expected = '13:45:16,401'

        # Act
        test_result = item.format_time(time_value)

        # Assert
        self.assertEqual(test_result, expected)

    def test_offset(self):
        # Arrange
        item = Test_SubtitleItem.sub_item
        offset = 1
        offset_td = timedelta(seconds=offset)
        expected_start = self.expected_start + offset_td
        expected_end = self.expected_end + offset_td

        # Act
        item.offset(offset)

        # Assert
        self.assertEqual(item.start, expected_start)
        self.assertEqual(item.end, expected_end)

    def test_srt_timestamp(self):
        # Arrange
        item = Test_SubtitleItem.sub_item
        expected_result = self.expected_ts

        # Act
        result = item.srt_timestamp()

        # Assert
        self.assertEqual(result, expected_result)

    # endregion

    # region Negative Tests

    def test_init_validation_raises_error(self):
        # Act
        with self.assertRaises(TypeError):
            subtitle.Item(5, '5', '5')
        with self.assertRaises(TypeError):
            subtitle.Item('5', 5, '5')
        with self.assertRaises(TypeError):
            subtitle.Item('5', '5', 5)


if __name__ == '__main__':
    unittest.main()
