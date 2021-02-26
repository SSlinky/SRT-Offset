import readerwriter
import unittest
from unittest.mock import patch, mock_open


class WriteExample():
    def w(self):
        pass


class Test_ReaderWriter(unittest.TestCase):

    def test_read_and_write(self):
        # Arrange
        open_mock = mock_open()
        filename = 'test.srt'
        test_data = [
            '1',
            '00:00:57,040 --> 00:02:00,044',
            "We're going to Braavos!"
            ]

        # Act
        with patch('readerwriter.open', open_mock, create=True):
            readerwriter.io.write(filename, '\n'.join(test_data))

        # Assert
        open_mock.assert_called_with(filename, 'w')
        open_mock.return_value.write.assert_called_once_with(test_data)

    def test_mock(self):
        open_mock = mock_open()
        filename = 'test.srt'


if __name__ == '__main__':
    unittest.main()
