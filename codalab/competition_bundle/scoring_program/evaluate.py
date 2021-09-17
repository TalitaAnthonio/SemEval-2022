
#!/usr/bin/env python3

import sys
import os
import os.path
import pandas as pd 


def compute_accuracy(submission_answer_dict, truth_dict): 
    """
        Compute the accuracy score. 

    """
    # compute the accuracy: 
    results = []
    for id, answer in submission_answer_dict.items(): 
        if submission_answer_dict[id] == truth_dict[id]: 
            results.append(1)

        else:
            results.append(0)


    if len(submission_answer_dict.keys()) != len(truth_dict.keys()): 
        raise ValueError("Number of instances {0} is not the same as truth dict {1}".format(len(submission_answer_dict.keys()), len(truth_dict.keys())))
 
    accuracy_score = sum(results)/len(results)
    sys.stdout.write("{0} {1}".format(sum(results), len(results)))
    return accuracy_score

def main(): 
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    submit_dir = os.path.join(input_dir, 'res')
    truth_dir = os.path.join(input_dir, 'ref')

    if not os.path.exists(truth_dir): 
       raise ValueError("Path {0} does not exist".format(truth_dir))
    
    if not os.path.exists(submit_dir): 
        raise ValueError("Path {0} does not exist".format(submit_dir))
    


    if not os.path.isdir(submit_dir):
        print("Doesn't exist {0}".format(submit_dir))

    if os.path.isdir(submit_dir) and os.path.isdir(truth_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)


        # write the score to the output file. 
        output_filename = os.path.join(output_dir, 'scores.txt')
        output_file = open(output_filename, 'w')


        # read the files 
        truth_file = os.path.join(truth_dir, "truth.tsv")
        truth = pd.read_csv(truth_file, sep='\t')
        truth_dict = {row["Id"]: row["Class"] for index,row in truth.iterrows()}
        

        # read the submission answer file and compute accuracy. 
        submission_answer_file = os.path.join(submit_dir, "answers.tsv")
        submission_answer = pd.read_csv(submission_answer_file, sep='\t')
        submission_answer_dict = {row["Id"]: row["Class"] for index, row in submission_answer.iterrows()}



        accuracy_score = compute_accuracy(submission_answer_dict, truth_dict)

        # just a dummy for now 
        ranking_score = 0.75
        output_file.write("ranking_score:{:.3f}\n".format(ranking_score))
        output_file.write("accuracy_score:{:.3f}\n".format(accuracy_score))
        output_file.close()

if __name__ == "__main__":
    main()