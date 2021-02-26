from typing import Tuple
import logging
# import setup_logger
from datetime import datetime, timedelta


logger = logging.getLogger('subo.subtitle')


class Item():
    """
    A class representation of the lines of text
    that make up a single subtitle item
    """

    # region Constructor

    def __init__(self, id: str, ts: str, text: str):
        """
        Default constructor

        kwargs:
            str id:   The sequence number.
            str ts:   The line containing the
                      start and end timestamps.
            str text: The subtitle text.
        """

        # Method to generate an error string for the logger
        def __log_type_error(value: any, t: type):
            """Logs a critical message for the type error"""
            err = f'{value} expected {type(t())} type but got {type(value)}.'
            logger.critical(err)

        # Validate the constructor arguments are strings
        should_error = False
        for arg in (id, ts, text):
            if not isinstance(arg, str):
                __log_type_error(arg)
                should_error = True
        if should_error:
            logger.critical('Failed to create instance of Item')
            raise TypeError('Constructor arguments invalid type.')

        # Set up Item
        self.id = id
        self.start, self.end = self.__get_times(ts)
        self.text = text

    # endregion

    # region Builtins

    def __str__(self):
        return f'{self.id}{self.srt_timestamp()}{self.text}'

    # endregion

    # region Private Helpers

    def __get_times(self, time_string: str) -> Tuple[datetime, datetime]:
        """
        Extracts the start and end times from the passed
        in string and converts to datetimes

        Arguments:
            str time_string: An srt timestamp line with a
                             start and end time separated by '-->'

        Returns:
            tuple(datetime, datetime): A tuple with two datetime object
            from the parsed timestamp line.
        """
        start, end = time_string.split(' --> ')
        return self.parse_time(start), self.parse_time(end)

    # endregion

    # region Public Methods

    def parse_time(self, t: str) -> datetime:
        """Parses a datetime from srt format

        Returns:
            datetime: The obj parsed from the string
        """
        return datetime.strptime('00010101' + t.rstrip(), r'%Y%m%d%H:%M:%S,%f')

    def offset_time_seconds(self, t: datetime, s: float) -> datetime:
        """Returns a time that is t offset by s seconds

        Arguments:
            datetime t: The time to be offset
            float s:    The number of seconds to offset

        Returns:
            datetime.datetime
        """
        try:
            return t + timedelta(seconds=s)
        except Exception as e:
            # Log a warning that the timestamp cannot be clipped
            msg = 'Timestamp cannot be offset for {}) {} by {} seconds.\n{}'
            logger.warn(msg.format(self.id, self.format_time(t), s, e))

    def format_time(self, t: datetime) -> str:
        """Returns a datetime in srt format"""
        return datetime.strftime(t, r'%H:%M:%S,%f')[:-3]

    def offset(self, s: float) -> None:
        """
        Update both the object's start and end time by the same value

        Arguments:
            float s: the number of seconds to offset the time
        """
        self.start = self.offset_time_seconds(self.start, s)
        self.end = self.offset_time_seconds(self.end, s)

    def srt_timestamp(self) -> str:
        """
        Generates a new timestamp from the start and end times.

        Returns:
            str: The srt formatted timestamp.
        """
        start, end = (
            self.format_time(self.start),
            self.format_time(self.end)
        )

        return f'{start} --> {end}\n'

    def lines_generator(self) -> str:
        """Yields the lines of the subtitle in srt format"""
        yield self.id
        yield self.srt_timestamp()
        yield self.text

    # endregion
