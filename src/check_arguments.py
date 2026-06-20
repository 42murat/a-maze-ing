from src.maze import MazeParameters

def check_arguments(argv: list[str]) -> MazeParameters:
    """Checks whether file with maze parameters exist, and if it's
    content is valid.
    
    Basically this makes all this:
        Your program must handle all errors gracefully: invalid configuration,
        file not found, bad syntax, impossible maze parameters, etc. It must
        never crash unexpectedly, and must always provide a clear error
        message to the user."""
    ...
    return MazeParameters()
