# -*- coding: utf-8 -*-

__all__ = [
    'InvalidDateList',
    'NoEventDefined',
    'InvalidStockCode',
    'InvalidIndustryName'
]


class BaseError(Exception):
    """Base class for all exceptions"""
    pass


class InvalidDateList(BaseError):
    """"Base class for exceptions related to the invalid date list"""
    pass


class NoEventDefined(BaseError):
    """"Base class for exceptions related to the no event defined"""
    pass


class InvalidStockCode(BaseError):
    """Base class for exceptions related to invalid stock code"""
    pass


class InvalidIndustryName(BaseError):
    """Base class for exceptions related to invalid industry name"""
    pass
