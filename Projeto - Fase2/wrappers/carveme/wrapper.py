__author__ = "Bruno Ferreira"
__license__ = "MIT"

from snakemake.shell import shell

genome = snakemake.input.genome
model  = snakemake.output.model
solver = snakemake.params.get("solver", "glpk")
media  = snakemake.params.get("media", "M9")

log = snakemake.log_fmt_shell(stdout=True, stderr=True)

shell(
    "carve {genome} "
    "--output {model} "
    "--solver {solver} "
    "--mediadb {media} "
    "{log}"
)
