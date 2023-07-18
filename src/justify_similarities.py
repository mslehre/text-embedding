import os

from ask_question import get_answer
from settings import DATA_DIR

def ask_about_fit(id_list: list, text_dir: str, q_index = 0, seperator_list: list = None) -> str:
    """For a pair of similar texts, answers the question why these person pairs are a good fit.

    Args:
        text_list (list): List of the names of the two documents to compare
        text_dir (str): Documents directory
        q_index (int): Number indicating which question should be asked
        seperator_list (list): List of strings to insert as seperators in between the text chunks.

    Returns:
        Answer generated by the LLM
    """

    if (len(id_list) != 2):
        print("The number of texts given should be two.")
        return None

    #List of potential questions to ask, can be adjusted/extended latet. The first item is the default
    questions = ["What topics could these researchers collaborate on?", 
    "What are common study areas of these researchers?",
    "What could be possible projects for these researchers to collaborate on?"]

    if (q_index not in range(len(questions))):
        print("Number given for q_index must be between 0 and " + str(len(questions)-1))
        return None
    else:
        question = questions[q_index] + " Please keep your answer short and concise, make only 5 suggestions."

    answer = get_answer(question, text_dir, id_list)
    return answer

def main():
    id_list = ["76", "86"]
    testdir = os.path.join(DATA_DIR, "publications")
    test_seps = ["researcher 1:", "researcher 2:"]
    this_result = ask_about_fit(id_list, testdir, 2, test_seps)
    print(this_result)

if __name__ == "__main__":
    main()