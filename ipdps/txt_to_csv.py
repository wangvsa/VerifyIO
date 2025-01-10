import csv
import re
import argparse
import pandas as pd


def parser(path, dir_prefix=None):
    with open(path, "r") as file:
        log_data = file.read()

    data = []
    # dir_regex = re.compile(r"Perform verification on\s+(.*/)")
    dir_regex = re.compile(r"Perform verification on\s+.+/([^/]+)/$")
    io_time_regex = re.compile(r"Step 1. read trace records and conflicts time:\s+([\d.]+)\s+secs")
    mpi_calls_regex = re.compile(r"Step 2. match mpi calls:\s+([\d.]+)\s+secs, mpi edges:\s+(\d+)")
    happens_before_regex = re.compile(r"Step 3. build happens-before graph:\s+([\d.]+)\s+secs, nodes:\s+(\d+)")
    run_the_algorithm_regex = re.compile(r"Step 4. run vector clock algorithm:\s+([\d.]+)\s+secs")
    semantic_violation_regex = re.compile(r"Total semantic violations:\s+(\d+)")
    conflict_pairs_regex = re.compile(r"Total conflict pairs:\s+(\d+)")
    verification_regex = re.compile(r"Step 5\.\s+(POSIX|MPI-IO|Commit|Session)\s+semantics\s+verification\s+time:\s+(\d+\.\d+)\s+secs")

    lines = log_data.strip().split("\n")
    entry = {}
    current_name = ""
    for line in lines:
        line = line.strip()
        if dir_match := dir_regex.match(line):
            current_name = dir_match.group(1)
        elif io_time_match := io_time_regex.search(line):
            entry["io_time"] = io_time_match.group(1)
        elif mpi_calls_match := mpi_calls_regex.search(line):
            entry["match_mpi_calls"] = mpi_calls_match.group(1)
            entry["mpi_edges"] = mpi_calls_match.group(2)
        elif happens_before_match := happens_before_regex.search(line):
            entry["build_happens-before_graph"] = happens_before_match.group(1)
            entry["nodes"] = happens_before_match.group(2)
        elif run_the_algorithm_match := run_the_algorithm_regex.search(line):
            entry["run_the_algorithm"] = run_the_algorithm_match.group(1) 
        elif semantic_violation_match := semantic_violation_regex.search(line):
            entry["total_semantic_violation"] = semantic_violation_match.group(1)
        elif conflict_pairs_match := conflict_pairs_regex.search(line):
            entry["total_conflict_pairs"] = conflict_pairs_match.group(1)
        elif verification_regex_match := verification_regex.search(line):
            entry["api"] = verification_regex_match.group(1)
            entry["verification_time"] = verification_regex_match.group(2)
            if dir_prefix is None:
                entry["directory_name"] = current_name
            else:
                split_str = current_name.split(dir_prefix)
                if len(split_str) > 1:
                    entry["directory_name"] = split_str[1]
                else:
                    entry["directory_name"] = None
            data.append(entry)
            entry = {}

    return data


def to_api_format(data):
    df = pd.DataFrame(data, columns=[
        'directory_name', 'io_time', 'match_mpi_calls', 'mpi_edges', 'build_happens-before_graph', 'nodes', 
        'run_the_algorithm', 'verification_time', 'total_semantic_violation', 'total_conflict_pairs', 'api'
    ])
    df_no_conflicts = df.drop(columns='total_conflict_pairs')
    df_pivot = df_no_conflicts.pivot(index='directory_name', columns='api')
    df_pivot.columns = ['_'.join(col).strip() for col in df_pivot.columns.values]
    df_pivot = df_pivot.reset_index()
    df_total_conflicts = df[['directory_name', 'total_conflict_pairs']].drop_duplicates()
    df_pivot = pd.merge(df_pivot, df_total_conflicts, on='directory_name')
    return df_pivot



def write_to_csv(data, csv_file):
    with open(csv_file, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["directory_name", "io_time", "match_mpi_calls", "mpi_edges", "build_happens-before_graph", "nodes", "run_the_algorithm", "verification_time", "total_semantic_violation", "total_conflict_pairs", "api"])
        writer.writeheader()
        writer.writerows(data)

    print(f"Data has been written to {csv_file}")

def write_df_to_csv(df, csv_file):
    df.to_csv(csv_file, index=False)
    print(f"Data has been written to {csv_file}")


def reshape_and_write_csv(parsed_data, output_csv):
    df = pd.DataFrame(parsed_data, columns=[
        'directory_name', 'io_time', 'match_mpi_calls', 'mpi_edges', 'build_happens-before_graph', 'nodes', 
        'run_the_algorithm', 'verification_time', 'total_semantic_violation', 'total_conflict_pairs', 'api'
    ])
    if args.group_by_api:
        df_no_conflicts = df.drop(columns='total_conflict_pairs')
        df_pivot = df_no_conflicts.pivot(index='directory_name', columns='api')
        df_pivot.columns = ['_'.join(col).strip() for col in df_pivot.columns.values]
        df_pivot = df_pivot.reset_index()
        df_total_conflicts = df[['directory_name', 'total_conflict_pairs']].drop_duplicates()
        df_pivot = pd.merge(df_pivot, df_total_conflicts, on='directory_name')
        df_pivot.to_csv(output_csv, index=False)
    else:
        df.to_csv(output_csv, index=False)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description="Convert text result to CSV files")
    arg_parser.add_argument("txt_file", type=str,  nargs='?', help="Path to the text result file", required=True)
    arg_parser.add_argument("csv_file", type=str,  nargs='?', help="Path to the output CSV file", required=True)
    arg_parser.add_argument("--dir_prefix", type=str, help="Remove the directory prefix", required=False)
    arg_parser.add_argument("--group_by_api", action="store_true", help="Group data by API", required=False)

    args = arg_parser.parse_args()
    parsed_data = parser(args.path, args.dir_prefix)
    reshape_and_write_csv(parsed_data, args.csv_file)
