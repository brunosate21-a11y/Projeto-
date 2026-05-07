__author__ = "Bruno Ferreira"
__license__ = "MIT"

from snakemake.shell import shell

models       = snakemake.input.models
global_out   = snakemake.output.global_scores
detailed_out = snakemake.output.detailed
solver       = snakemake.params.get("solver", "glpk")

models_str = " ".join(models)

log = snakemake.log_fmt_shell(stdout=True, stderr=True)

shell(
    "smetana {models_str} "
    "--mode global "
    "--solver {solver} "
    "--output {global_out} "
    "{log}"
)

shell(
    "smetana {models_str} "
    "--mode detailed "
    "--solver {solver} "
    "--output {detailed_out} "
    "{log}"
)
