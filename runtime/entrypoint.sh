#!/bin/bash
set -euxo pipefail
exit_code=0

{
    cd /code_execution

    echo "List installed packages"
    echo "######################################"
    conda list -n condaenv
    echo "######################################"

    echo "Unpacking submission..."
    unzip ./submission/submission.zip -d ./
    ls -alh

    # Generate descriptors on a subset of query videos (primarily for measurement of 
    # resouce usage but also optionally for performance eval). 
    # Generate resource usage report

    # if [ -f "main.py" ]
    # then
    #     echo "Generating descriptors on a subset of query videos..."

    #     time how long this takes?

    #     conda run --no-capture-output -n condaenv python main.py

        # if [[ -f "subset_query_descriptors.npz" && -f "reference_descriptors.npz" ]]
        # then
        #     echo "Running similarity search to generate rankings for scoring..."
        #     conda run --no-capture-output -n condaenv \
        #         python /opt/scoring/generate_rankings.py \
        #         subset_query_descriptors.npz reference_descriptors.npz \
        #         subset_rankings.csv
        #     echo "... finished"
        #     else
        #         echo "WARNING: Could not find subset_query_descriptors.npz or reference_descriptors.npz in submission.zip"
        # fi
	#     echo "... finished"

    #     else
    #         echo "WARNING: Could not find main.py in submission.zip"
    # fi

    # Use descriptors to generate rank submission
    #   Load user query and reference descriptors
    #       (Optionally replace loaded descriptors with subset of generated descriptors)
    #   Validate data format
    #   Run similarity search
    #   Generate CSV of scored pairings for submission to RankLearningScorer using MicroAP
    # Generate subset_rankings.csv

    # Expecting two files - query npz and ref npz, generate full_rankings.csv
    if [[ -f "query_descriptors.npz" && -f "reference_descriptors.npz" ]]
    then
        echo "Running similarity search to generate rankings for scoring..."
        conda run --no-capture-output -n condaenv \
            python /opt/scoring/generate_rankings.py \
            query_descriptors.npz reference_descriptors.npz \
            full_rankings.csv
	    echo "... finished"
        else
            echo "ERROR: Could not find query_descriptors.npz or reference_descriptors.npz in submission.zip"
            exit_code=1
    fi

    # Tar the full ranking csv and the subset ranking csv together to form the submission file
    tar -czvf /code_execution/submission/submission.tar.gz \
        full_rankings.csv \
        subset_rankings.csv \

    echo "================ END ================"
} |& tee "/code_execution/submission/log.txt"

cp /code_execution/submission/log.txt /tmp/log
exit $exit_code
