import subprocess
import uuid
import os

# You can configure this if needed
LANGUAGE_SETTINGS = {
    'Python': {
        'extension': '.py',
        'run_cmd': lambda file: ['python3', file]
    },
    'C++': {
        'extension': '.cpp',
        'compile_cmd': lambda file, out: ['g++', file, '-o', out],
        'run_cmd': lambda out: [f'./{out}']
    },
    'Java': {
        'extension': '.java',
        'compile_cmd': lambda file, _: ['javac', file],
        'run_cmd': lambda file: ['java', file.replace('.java', '')]
    }
}

def run_code(code, language, input_data):
    file_id = str(uuid.uuid4())
    settings = LANGUAGE_SETTINGS.get(language)
    ext = settings['extension']
    filename = f'{file_id}{ext}'
    file_path = f'/tmp/{filename}'
    with open(file_path, 'w') as f:
        f.write(code)

    exe_output = ''
    exe_error = ''

    try:
        if 'compile_cmd' in settings:
            exe_name = f'/tmp/{file_id}_exe'
            compile_result = subprocess.run(
                settings['compile_cmd'](file_path, exe_name),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            if compile_result.returncode != 0:
                return '', compile_result.stderr.strip()

            run_cmd = settings['run_cmd'](exe_name if language == 'C++' else filename)
        else:
            run_cmd = settings['run_cmd'](file_path)

        run_result = subprocess.run(
            run_cmd,
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5  # prevent infinite loops
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
        if language == 'C++':
            try: os.remove(exe_name)
            except: pass
        elif language == 'Java':
            try: os.remove(file_path.replace('.java', '.class'))
            except: pass

    return exe_output, exe_error
