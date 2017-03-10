

def download_input(base_url):
	base_url = build_base_url(contest_id)
	PROBLEM_IDS =retrive_problem_ids(base_url)
	TOKEN = retrive_token(contest_id)
	download_all_input(contest_id, get_PROBLEM(), get_SIZE(), PROBLEM_IDS,TOKEN)


def download_solution(base_url):
	base_url = build_base_url(contest_id)
	problem_ids = retrive_problem_ids(base_url)
	download_all_pages(base_url,problem_ids,contest_id)
