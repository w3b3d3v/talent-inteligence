"""Talent Intelligence Exceptions"""

class InsufficientCommandArguments(Exception):
    """Raised when there are insufficient arguments for a command"""
    pass

class CloudFunctionUrlNotFound(Exception):
    """Raised when the cloud function url is not found on envs"""
    pass