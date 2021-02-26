# import subo
# import unittest
# from datetime import datetime


# class TestSubo(unittest.TestCase):
#     def test_offset_time_seconds_addfive(self):
#         # Arrange
#         start_time = datetime(2021, 2, 18, 10, 50)
#         offset_seconds = 5
#         expected_result = datetime(2021, 2, 18, 10, 50, offset_seconds)

#         # Act
#         test_result = subo.offset_time_seconds(start_time, offset_seconds)

#         # Assert
#         self.assertEqual(test_result, expected_result)

#     def test_offset_time_seconds_outofbounds(self):
#         # Arrange
#         start_time = datetime(1, 1, 1, 0, 1)
#         offset_seconds = -61

#         # Act
#         with self.assertRaises(Exception):
#             subo.offset_time_seconds(start_time, offset_seconds)


# if __name__ == '__main__':
#     unittest.main()
