import subprocess
import uuid
import os
from .language_settings import LANGUAGE_SETTINGS


def run_code(code, language, input_data):
    file_id = str(uuid.uuid4())
    settings = LANGUAGE_SETTINGS.get(language.lower())
    
    if settings is None:
        return '', f"Unsupported language: {language}"

    ext = settings['extension']
    filename = f'{file_id}{ext}'
    file_path = os.path.join('/tmp', filename)

    with open(file_path, 'w') as f:
        f.write(code)

    exe_output = ''
    exe_error = ''

    try:
        if settings.get("compile"):
            exe_name = os.path.join('/tmp', f'{file_id}_exe')
            compile_result = subprocess.run(
                settings['compile_cmd'](file_path, exe_name),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            if compile_result.returncode != 0:
                return '', compile_result.stderr.strip()

            run_cmd = settings['run_cmd'](exe_name if language.lower() == "cpp" else filename)
        else:
            run_cmd = settings['run_cmd'](file_path)

        run_result = subprocess.run(
            run_cmd,
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )

        exe_output = run_result.stdout.strip()
        exe_error = run_result.stderr.strip()

    except subprocess.TimeoutExpired:
        exe_error = 'Execution timed out.'
    except Exception as e:
        exe_error = f'Error: {str(e)}'
    finally:
        # Clean up
        try: os.remove(file_path)
        except: pass
        if language.lower() == "cpp":
            try: os.remove(exe_name)
            except: pass
        elif language.lower() == "java":
            try: os.remove(file_path.replace('.java', '.class'))
            except: pass

    return exe_output, exe_error
