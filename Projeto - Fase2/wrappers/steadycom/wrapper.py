__author__ = "Bruno Ferreira"
__license__ = "MIT"

from snakemake.shell import shell

models      = snakemake.input.models
abundances  = snakemake.output.abundances

models_str = " ".join(models)

log = snakemake.log_fmt_shell(stdout=True, stderr=True)

shell(
    "python -c \""
    "from cobra.io import read_sbml_model; "
    "print('SteadyCom placeholder')\" "
    "{log}"
)
