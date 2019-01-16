# -*- coding: utf-8 -*-

__all__ = [
    'InvalidTimeInterval',
    'InvalidDateList',
    'InvalidPath'
]

class BaseError(Exception):
    """Base class for all exceptions"""
    pass

class InvalidTimeInterval(BaseError):
    """"Base class for exceptions related to the invalid time interval"""
    pass

class InvalidDateList(BaseError):
    """"Base class for exceptions related to the invalid date list"""
    pass

class InvalidPath(BaseError):
    """"Base class for exceptions related to the invalid date list"""
    pass

class NoEventDefined(BaseError):
    """"Base class for exceptions related to the no event defined"""
    pass