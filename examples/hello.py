import pygrunt
import pygrunt.compiler

def build():
    # Setup project
    project = pygrunt.Project('hello')
    project.working_dir = 'hello/'
    project.output_dir = 'build/'

    # Sanitize aka. set reasonable defaults
    # Also needed before adding sources
    # ( otherwise pygrunt will be looking in the wrong directories )
    project.sanitize()

    # Add sources
    project.sources.add('*.c')

    # Compile the whole thing
    project.compiler = pygrunt.compiler.any()
    project.compile()
