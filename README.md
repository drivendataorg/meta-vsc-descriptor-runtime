### If you haven't already done so, start by reading the [Code Submission Format](https://www.drivendata.org/competitions/101/meta-video-similarity-descriptor/page/580/) page on the competition website.


# Meta Video Similarity Challenge: Descriptor Track Code Execution Runtime

[![Meta Video Similarity Competition](https://img.shields.io/badge/DrivenData%20Challenge-Meta%20Video%20Similarity-white?logo=data:image/png;base64,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)](https://www.drivendata.org/competitions/group/meta-video-similarity/)
![Python 3.9.13](https://img.shields.io/badge/Python-3.9.13-blue)
[![Build and publish image](https://github.com/drivendataorg/meta-vsc-descriptor-runtime/actions/workflows/build-images.yml/badge.svg?branch=main)](https://github.com/drivendataorg/meta-vsc-descriptor-runtime/actions/workflows/build-images.yml?query=main)

Welcome to the runtime repository for the [Meta Video Similarity Competition](https://www.drivendata.org/competitions/101/meta-video-similarity-descriptor/)!

As mentioned in the [Problem Description](https://www.drivendata.org/competitions/101/meta-video-similarity-descriptor/page/579/) and [Code Submission Format](https://www.drivendata.org/competitions/101/meta-video-similarity-descriptor/page/580/) pages, this competition is a **hybrid code execution** competition. This means that you will submit **both** the full set of query and reference descriptors that you generate for videos in the test set **as well as** the code that generates those descriptors. This repository contains the definition of the environment where your code submissions will run on a subset of videos in the query set to ensure that your submission meets the given resource constraints. It specifies both the operating system and the software packages that will be available to your solution.

This repository has three primary uses for competitors:

1. 💡 **[Quickstart example](https://github.com/drivendataorg/meta-vsc-descriptor-runtime/tree/main/submission_quickstart):** A minimal code example that runs successfully in the runtime environment and outputs a properly formatted submission tarfile. This will generate random descriptors, so unfortunately you won't win the competition with this example, but you can use it as a guide for bringing in your own work and generating a real submission.
2. 🔧 **Test your submission**: Test your submission with a locally running version of the container to discover errors before submitting to the competition site.
3. 📦 **Request new packages in the official runtime**: Since the Docker container will not have network access, all packages must be pre-installed. If you want to use a package that is not in the runtime environment, make a pull request to this repository.

 ----

### [Quickstart](#quickstart)
 - [Prerequisites](#prerequisites)
 - [Download the data](#download-the-data)
 - [Run Make commands](#run-make-commands)
### [Developing your own submission](#developing-your-own-submission)
 - [Steps](#steps)
 - [Logging](#logging)
### [Getting Started: the `vsc2022` repo](#getting-started-the-vsc2022-repo)
 - [A working benchmark submission](#a-working-benchmark-submission) 
### [Additional information](#additional-information)
 - [Scoring your submission](#scoring-your-submission)
 - [Runtime network access](#runtime-network-access)
 - [CPU and GPU](#cpu-and-gpu)
 - [Make commands](#make-commands)
 - [Updating runtime packages](#updating-runtime-packages)


----

## Quickstart

The quickstart example allows you to generate valid (but random) descriptors for the full set of query and reference videos, as well as an example `main.py` script for generating descriptors for the test subset.

This section guides you through the steps to generate a simple but valid submission for the competition.

### Prerequisites

First, make sure you have the prerequisites installed.

 - A clone or fork of this repository
 - At least 12 GB of free space for the Docker container images, and an additional 79GB of free space for storing the videos from the training set you'll use as your local test set (163GB if you download the entire dataset including the test set).
 - [Docker](https://docs.docker.com/get-docker/)
 - [GNU make](https://www.gnu.org/software/make/) (optional, but useful for running commands in the Makefile)

 ### Download the data

 Download the competition data to the `competition_data` by following the instructions on the [data download page](https://www.drivendata.org/competitions/101/meta-video-similarity-descriptor/data/). Once everything is downloaded and in the right location, it should look like this:
   
   ```
   competition_data/                # Runtime data directory
   ├── train/                       # Directory containing the training set
   │   ├── query_metadata.csv       # Training set metadata file
   │   ├── reference_metadata.csv   # Training set metadata file
   │   ├── ground_truth.csv         # Training set ground truth file
   │   ├── query/                   # Directory containing the test set query videos
   │   │   ├── Q10000.mp4
   │   │   ├── Q10001.mp4
   │   │   ├── Q10002.mp4
   │   │   └── ...
   │   └── reference/               # Directory containing the test set reference videos
   │       ├── R100000.mp4
   │       ├── R100001.mp4
   │       ├── R100002.mp4
   │       └── ...
   │
   └── test/                        # Directory containing the test set
   │   ├── query_metadata.csv       # Test set query metadata file
   │   ├── reference_metadata.csv   # Test set reference metadata file
       ├── query/                   # Directory containing the test set query videos
       │   ├── Q20000.mp4
       │   ├── Q20001.mp4
       │   ├── Q20002.mp4
       │   └── ...
       └── reference/               # Directory containing the test set reference videos
           ├── R200000.mp4
           ├── R200001.mp4
           ├── R200002.mp4
           └── ...
   ```

If you are competing in both tracks of the competition, you can symlink `competition_data` to a single folder where you have all the competition data stored to avoid having two copies of the 162GB dataset.

### Run Make commands

To test out the full execution pipeline, make sure Docker is running and then run the following commands in the terminal:

1. **`make pull`** pulls the latest official Docker image from the container registry ([Azure](https://azure.microsoft.com/en-us/services/container-registry/)). You'll need an internet connection for this.
2. **`make data-subset`** generates and copies a subset of the `competition_data/train` dataset into the `data` folder in the format it will exist in the code execution environment. By default, this will copy over videos and metadata from the training set, but you can modify both the proportion of videos copied and the source by editing the `Makefile`. Note that the subset of videos you will generate is different from the subset specified at runtime.
3. **`make pack-quickstart`** generates valid, random descriptors for the full query and reference sets, and then zips the contents of the `submission_quickstart` directory (including the `main.py` script which also generates random descriptors) and saves it as `submission/submission.zip`. The `submission.zip` file will contain both the `.npz` and `main.py` files, and is what you will upload to the DrivenData competition site for code execution. But first we'll test that everything looks good locally (see next step).
4. **`make test-submission`** will do a test run of your submission, simulating what happens during actual code execution. This command runs the Docker container with the requisite host directories mounted, and executes `main.py` to produce a tar file with your rankings for the full set and subset. 

```bash
make pull
make data-subset
make pack-quickstart
make test-submission
```

🎉 **Congratulations!** You've just completed your first test run for the Video Similarity Challenge Descriptor Track. If everything worked as expected, you should see a new file `submission/submission.tar.gz` has been generated. If you unpack this file, you should see a `full_rankings.csv` and a `subset_rankings.csv` csv file, each of which contains scored query-ref pairs that predict the video pairs most likely to have a derived content relationship based on your submitted descriptors. These rankings are generated from the [descriptor evaluation code](https://github.com/facebookresearch/vsc2022/blob/main/descriptor_eval.py) in Meta's [vsc2022 repository](https://github.com/facebookresearch/vsc2022)

If you were ready to make a real submission to the competition, you would upload the `submission.zip` file from step 2 above to the competition [Submissions page](https://www.drivendata.org/competitions/101/meta-video-similarity-descriptor/submissions/). The `submission.tar.gz` that is written out during code execution will get **scored** automatically using the [competition scoring metric](https://www.drivendata.org/competitions/101/meta-video-similarity-descriptor/page/579/#metric) to determine your rank on the leaderboard.

----

## Developing your own submission

Now that you've gone through the quickstart example, let's talk about how to develop your own solution for the competition.

### Steps

This section provides instructions on how to develop and run your code submission locally using the Docker container. To make things simpler, key processes are already defined in the `Makefile`. Commands from the `Makefile` are then run with `make {command_name}`. The basic steps are:

```
make pull
make data-subset
make pack-submission
make test-submission
```

Let's walk through what you'll need to do, step-by-step. The overall process here is very similar to what we've already covered in the [Quickstart](#quickstart), but we'll go into more depth this time around.

0. **[Set up the prerequisites](#prerequisites)**, including downloading the data.

1. **Download the official competition Docker image**, if you haven't already:

    ```bash
    $ make pull
    ```

2. ⚙️ **Develop your model.**  

   Keep in mind that the runtime already contains a number of packages that might be useful for you ([cpu](https://github.com/drivendataorg/meta-vsc-descriptor-runtime/blob/main/runtime/environment-cpu.yml) and [gpu](https://github.com/drivendataorg/meta-vsc-descriptor-runtime/blob/main/runtime/environment-gpu.yml) versions). If there are other packages you'd like added, see the section below on [updating runtime packages](#updating-runtime-packages).

3. **Save your `.npz` descriptor files and `main.py` script in the `submission_src` folder of the runtime repository.**
   * Working off the `main.py` template we've provided, you'll want to add code as necessary to process the queries, cache intermediate results as necessary, and write out your descriptors.
   * Make sure any model weights or other files you need are also saved in `submission_src` (you can include these in that folder or in a subfolder, e.g., `submission_src/model_assets`)

4. **Create a `submission/submission.zip` file containing your code and model assets:**

    ```bash
    $ make pack-submission
    cd submission_src; zip -r ../submission/submission.zip ./*
      adding: main.py (deflated 50%)
    ```

5. **Test your submission with `make test-submission`** 

    This command launches an instance of the competition Docker image, simulating the same process that will take place in the official code execution runtime.** The requisite host directories will be mounted on the Docker container, `submission/submission.zip` will be unzipped into the root directory of the container, and `main.py` will be executed to produce your subset rankings.

   ```
   $ make test-submission
   ```


> ⚠️ **Remember** in the official code execution environment, `/data` will contain just the subset of test set videos a and full metadata CSV files for the query and reference sets. When testing locally, the `/data` directory is a mounted version of whatever you have saved locally in this project's `data` directory. `make data-subset` generates a `data` directory that matches what will exist in the execution environment.


### Logging

When you run `make test-submission` the logs will be printed to the terminal and written out to `submission/log.txt`. If you run into errors, use the `log.txt` to determine what changes you need to make for your code to execute successfully. Note that the log messages generated by `tqdm` on a submission to the platform will not by default log until the interations have completed.


## Getting Started: the `vsc2022` repository

As part of this competition, our partners at Meta have made a benchmark solution available in the [vsc2022](https://github.com/facebookresearch/vsc2022) repository. You are encouraged to use this benchmark solution as a starting point for your own solution if you wish.

### A working benchmark solution

In addition to creating a quickstart solution, it may be instructive to use the provided benchmark code to generate an initial local submission. To do so, you would follow the instructions above as well as the instructions in the vsc2022 [documentation](https://github.com/facebookresearch/vsc2022/tree/main/docs) for [installation](https://github.com/facebookresearch/vsc2022/blob/main/docs/installation.md) and running the [baseline](https://github.com/facebookresearch/vsc2022/blob/main/docs/baseline.md). 

Your workflow might look something like this:

* Cloning and recursively updating submodules for the `vsc2022` repo into `submission_src`
* Downloading and transforming the sscd model into `submission_src/model_assets/`
* Running inference on the training query and reference datasets to generate descriptors
* Adapting `main.py` to call
    * Note: Within the code execution runtime, the conda environment is accessible to commands run via `subprocess` by including the prefix `conda run --no-capture-output -n condaenv [command]`, so your `main.py` might include a `subprocess` call to something that looks like:
    ```sh
    conda run --no-capture-output -n condaenv python -m vsc.baseline.inference
        --torchscript_path "/code_execution/vsc2022/vsc/baseline/adapted_sscd_disc_mixup.torchscript.pt"
        --accelerator=cuda --processes="1"
        --dataset_path "{QUERY_SUBSET_VIDEOS_FOLDER}"
        --output_file "{OUTPUT_FILE}"
    ```

---
## Additional information

### Scoring your submission

For convenience and consistency, the `vsc2022` repository, including the scoring scripts for both the descriptor track and the matching track, is included as a submodule of this runtime. The descriptor evaluation similarity search is also conducted by the code in this library. After cloning this repository, run `make update-submodules` to download the contents of `vsc2022` into the specified folder, and unpack the `submission.tar.gz` folder to obtain the generated rankings files to provide to `vsc2022/descriptor_eval.py`.

> Note: When evaluating your generated subset submission on the training set, you should provide only the subset of the ground truth that contains the query videos in the subset.

### Runtime network access

In the real competition runtime, all internet access is blocked. The local test runtime does not impose the same network restrictions. It's up to you to make sure that your code does not make requests to any web resources.

You can test your submission _without_ internet access by running `BLOCK_INTERNET=true make test-submission`.

### Downloading pre-trained weights

It is common for models to download pre-trained weights from the internet. Since submissions do not have open access to the internet, you will need to include all weights along with your `submission.zip` and make sure that your code loads them from disk and rather than the internet.


### CPU and GPU

For local testing, the `make` commands will try to select the CPU or GPU image automatically by setting the `CPU_OR_GPU` variable based on whether `make` detects `nvidia-smi`.

You can explicitly set the `CPU_OR_GPU` variable by prefixing the command with:
```bash
CPU_OR_GPU=cpu <command>
```

**If you have `nvidia-smi` and a CUDA version other than 11**, you will need to explicitly set `make test-submission` to run on CPU rather than GPU. `make` will automatically select the GPU image because you have access to GPU, but it will fail because `make test-submission` requires CUDA version 11.
```bash
CPU_OR_GPU=cpu make pull
CPU_OR_GPU=cpu make test-submission
```

If you want to try using the GPU image on your machine but you don't have a GPU device that can be recognized, you can use `SKIP_GPU=true`. This will invoke `docker` without the `--gpus all` argument.

### Updating runtime packages

If you want to use a package that is not in the environment, you are welcome to make a pull request to this repository. If you're new to the GitHub contribution workflow, check out [this guide by GitHub](https://docs.github.com/en/get-started/quickstart/contributing-to-projects). The runtime manages dependencies using [conda](https://docs.conda.io/en/latest/) environments. [Here is a good general guide](https://towardsdatascience.com/a-guide-to-conda-environments-bc6180fc533) to conda environments. The official runtime uses **Python 3.9.13** environments.

To submit a pull request for a new package:

1. Fork this repository.

2. Edit the [conda](https://docs.conda.io/en/latest/) environment YAML files, `runtime/environment-cpu.yml` and `runtime/environment-gpu.yml`. There are two ways to add a requirement:
    - Add an entry to the `dependencies` section. This installs from a conda channel using `conda install`. Conda performs robust dependency resolution with other packages in the `dependencies` section, so we can avoid package version conflicts.
    - Add an entry to the `pip` section. This installs from PyPI using `pip`, and is an option for packages that are not available in a conda channel.

    For both methods be sure to include a version, e.g., `numpy==1.20.3`. This ensures that all environments will be the same.

3. Locally test that the Docker image builds and tests successfully for CPU and GPU images:

    ```sh
    CPU_OR_GPU=cpu make build
    CPU_OR_GPU=cpu make test-container
    CPU_OR_GPU=gpu make build
    CPU_OR_GPU=gpu make test-container # Ensure this command is run on a machine with `nvidia-smi`
    ```

4. Commit the changes to your forked repository.

5. Open a pull request from your branch to the `main` branch of this repository. Navigate to the [Pull requests](https://github.com/drivendataorg/meta-vsc-descriptor-runtime/pulls) tab in this repository, and click the "New pull request" button. For more detailed instructions, check out [GitHub's help page](https://help.github.com/en/articles/creating-a-pull-request-from-a-fork).

6. Once you open the pull request, Github Actions will automatically try building the Docker images with your changes and running the tests in `runtime/tests`. These tests can take up to 30 minutes, and may take longer if your build is queued behind others. You will see a section on the pull request page that shows the status of the tests and links to the logs.

7. You may be asked to submit revisions to your pull request if the tests fail or if a DrivenData team member has feedback. Pull requests won't be merged until all tests pass and the team has reviewed and approved the changes.


### Make commands

Running `make` at the terminal will tell you all the commands available in the repository:

```
❯ make

Settings based on your machine:
SUBMISSION_IMAGE=db463d9663ac   # ID of the image that will be used when running test-submission

Available competition images:
meta-vsc-descriptor-runtime:gpu-local (f314bbf3beed); meta-vsc-descriptor-runtime:cpu-local (db463d9663ac);

Available commands:

build               Builds the container locally 
clean               Delete temporary Python cache and bytecode files 
interact-container  Start your locally built container and open a bash shell within the running container; same as submission setup except has network access 
pack-benchmark      Creates a submission/submission.zip file from the source code in submission_benchmark 
pack-quickstart     Creates a submission/submission.zip file from the source code in submission_quickstart 
pack-submission     Creates a submission/submission.zip file from the source code in submission_src 
pull                Pulls the official container from Azure Container Registry 
test-container      Ensures that your locally built container can import all the Python packages successfully when it runs 
test-submission     Runs container using code from `submission/submission.zip` and data from `data/`

```

---

## Good luck! And have fun!

Thanks for reading! Enjoy the competition, and [hit up the forums](https://community.drivendata.org/c/video-similarity-challenge/90) if you have any questions!
