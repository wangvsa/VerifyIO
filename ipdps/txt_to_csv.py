import csv
import re
import argparse
import pandas as pd

#CSV_HEADER=['Test', 'Read Trace (secs)', 'Match MPI (secs)',
#            'Graph Edges', 'Build HB Graph (secs)', 'Graph Nodes',
#            'Vector Clock (secs)', 'Verification (secs)',
#            'Semantics Violations', 'Total Conflicts', 'Semantics']

CSV_HEADER=['test', 'io_time', 'match_mpi_calls', 'mpi_edges', 'build_happens-before_graph', 'nodes','run_the_algorithm', 'verification_time', 'total_semantic_violation', 'total_conflict_pairs', 'semantics']

def parser(txt_file):
    with open(txt_file, "r") as file:
        log_data = file.read()

    data = []
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
    test_name = ""
    for line in lines:
        line = line.strip()
        if dir_match := dir_regex.match(line):
            test_name = dir_match.group(1)
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
            entry["semantics"] = verification_regex_match.group(1)
            entry["verification_time"] = verification_regex_match.group(2)
            entry["test"] = test_name 
            data.append(entry)
            entry = {}

    return data

def reshape_and_write_csv(parsed_data, csv_file):
    df = pd.DataFrame(parsed_data, columns=CSV_HEADER)
    if args.group_by_test:
        df_no_conflicts = df.drop(columns='total_conflict_pairs')
        df_pivot = df_no_conflicts.pivot(index='test', columns='semantics')
        df_pivot.columns = ['_'.join(col).strip() for col in df_pivot.columns.values]
        df_pivot = df_pivot.reset_index()
        df_total_conflicts = df[['test', 'total_conflict_pairs']].drop_duplicates()
        df_pivot = pd.merge(df_pivot, df_total_conflicts, on='test')
        df_pivot.to_csv(csv_file, index=False)
    else:
        df.to_csv(csv_file, index=False)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description="Convert text result to CSV files")
    arg_parser.add_argument("txt_file", type=str,  nargs='?', help="Path to the text result file")
    arg_parser.add_argument("csv_file", type=str,  nargs='?', help="Path to the output CSV file")
    arg_parser.add_argument("--group_by_test", action="store_true", help="Group data by consistency semantics", required=False)

    args = arg_parser.parse_args()
    parsed_data = parser(args.txt_file)
    reshape_and_write_csv(parsed_data, args.csv_file)
