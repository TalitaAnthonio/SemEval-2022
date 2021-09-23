
#!/usr/bin/env python3
from __future__ import division
from scoring_program.format_checker_for_submission import check_format_of_submission
from ranking_score import score_ranking_task
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
        output_file = open(output_filename, 'wb')


        # read the truth file 
        truth_file = os.path.join(truth_dir, "truth.tsv")

        # list the files in the directory 
        path_to_classification = os.path.join(submit_dir, "classification")
        path_to_ranking = os.path.join(submit_dir, "ranking")
        files_in_submit_dir_classification = [file for file in os.listdir(path_to_classification)]
        files_in_submit_dir_ranking = [file for file in os.listdir(path_to_ranking)]

        if 'classification_answers.tsv' in files_in_submit_dir_classification and "ranking_answers.tsv" in files_in_submit_dir_ranking:  
            # read the truth files. 
            sys.stdout.write("participation in both tasks")
     
            # read the submitted file 
            submission_answer_file = os.path.join(submit_dir, "classification", "classification_answers.tsv")
            submission_answer = pd.read_csv(submission_answer_file, sep='\t', header=None)
            check_format_of_submission(submission_answer, evaluation_mode="classification")
            submission_answer_dict = {row[0]: row[1] for index, row in submission_answer.iterrows()}

            # compute the accuracy 
            truth = pd.read_csv(truth_file, sep='\t')
            del truth['Rating']
            truth_dict = {row["Id"]: row["Class"] for index,row in truth.iterrows()}
            accuracy_score = compute_accuracy(submission_answer_dict, truth_dict)
            
            # compute the ranking score 
            submission_answer_file = os.path.join(submit_dir, "ranking", "ranking_answers.tsv")
            ranking_score = score_ranking_task(submission_answer_file, truth_file)
        
        elif 'classification_answers.tsv' in files_in_submit_dir_classification: 
            sys.stdout.write("participation in classification")
            submission_answer_file = os.path.join(submit_dir, "classification", "classification_answers.tsv")
            submission_answer = pd.read_csv(submission_answer_file, sep='\t', header=None)
            check_format_of_submission(submission_answer, evaluation_mode="classification")
            submission_answer_dict = {row[0]: row[1] for index, row in submission_answer.iterrows()}

            # compute the accuracy 
            truth = pd.read_csv(truth_file, sep='\t')
            del truth['Rating']
            truth_dict = {row["Id"]: row["Class"] for index,row in truth.iterrows()}
            accuracy_score = compute_accuracy(submission_answer_dict, truth_dict)
            ranking_score = 0 
        
        elif "ranking_answers.tsv" in files_in_submit_dir_ranking: 
            submission_answer_file = os.path.join(submit_dir, "ranking", "ranking_answers.tsv")
            sys.stdout.write("participation in ranking")
            ranking_score = score_ranking_task(submission_answer_file, truth_file)
            accuracy_score = 0 

        else: 
            raise ValueError("Submitted file should be classification/classification_answers.tsv or ranking/ranking_answers.tsv. Files in classification {0} and in ranking folder are {1}".format(files_in_submit_dir_classification, files_in_submit_dir_ranking)) 
            

        output_file.write("ranking_score:{:.3f}\n".format(ranking_score))
        output_file.write("accuracy_score:{:.3f}\n".format(accuracy_score))
        output_file.close()

if __name__ == "__main__":
    main()
