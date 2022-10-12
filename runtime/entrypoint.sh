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

    # Use submitted code to generate descriptors on a subset of query videos 
    if [ -f "main.py" ]
    then
        echo "Generating descriptors on a subset of query videos..."

        conda run --no-capture-output -n condaenv python main.py

        # If code successfully generates subset of descriptors, run similarity search
        # to generate similarity rankings
        if [[ -f "subset_query_descriptors.npz" && -f "reference_descriptors.npz" ]]
        then
            echo "Running similarity search to generate subset rankings for scoring..."
            conda run --no-capture-output -n condaenv \
                python /opt/scoring/generate_rankings.py \
                subset_query_descriptors.npz reference_descriptors.npz \
                subset_rankings.csv
            echo "... finished"
            else
                echo "WARNING: Could not find generated subset_query_descriptors.npz or find reference_descriptors.npz in submission.zip"
                echo "query_id,reference_id,score" >> subset_rankings.csv
        fi
	    echo "... finished"

        else
            echo "WARNING: Could not find main.py in submission.zip"
            echo "query_id,reference_id,score" >> subset_rankings.csv
    fi

    # Generate full rankings from submitted descriptors via a similarity search
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
        subset_rankings.csv

    echo "================ END ================"
} |& tee "/code_execution/submission/log.txt"

cp /code_execution/submission/log.txt /tmp/log
exit $exit_code
