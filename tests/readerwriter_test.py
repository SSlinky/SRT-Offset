import readerwriter
import unittest
from unittest.mock import patch, mock_open


class WriteExample():
    def w(self, fn, s):
        with open(fn, 'w') as f:
            f.write(s)


class Test_ReaderWriter(unittest.TestCase):

    def test_write(self):
        # Arrange
        m = mock_open()
        filename = 'unittest_write.txt'
        test_data = '\n'.join([f'Line_{n}.' for n in range(1, 6)])

        # Act
        with patch('builtins.open', m):
            readerwriter.Io.write(filename, test_data)

        # Assert
        m.assert_called_with(filename, 'w')
        m.return_value.writelines.assert_called_once_with(test_data)

    def test_read(self):
        # Arrange
        filename = 'unittest_read.txt'
        test_data = [f'Line_{n}.\n' for n in range(1, 6)]
        m = mock_open(read_data=''.join(test_data))

        # Act
        with patch('builtins.open', m):
            result = readerwriter.Io.read(filename)

        # Assert
        m.assert_called_with(filename, 'r')
        m.return_value.readlines.assert_called_once()
        self.assertEqual(test_data, result)


if __name__ == '__main__':
    unittest.main()
