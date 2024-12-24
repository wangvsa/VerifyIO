# IPDPS'25 Reproducibility Effort

To ensure reproducibility, a Docker environment containing the required source code and traces has been provided. Since the standard test cases of the corresponding high-level I/O libraries were analyzed using VerifyIO for the IPDPS paper, a script was developed and adapted to automate this process. This enables the verification to be performed in batches for multiple traces. The following steps outline the process for handling multiple traces more efficiently:

## Step 1. Environment Setup:

### Prerequisites

- Docker installed on your local system
- Ensure that you have the correct Docker image available locally. If not, pull the image from a Docker registry using:

```bash
docker pull <image_name>:<tag>
```

### Run the Docker Container

```bash
docker run -it --name <container_name> ....

```

### Exitand stop the container,
```bash
exit

```

```bash
docker stop <container_name>
docker rm <container_name>
```


## Step 2. Batch Execution:
Navigate to the directory where the corresponding script resides:

### Conflict Detection:
The [`auto_detect.sh`](https://github.com/wangvsa/VerifyIO/blob/main/ipdps/auto_detect.sh) script can be used to process multiple traces and detect conflicts. The script requires the path to the directory containing the traces as an argument. Please adjust the configuartion for resource manager accordingly. 

```bash
./auto_detect.sh /path/to/target/traces
```

### Semantic Verification
The [`auto_verify.sh`](https://github.com/wangvsa/VerifyIO/blob/main/ipdps/auto_verify.sh) script can be used for verification. This script requires the path to the directory containing the traces, and the path to verifyio as arguments. By default, it verifies all supported semantics, i.e., POSIX, MPI-IO, Commit, Session with Vector clock algorithm.

```bash
./auto_verify.sh /path/to/target/traces /path/to/verifyio.py
```

## Step 3. Post-Processing and Visualization:

### Heatmap Plot
For visualizing up to three CSV files in a single heatmap, use the following argument:
```bash
python verifyio_plot_heatmap.py --files="/path/to/output1.csv" "/path/to/output2.csv" "/path/to/output3.csv"
```



