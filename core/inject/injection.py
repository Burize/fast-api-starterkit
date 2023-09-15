from injector import Injector

from core import settings
from core.inject.configuration import TestConfiguration
from core.inject.configuration import Configuration


configuration = TestConfiguration() if settings.IS_TEST else Configuration()

injector = Injector([configuration])
