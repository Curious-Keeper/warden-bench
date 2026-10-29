❯ python3 serve.py               
INFO:     Started server process [48809]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8765 (Press CTRL+C to quit)
INFO:     127.0.0.1:53000 - "GET / HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:53000 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:44216 - "GET /healthz HTTP/1.1" 200 OK
INFO:     127.0.0.1:44216 - "GET /state HTTP/1.1" 200 OK
INFO:     127.0.0.1:44216 - "POST /goto HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "browser-agent/.venv/lib/python3.14/site-packages/uvicorn/protocols/http/httptools_impl.py", line 421, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.scope, self.receive, self.send
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/uvicorn/middleware/proxy_headers.py", line 56, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/applications.py", line 1159, in __call__
    await super().__call__(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/errors.py", line 186, in __call__
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 680, in app
    await route.handle(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 276, in handle
    await self.app(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 134, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 120, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 674, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 328, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/browser/server.py", line 172, in _goto
    await actions.goto(_page(), body.url)
  File "browser-agent/browser/actions.py", line 24, in goto
    await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/async_api/_generated.py", line 9045, in goto
    await self._impl_obj.goto(
        url=url, timeout=timeout, waitUntil=wait_until, referer=referer
    )
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_page.py", line 552, in goto
    return await self._main_frame.goto(**locals_to_params(locals()))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_frame.py", line 153, in goto
    await self._channel.send(
        "goto", self._navigation_timeout, locals_to_params(locals())
    )
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_connection.py", line 69, in send
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_connection.py", line 559, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
playwright._impl._errors.Error: Page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:3000/
Call log:
  - navigating to "http://localhost:3000/", waiting until "domcontentloaded"

INFO:     127.0.0.1:46974 - "POST /goto HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "browser-agent/.venv/lib/python3.14/site-packages/uvicorn/protocols/http/httptools_impl.py", line 421, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.scope, self.receive, self.send
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/uvicorn/middleware/proxy_headers.py", line 56, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/applications.py", line 1159, in __call__
    await super().__call__(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/errors.py", line 186, in __call__
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 680, in app
    await route.handle(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 276, in handle
    await self.app(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 134, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 120, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 674, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 328, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/browser/server.py", line 172, in _goto
    await actions.goto(_page(), body.url)
  File "browser-agent/browser/actions.py", line 24, in goto
    await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/async_api/_generated.py", line 9045, in goto
    await self._impl_obj.goto(
        url=url, timeout=timeout, waitUntil=wait_until, referer=referer
    )
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_page.py", line 552, in goto
    return await self._main_frame.goto(**locals_to_params(locals()))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_frame.py", line 153, in goto
    await self._channel.send(
        "goto", self._navigation_timeout, locals_to_params(locals())
    )
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_connection.py", line 69, in send
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_connection.py", line 559, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
playwright._impl._errors.Error: Page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:8080/
Call log:
  - navigating to "http://localhost:8080/", waiting until "domcontentloaded"

INFO:     127.0.0.1:46990 - "POST /goto HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "browser-agent/.venv/lib/python3.14/site-packages/uvicorn/protocols/http/httptools_impl.py", line 421, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.scope, self.receive, self.send
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/uvicorn/middleware/proxy_headers.py", line 56, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/applications.py", line 1159, in __call__
    await super().__call__(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/errors.py", line 186, in __call__
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 680, in app
    await route.handle(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 276, in handle
    await self.app(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 134, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 120, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 674, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 328, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/browser/server.py", line 172, in _goto
    await actions.goto(_page(), body.url)
  File "browser-agent/browser/actions.py", line 24, in goto
    await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/async_api/_generated.py", line 9045, in goto
    await self._impl_obj.goto(
        url=url, timeout=timeout, waitUntil=wait_until, referer=referer
    )
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_page.py", line 552, in goto
    return await self._main_frame.goto(**locals_to_params(locals()))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_frame.py", line 153, in goto
    await self._channel.send(
        "goto", self._navigation_timeout, locals_to_params(locals())
    )
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_connection.py", line 69, in send
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_connection.py", line 559, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
playwright._impl._errors.Error: Page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:1337/
Call log:
  - navigating to "http://localhost:1337/", waiting until "domcontentloaded"

INFO:     127.0.0.1:47002 - "GET /screenshot?full_page=false HTTP/1.1" 200 OK
INFO:     127.0.0.1:47002 - "POST /goto HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "browser-agent/.venv/lib/python3.14/site-packages/uvicorn/protocols/http/httptools_impl.py", line 421, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.scope, self.receive, self.send
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/uvicorn/middleware/proxy_headers.py", line 56, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/applications.py", line 1159, in __call__
    await super().__call__(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/errors.py", line 186, in __call__
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 680, in app
    await route.handle(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 276, in handle
    await self.app(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 134, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 120, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 674, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 328, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/browser/server.py", line 172, in _goto
    await actions.goto(_page(), body.url)
  File "browser-agent/browser/actions.py", line 24, in goto
    await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/async_api/_generated.py", line 9045, in goto
    await self._impl_obj.goto(
        url=url, timeout=timeout, waitUntil=wait_until, referer=referer
    )
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_page.py", line 552, in goto
    return await self._main_frame.goto(**locals_to_params(locals()))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_frame.py", line 153, in goto
    await self._channel.send(
        "goto", self._navigation_timeout, locals_to_params(locals())
    )
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_connection.py", line 69, in send
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_connection.py", line 559, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
playwright._impl._errors.Error: Page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:5000/
Call log:
  - navigating to "http://localhost:5000/", waiting until "domcontentloaded"

INFO:     127.0.0.1:58422 - "POST /goto HTTP/1.1" 200 OK
INFO:     127.0.0.1:58422 - "GET /state HTTP/1.1" 200 OK
INFO:     127.0.0.1:58422 - "POST /goto HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "browser-agent/.venv/lib/python3.14/site-packages/uvicorn/protocols/http/httptools_impl.py", line 421, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.scope, self.receive, self.send
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/uvicorn/middleware/proxy_headers.py", line 56, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/applications.py", line 1159, in __call__
    await super().__call__(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/errors.py", line 186, in __call__
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 680, in app
    await route.handle(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 276, in handle
    await self.app(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 134, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 120, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 674, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 328, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/browser/server.py", line 172, in _goto
    await actions.goto(_page(), body.url)
  File "browser-agent/browser/actions.py", line 24, in goto
    await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/async_api/_generated.py", line 9045, in goto
    await self._impl_obj.goto(
        url=url, timeout=timeout, waitUntil=wait_until, referer=referer
    )
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_page.py", line 552, in goto
    return await self._main_frame.goto(**locals_to_params(locals()))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_frame.py", line 153, in goto
    await self._channel.send(
        "goto", self._navigation_timeout, locals_to_params(locals())
    )
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_connection.py", line 69, in send
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_connection.py", line 559, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
playwright._impl._errors.Error: Page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:9000/
Call log:
  - navigating to "http://localhost:9000/", waiting until "domcontentloaded"

INFO:     127.0.0.1:34328 - "POST /goto HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "browser-agent/.venv/lib/python3.14/site-packages/uvicorn/protocols/http/httptools_impl.py", line 421, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.scope, self.receive, self.send
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/uvicorn/middleware/proxy_headers.py", line 56, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/applications.py", line 1159, in __call__
    await super().__call__(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/errors.py", line 186, in __call__
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 680, in app
    await route.handle(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 276, in handle
    await self.app(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 134, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 120, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 674, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 328, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/browser/server.py", line 172, in _goto
    await actions.goto(_page(), body.url)
  File "browser-agent/browser/actions.py", line 24, in goto
    await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/async_api/_generated.py", line 9045, in goto
    await self._impl_obj.goto(
        url=url, timeout=timeout, waitUntil=wait_until, referer=referer
    )
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_page.py", line 552, in goto
    return await self._main_frame.goto(**locals_to_params(locals()))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_frame.py", line 153, in goto
    await self._channel.send(
        "goto", self._navigation_timeout, locals_to_params(locals())
    )
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_connection.py", line 69, in send
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_connection.py", line 559, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
playwright._impl._errors.Error: Page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:4000/
Call log:
  - navigating to "http://localhost:4000/", waiting until "domcontentloaded"

INFO:     127.0.0.1:34334 - "POST /goto HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "browser-agent/.venv/lib/python3.14/site-packages/uvicorn/protocols/http/httptools_impl.py", line 421, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.scope, self.receive, self.send
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/uvicorn/middleware/proxy_headers.py", line 56, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/applications.py", line 1159, in __call__
    await super().__call__(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/errors.py", line 186, in __call__
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 680, in app
    await route.handle(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 276, in handle
    await self.app(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 134, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 120, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 674, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 328, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/browser/server.py", line 172, in _goto
    await actions.goto(_page(), body.url)
  File "browser-agent/browser/actions.py", line 24, in goto
    await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/async_api/_generated.py", line 9045, in goto
    await self._impl_obj.goto(
        url=url, timeout=timeout, waitUntil=wait_until, referer=referer
    )
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_page.py", line 552, in goto
    return await self._main_frame.goto(**locals_to_params(locals()))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_frame.py", line 153, in goto
    await self._channel.send(
        "goto", self._navigation_timeout, locals_to_params(locals())
    )
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_connection.py", line 69, in send
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_connection.py", line 559, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
playwright._impl._errors.Error: Page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:7777/
Call log:
  - navigating to "http://localhost:7777/", waiting until "domcontentloaded"

INFO:     127.0.0.1:34338 - "POST /goto HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "browser-agent/.venv/lib/python3.14/site-packages/uvicorn/protocols/http/httptools_impl.py", line 421, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.scope, self.receive, self.send
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/uvicorn/middleware/proxy_headers.py", line 56, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/applications.py", line 1159, in __call__
    await super().__call__(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/errors.py", line 186, in __call__
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 680, in app
    await route.handle(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/routing.py", line 276, in handle
    await self.app(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 134, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 120, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 674, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/fastapi/routing.py", line 328, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/browser/server.py", line 172, in _goto
    await actions.goto(_page(), body.url)
  File "browser-agent/browser/actions.py", line 24, in goto
    await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/async_api/_generated.py", line 9045, in goto
    await self._impl_obj.goto(
        url=url, timeout=timeout, waitUntil=wait_until, referer=referer
    )
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_page.py", line 552, in goto
    return await self._main_frame.goto(**locals_to_params(locals()))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_frame.py", line 153, in goto
    await self._channel.send(
        "goto", self._navigation_timeout, locals_to_params(locals())
    )
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_connection.py", line 69, in send
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/playwright/_impl/_connection.py", line 559, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
playwright._impl._errors.Error: Page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:8000/
Call log:
  - navigating to "http://localhost:8000/", waiting until "domcontentloaded"

^CINFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [48809]


---


󰣇 @ x1carbon …/warden-bench/browser-agent  main ! mod 6 ? untrk 114 ✓  🐍  .venv  16:36
❯ python -m agent.loop --target warden --goal "Solve level 1 — extract the password and submit it"
^CTraceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "browser-agent/agent/loop.py", line 283, in <module>
    sys.exit(main())
             ~~~~^^
  File "browser-agent/agent/loop.py", line 265, in main
    result = run(
        goal=args.goal,
    ...<5 lines>...
        max_tokens=args.max_tokens,
    )
  File "browser-agent/agent/loop.py", line 109, in run
    response = api.messages.create(
        model=model,
    ...<3 lines>...
        messages=messages,
    )
  File "browser-agent/.venv/lib/python3.14/site-packages/anthropic/_utils/_utils.py", line 268, in wrapper
    return func(*args, **kwargs)
  File "browser-agent/.venv/lib/python3.14/site-packages/anthropic/resources/messages/messages.py", line 991, in create
    return self._post(
           ~~~~~~~~~~^
        "/v1/messages",
        ^^^^^^^^^^^^^^^
    ...<30 lines>...
        stream_cls=Stream[RawMessageStreamEvent],
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "browser-agent/.venv/lib/python3.14/site-packages/anthropic/_base_client.py", line 1368, in post
    return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))
                           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/anthropic/_base_client.py", line 1076, in request
    response = self._client.send(
        request,
        stream=stream or self._should_stream_response_body(request=request),
        **kwargs,
    )
  File "browser-agent/.venv/lib/python3.14/site-packages/httpx/_client.py", line 914, in send
    response = self._send_handling_auth(
        request,
    ...<2 lines>...
        history=[],
    )
  File "browser-agent/.venv/lib/python3.14/site-packages/httpx/_client.py", line 942, in _send_handling_auth
    response = self._send_handling_redirects(
        request,
        follow_redirects=follow_redirects,
        history=history,
    )
  File "browser-agent/.venv/lib/python3.14/site-packages/httpx/_client.py", line 979, in _send_handling_redirects
    response = self._send_single_request(request)
  File "browser-agent/.venv/lib/python3.14/site-packages/httpx/_client.py", line 1014, in _send_single_request
    response = transport.handle_request(request)
  File "browser-agent/.venv/lib/python3.14/site-packages/httpx/_transports/default.py", line 250, in handle_request
    resp = self._pool.handle_request(req)
  File "browser-agent/.venv/lib/python3.14/site-packages/httpcore/_sync/connection_pool.py", line 256, in handle_request
    raise exc from None
  File "browser-agent/.venv/lib/python3.14/site-packages/httpcore/_sync/connection_pool.py", line 236, in handle_request
    response = connection.handle_request(
        pool_request.request
    )
  File "browser-agent/.venv/lib/python3.14/site-packages/httpcore/_sync/connection.py", line 103, in handle_request
    return self._connection.handle_request(request)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/httpcore/_sync/http11.py", line 136, in handle_request
    raise exc
  File "browser-agent/.venv/lib/python3.14/site-packages/httpcore/_sync/http11.py", line 106, in handle_request
    ) = self._receive_response_headers(**kwargs)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "browser-agent/.venv/lib/python3.14/site-packages/httpcore/_sync/http11.py", line 177, in _receive_response_headers
    event = self._receive_event(timeout=timeout)
  File "browser-agent/.venv/lib/python3.14/site-packages/httpcore/_sync/http11.py", line 217, in _receive_event
    data = self._network_stream.read(
        self.READ_NUM_BYTES, timeout=timeout
    )
  File "browser-agent/.venv/lib/python3.14/site-packages/httpcore/_backends/sync.py", line 128, in read
    return self._sock.recv(max_bytes)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^
  File "/usr/lib/python3.14/ssl.py", line 1285, in recv
    return self.read(buflen)
           ~~~~~~~~~^^^^^^^^
  File "/usr/lib/python3.14/ssl.py", line 1140, in read
    return self._sslobj.read(len)
           ~~~~~~~~~~~~~~~~~^^^^^
KeyboardInterrupt