============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Proyecto32\backend-premium-api(2)
plugins: anyio-4.16.0, cov-7.1.0
collected 11 items

app\tests\test_users.py ...........                                      [100%]

============================== warnings summary ===============================
.venv\Lib\site-packages\fastapi\testclient.py:1
  C:\Proyecto32\backend-premium-api(2)\.venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=============================== tests coverage ================================
_______________ coverage: platform win32, python 3.11.9-final-0 _______________

Name                               Stmts   Miss  Cover   Missing
----------------------------------------------------------------
app\__init__.py                        0      0   100%
app\api\__init__.py                    0      0   100%
app\api\deps.py                       21      0   100%
app\api\v1\__init__.py                 0      0   100%
app\api\v1\api.py                      6      0   100%
app\api\v1\endpoints\__init__.py       0      0   100%
app\api\v1\endpoints\auth.py          20      0   100%
app\api\v1\endpoints\items.py         20      7    65%   34-40, 55-62
app\api\v1\endpoints\users.py         29      3    90%   57, 77-78
app\core\__init__.py                   0      0   100%
app\core\config.py                    19      0   100%
app\core\database.py                  11      4    64%   33-37
app\core\security.py                  22      2    91%   60, 93
app\main.py                            8      0   100%
app\models\__init__.py                 0      0   100%
app\models\base.py                     1      1     0%   8
app\models\item.py                    10      0   100%
app\models\user.py                    12      0   100%
app\schemas\__init__.py                0      0   100%
app\schemas\item.py                   13      0   100%
app\schemas\token.py                   7      0   100%
app\schemas\user.py                   17      0   100%
app\tests\__init__.py                  0      0   100%
app\tests\conftest.py                 30      0   100%
app\tests\test_users.py               61      0   100%
----------------------------------------------------------------
TOTAL                                307     17    94%
======================== 11 passed, 1 warning in 6.00s ========================
