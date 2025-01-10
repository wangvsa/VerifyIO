# IPDPS'25 Reproducibility Effort

To ensure reproducibility, we provide a Docker environment containing the required source code and trace files. The standard test cases of the corresponding high-level I/O libraries were analyzed using VerifyIO, as presented in the IPDPS paper. To streamline this process, a script was developed for batch verification across multiple traces. Follow the steps below to reproduce our results efficiently.

## 1. Install and Run Docker

Please make sure Docker is installed on your system before proceeding.

Pull the VerifyIO Docker image:
```bash
docker pull wangvsa/verifyio
```

Create a local directory to save the results:
```bash
mkdir ~/ipdps-verifyio-result
```

Then run the Docker iamge:
```bash
docker run --rm -it -v ~/ipdps-verifyio-result:/ipdps wangvsa/verifyio /bin/bash
```

Notes:
- The `--rm` parameter automatically deletes the Docker container after exiting.
- The `-v` option mounts your local directory to the Docker container’s /ipdps directory, ensuring data persistence outside the container.


## 2. Reproduce the IPDPS result:

Once inside the Docker container, you should be at the `/ipdps` directory:

```bash
root@933cb4b115cb:/ipdps# pwd
/ipdps
```

Our IPDPS paper presents two tools: Recorder and VerifyIO. They are pre-compiled and installed in the `/source` directory:

```bash
root@933cb4b115cb:/ipdps# ls /source
Recorder  VerifyIO
root@933cb4b115cb:/ipdps# echo $RECORDER_INSTALL_PATH/
/source/Recorder/install/
root@933cb4b115cb:/ipdps# echo $VERIFYIO_INSTALL_PATH/
/source/VerifyIO/
```

### 2.1 Download dataset

Our paper verifies the consistency semantics of 91 built-in tests from three high-level I/O libraries against four consistency models.
The dataset used in our paper is available on [Zenodo](https://doi.org/10.5281/zenodo.14553174).

Use the provided script `01-download-dataset.sh` to download and extract the trace files:
```bash
$VERIFYIO_INSTALL_PATH/ipdps/01-download-dataset.sh
```

The script will download, decompress and save all trace files in the `./dataset` directory:
```bash
root@933cb4b115cb:/ipdps# ls ./dataset/*
dataset/hdf5-1.14.4-3-recorder-traces:
2Gio   cache		 init_term  pflush2	 pread	   pshutdown	   shapesame  vfd
bigio  filters_parallel  mpi	    pmulti_dset  prestart  select_io_dset  testphdf5

dataset/netcdf-4.9.2-recorder-traces:
h_par		mpi_parallel  parallel	 parallel3  parallel5  parallel_compress  quantize_par
h_par_compress	nc4perf       parallel2  parallel4  parallel6  parallel_zlib	  simplerw_coll_r

dataset/pnetcdf-1.13.0-recorder-traces:
add_var		  flexible	  ivarn			  put_all_kinds       test_vard_rec	tst_redefine
alignment_test	  flexible2	  large_var_cdf5	  put_parameter       test_vardf	tst_symlink
attrf		  flexible_api	  last_large_var	  record	      test_vardf90	tst_vars_fill
buftype_free	  flexible_var	  mix_collectives	  redef1	      test_varm		tst_version
buftype_freef	  flexible_varm   modes			  scalar	      tst_def_var_fill	varn_contig
check_striping	  inq_num_vars	  ncmpi_vars_null_stride  test_erange	      tst_del_attr	varn_int
check_type	  inq_num_varsf   noclobber		  test_fillvalue      tst_dimsizes	varn_intf
collective_error  inq_recsize	  nonblocking		  test_get_varn       tst_free_comm	varn_real
erange_fill	  inq_recsizef	  null_args		  test_vard	      tst_info		vectors
error_precedence  iput_all_kinds  one_record		  test_vard_multiple  tst_max_var_dims
```

### 2.2 Conflict detection

To detect conflicts across multiple traces, use the `02-detect-conflicts.sh` script. Specify the directory containing the library test traces.

For example, the following command performs conflict detection on all PnetCDF tests:
```bash
$VERIFYIO_INSTALL_PATH/ipdps/02-detect-conflicts.sh ./dataset/pnetcdf-1.13.0-recorder-traces
```

### 2.3 Semantic verification

For semantic verification, use the `03-perform-verification.sh` script. Provide the directory containing the trace files as an argument.
By default, this script verifies all supported semantics, including POSIX, MPI-IO, Commit, and Session, using a vector clock algorithm.

For example, the following command performs semantic verification on all PnetCDF tests:
```bash
$VERIFYIO_INSTALL_PATH/ipdps/03-perform-verification.sh ./dataset/pnetcdf-1.13.0-recorder-traces
```
Once the command finishes, the result will be written to `./result/pnetcdf.csv`.

Similarly, you can perform verification on the tests of the other two libraries as well. Note that some NetCDF and HDF5 tests can take some time to finish; For those tests, you may need to grant your Docker engine more memory (>8GB).

For validation purposes (and to save time), we have included the resulting CSV files for all three library tests at `$VERIFYIO_INSTALL_PATH/ipdps/result`.
```bash
root@933cb4b115cb:/ipdps# ls $VERIFYIO_INSTALL_PATH/ipdps/result/*.csv
hdf5.csv netcdf.csv pnetcdf.csv
```

## 3. Post-Processing and Visualization:

The CSV files generated from the previous step contain all the necessary data for conducting the analyses discussed in our paper. This data includes the number of conflicts, the number of semantic violations, detailed timing information, and more. All the tables and figures presented in the Evaluation section (Sec. V) of our paper can be reproduced using these three CSV files.

For instance, the heatmap figure (Fig. 4) in the paper can be generated using:
```bash
$VERIFYIO_INSTALL_PATH/ipdps/csv_to_heatmap.py $VERIFYIO_INSTALL_PATH/ipdps/result/hdf5.csv $VERIFYIO_INSTALL_PATH/ipdps/result/netcdf.csv $VERIFYIO_INSTALL_PATH/ipdps/result/pnetcdf.csv
```

The heatmap figure will be written to the current directory.
![heatmap](./_static/heatmap.png)

You can also generate a single heatmap from the PnetCDF CSV file you created in step 2.3.
```bash
$VERIFYIO_INSTALL_PATH/ipdps/csv_to_heatmap.py ./result/pnetcdf.csv
```


Finally, exit the container once you are done.
```bash
exit
```
