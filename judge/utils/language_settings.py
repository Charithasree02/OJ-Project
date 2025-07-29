import os

LANGUAGE_SETTINGS = {
    "python": {
        "extension": ".py",
        "run_cmd": lambda file: ["python3", file],
    },
    "cpp": {
        "extension": ".cpp",
        "compile": True,
        "compile_cmd": lambda file, exe: ["g++", file, "-o", exe],
        "run_cmd": lambda exe: [exe],
    },
    "java": {
        "extension": ".java",
        "compile": True,
        "compile_cmd": lambda file, _: ["javac", file],
        "run_cmd": lambda file: ["java", os.path.splitext(os.path.basename(file))[0]],
    }
}
