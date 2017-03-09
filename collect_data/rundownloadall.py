
list_of_contest_ids = get_CONTEST_IDS()
numberofpages = 3030;

def build_base_table_url(base_url,contest_id)
	return base_url+'/do/?cmd=GetScoreboard&contest_id='+contest_id+'&show_type=all&start_pos='


def download_all():
	for contest_id in list_of_contest_ids:
		list_of_problem_ids = get_list_of_problems(contest_id):
		download_input_mp(list_of_problem_ids,numberofpages)
		download_solutions_mp(list_of_problem_ids)
		download_table_data_mp(numberofpages)

def download_input_mp(list_of_problem_ids):
	pool = mp.Pool(processes = 6)
	results = pool.map(download_input,list_of_problem_ids)

def download_solutions_mp(list_of_contest_ids): 
	pool = mp.Pool(processes = 6)
	results = pool.map(download_solution,list_of_problem_ids)

def download_table_data_mp(numberofpages)
	pool = mp.Pool(processes=6)
	results = pool.map(download_table_data,range(1,numerofpages))

clean_home_dir()
download_all()
