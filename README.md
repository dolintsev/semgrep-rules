# Semgrep rules

Taint-правило Semgrep для поиска инъекции команд во Flask-приложениях и тесты к нему.

| Правило | Уязвимость | CWE |
| --- | --- | --- |
| flask-command-injection-shell | Инъекция команд | CWE-78 |

## Как работает правило

- **Источник:** данные из `flask.request`.
- **Сток:** команда в `subprocess.*(..., shell=True)`, `os.system()` и `os.popen()`.
- **Санитайзер:** `shlex.quote()`.

Правило сообщает о находке, если данные пользователя доходят до команды оболочки без очистки.

## Запуск

```bash
semgrep --validate --config .
semgrep --test .
semgrep --config flask-command-injection-shell.yaml --metrics=off путь/к/проекту
```

## Тесты

В файле `flask-command-injection-shell.py` собраны уязвимые и безопасные примеры:

- `# ruleid:` отмечает строку, где правило должно сработать.
- `# ok:` отмечает строку, где оно срабатывать не должно.

## Ограничения

- Semgrep CE отслеживает данные только внутри одной функции.
- Источником считается только `flask.request`.
- Правило не находит запуск оболочки через список аргументов, например `subprocess.run(["sh", "-c", command])`.
