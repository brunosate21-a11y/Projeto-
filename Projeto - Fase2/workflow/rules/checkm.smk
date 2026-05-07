rule checkm:
    input:
        genome = "data/mags/{mag}.fna"
    output:
        output_dir = directory("results/checkm/{mag}"),
        quality    = "results/checkm/{mag}/quality.tsv"
    threads: 4
    log:
        "logs/checkm/{mag}.log"
    wrapper:
        "file:wrappers/checkm"
        