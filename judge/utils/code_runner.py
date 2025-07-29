import subprocess
import uuid
import os
import tempfile
from .language_settings import LANGUAGE_SETTINGS
def run_code(code, language, input_data):
    file_id = str(uuid.uuid4())
    settings = LANGUAGE_SETTINGS.get(language.lower())

    if settings is None:
        return {"output": "", "error": f"❌ Unsupported language: {language}"}

    ext = settings['extension']
    filename = f'{file_id}{ext}'
    file_path = os.path.join('/tmp', filename)

    with open(file_path, 'w') as f:
        f.write(code)

    output = ''
    error = ''
    exe_name = ''

    try:
        # Compile if necessary (C++ or Java)
        if settings.get("compile"):
            exe_name = os.path.join('/tmp', f'{file_id}_exe') if language == 'cpp' else file_path.replace('.java', '')
            compile_cmd = settings['compile_cmd'](file_path, exe_name)

            compile_proc = subprocess.run(
                compile_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if compile_proc.returncode != 0:
                return {"output": "", "error": compile_proc.stderr.strip()}

            run_cmd = settings['run_cmd'](exe_name)
        else:
            run_cmd = settings['run_cmd'](file_path)

        # Run the code
        run_proc = subprocess.run(
            run_cmd,
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )

        output = run_proc.stdout.strip()
        error = run_proc.stderr.strip()

    except subprocess.TimeoutExpired:
        error = '❌ Execution timed out.'
    except Exception as e:
        error = f'❌ Internal Error: {str(e)}'
    finally:
        # Clean up files
        try: os.remove(file_path)
        except: pass
        if language == "cpp" and exe_name and os.path.exists(exe_name):
            try: os.remove(exe_name)
            except: pass
        elif language == "java":
            class_file = file_path.replace('.java', '.class')
            if os.path.exists(class_file):
                try: os.remove(class_file)
                except: pass
         
    return {"output": output, "error": error}
