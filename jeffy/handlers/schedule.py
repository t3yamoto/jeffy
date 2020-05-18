import functools
from typing import Callable

from jeffy.validator import NoneValidator, Validator


class ScheduleHandlerMixin(object):
    """Schedule event handler decorators."""

    def schedule(
        self,
        validator: Validator = NoneValidator()
    ) -> Callable:
        """
        Decorator for scheduled events.

        Usage::
            >>> from jeffy.framework import get_app
            >>> app = get_app()
            >>> @app.handlers.schedule
            ... def handler(event, context):
            ...     return event['body']['foo']
        """
        def _schedule(self, func: Callable) -> Callable:    # type: ignore
            @functools.wraps(func)
            def wrapper(event, context):                    # type: ignore
                validator.varidate(event)
                self.capture_correlation_id(event)
                try:
                    return func(event, context)
                except Exception as e:
                    raise e
            return wrapper
        return _schedule
