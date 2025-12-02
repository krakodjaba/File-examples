import os
import sys
import subprocess
import platform

def run_command(cmd, cwd=None):
    """Запускает команду и выводит результат."""
    print(f"Выполняю: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Ошибки:", result.stderr)
    return result.returncode == 0

def main():
    # Узнаём ОС
    os_type = platform.system().lower()
    
    # Создаём virtualenv
    print("1) Создаём virtualenv...")
    if not os.path.exists("venv"):
        if not run_command("python -m venv venv"):
            print("Ошибка при создании virtualenv.")
            sys.exit(1)
    else:
        print("virtualenv уже существует.")
    
    # Определяем путь к pip в виртуальном окружении
    if os_type == "windows":
        pip_path = "venv\\Scripts\\pip.exe"
        python_path = "venv\\Scripts\\python.exe"
    else:
        pip_path = "venv/bin/pip"
        python_path = "venv/bin/python"
    
    # Устанавливаем зависимости
    print("2) Устанавливаем зависимости из requirements.txt...")
    if not run_command(f"{pip_path} install -r requirements.txt"):
        print("Ошибка при установке зависимостей.")
        sys.exit(1)
    
    # Запускаем все .py файлы в new/
    print("3) Запускаем все .py файлы в папке new/...")
    new_dir = "new"
    if not os.path.exists(new_dir):
        print(f"Папка {new_dir} не найдена.")
        sys.exit(1)
    
    for filename in os.listdir(new_dir):
        if filename.endswith(".py"):
            filepath = os.path.join(new_dir, filename)
            print(f"\n--- Запуск {filename} ---")
            if not run_command(f"{python_path} {filepath}"):
                print(f"Ошибка при запуске {filename}.")
    
    print("\nГотово. Проверьте созданные файлы в рабочей папке.")

if __name__ == "__main__":
    main()