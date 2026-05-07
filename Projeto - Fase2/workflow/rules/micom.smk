rule micom:
    input:
        models          = expand("results/gems/{mag}.xml", mag=MAGS)
    output:
        exchange_fluxes = "results/micom/exchange_fluxes.tsv"
    log:
        "logs/micom/micom.log"
    wrapper:
        "file:wrappers/micom"
        