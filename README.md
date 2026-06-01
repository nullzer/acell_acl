# Acell ACL

Небольшое локальное Python-приложение для Windows 10 и ALT Linux.

## Назначение

Приложение запускается локально на рабочем месте пользователя и показывает базовую структуру будущего продукта:

- локальный режим работы;
- режим работы через сетевой ресурс;
- поддерживаемые платформы Windows 10 и ALT Linux;
- основные этапы разработки.

## Запуск из исходников

```bash
python3 -m acell_acl
```

Проверка без открытия графического интерфейса:

```bash
python3 -m acell_acl --check
```

## Сборка под ALT Linux

Сборку необходимо выполнять на ALT Linux:

```bash
./scripts/build_alt_linux.sh
```

Скрипт создаст локальное окружение `.venv-build`, установит PyInstaller и сформирует результат `dist/acell-acl`.

## Сборка под Windows 10

Сборку необходимо выполнять на Windows 10:

```powershell
.\scripts\build_windows.ps1
```

Скрипт создаст локальное окружение `.venv-build`, установит PyInstaller и сформирует результат `dist\acell-acl.exe`.

## Тестирование

```bash
python3 -m unittest discover -s tests
python3 -m compileall acell_acl tests
python3 -m acell_acl --check
```
