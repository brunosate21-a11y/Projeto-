rule carveme:
    input:
        genome  = "data/mags/{mag}.fna"
    output:
        model   = "results/gems/{mag}.xml"
    params:
        solver  = config["solver"],
        media   = config["media"]
    threads: 4
    log:
        "logs/carveme/{mag}.log"
    wrapper:
        "file:wrappers/carveme"
        