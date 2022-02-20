import os

# creating directory to store links to crawl and crawled
def create_project_directory(directory):
        if not os.path.exists(directory):
            print("Creating directory" + directory)
            os.makedirs(directory)

# create urls_to_crawl and crawled files
def create_data_files(project_name, base_url):
    urls_to_crawl = project_name + '/urls_to_crawl.txt'
    crawled = project_name + '/crawled.txt'
    if not os.path.isfile(urls_to_crawl):
        write_file(urls_to_crawl, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')

# create a new file
def write_file(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    f = open(path, 'w')
    f.write(data)
    f.close()

# add data to en existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')

# Delete the content of a file
def delete_file_contents(path):
    with open(path, 'w'):
        pass

# Read a file and convert each file into a set
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results

# iterate through a set, each item will be a new line in the file
def set_to_file(links, file):
    delete_file_contents(file)
    for link in sorted(links):
        append_to_file(file, link)

