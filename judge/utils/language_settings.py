LANGUAGE_SETTINGS = {
    'python': {
        'extension': '.py',
        'run_cmd': lambda file: ['python', file]
    },
    'cpp': {
        'extension': '.cpp',
        'compile_cmd': lambda file, out: ['g++', file, '-o', out],
        'run_cmd': lambda out: [f'./{out}']
    },
    'java': {
        'extension': '.java',
        'compile_cmd': lambda file, _: ['javac', file],
        'run_cmd': lambda file: ['java', file.replace('.java', '')]
    }
}
