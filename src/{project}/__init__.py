__version__ = "0.1.0"

# Shared Typer settings - import in all CLI modules
# Enables -h as alias for --help (standard convention)
TYPER_SETTINGS: dict = {"help_option_names": ["-h", "--help"]}
