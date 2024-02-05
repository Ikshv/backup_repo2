import os
from simhash import Simhash
import re
from collections import defaultdict
from utils import get_logger

class Results:
    def __init__(self):
        # self.unique_urls = 0
        self.visited_urls = set()
        self.max_words_per_page = 0
        self.max_words_per_page_url = ""
        self.common_words = defaultdict(int)
        self.subdomains = defaultdict(int)
        self.stop_words = self.initialize_stop_words()
        self.simhash_values_SET = set()
        self.simhash_values_LIST = []
        self.logger = get_logger("RESULTS")

    def is_similar_simhash(self, simhash):
        
        simhash_distance = 3

        if simhash.value in self.simhash_values_SET: # if simhash in set
            print("simhash in set")
            return True
        for simhash_value in self.simhash_values_LIST: # if simhash in list
            if simhash.distance(Simhash(simhash_value)) < simhash_distance: #
                return True
            # print(simhash.distance(Simhash(simhash_value)))
        return False
    
    def handle_max_words_per_page(self, url, num_words):
        if num_words > self.max_words_per_page:
            self.max_words_per_page = num_words
            self.max_words_per_page_url = url

    def handle_simhash(self, simhash):
        if not self.is_similar_simhash(simhash):
            self.simhash_values_SET.add(simhash.value)
            self.simhash_values_LIST.append(simhash)
            return True
        return False
    
    def add_to_visited(self, url):
        #split on fragment
        url = url.split('#')[0]
        self.visited_urls.add(url)

    def add_word_to_common_count(self, word):
        if word not in self.stop_words:
            self.common_words[word] += 1

    def get_most_common_words(self, n):
        return sorted(self.common_words.items(), key=lambda x: x[1], reverse=True)[:n]
    
    def add_subdomain(self, subdomain):
        pattern = r'^(?:http[s]*://)?([^:/\s]+)'
        match = re.search(pattern, subdomain)
        if match:
            self.subdomains[match.group(1)] += 1
        else:
            match = re.search(r'([^:/\s]+)', subdomain)
            self.subdomains[match.group(0)] += 1
        
    def initialize_stop_words(self):
        stop_words = set()
        with open("stop_words.txt", "r") as f:
            for line in f:
                stop_words.add(line.strip())
        return stop_words
    
    def log_results(self, url):
        self.logger.info(
            f"URL: {url} | "
            f"Visited URLs: {len(self.visited_urls)} | "
            f"Max words per page: {self.max_words_per_page} from URL {self.max_words_per_page_url} | "
            f"Common words: {self.get_most_common_words(50)} | "
            f"Subdomains: {self.subdomains.items()} | "
            )
        
    def write_to_file(self, filename):
        print("writing to file")
        with open(filename, "w") as f:
            f.write(
                f"{len(self.visited_urls)},{','.join(list(self.visited_urls))}\n" #comma-separated list of visited urls
                f"{self.max_words_per_page},{self.max_words_per_page_url}\n"
                f"{','.join([f'{word},{freq}' for (word,freq) in sorted(self.common_words.items(), key=lambda x: x[1], reverse=True)])}\n"
                f"{len(self.subdomains)},{','.join([f'{subdomain},{freq}' for (subdomain,freq) in self.subdomains.items()])}\n"
                # f"{','.join(self.simhash_values_LIST)}\n"
                f"{','.join([str(simhash_value) for simhash_value in self.simhash_values_SET])}\n"
            )

    def read_from_file(self, filename):
        print("reading from file")
        r = Results()
        if not filename or not os.path.exists(filename):
            return r
        with open(filename, "r") as f:
            visited_urls = f.readline().strip().split(',')
            r.visited_urls = set(visited_urls[1:])
            max_words_per_page = f.readline().strip().split(',')
            r.max_words_per_page = int(max_words_per_page[0])
            r.max_words_per_page_url = max_words_per_page[1]
            common_words = f.readline().strip().split(',')
            for i in range(0, len(common_words), 2):
                r.common_words[common_words[i]] = int(common_words[i+1])
            subdomains = f.readline().strip().split(',')
            for i in range(1, len(subdomains), 2):
                r.subdomains[subdomains[i]] = int(subdomains[i+1])
            simhash_values_set = f.readline().strip().split(',')
            for simhash_value in simhash_values_set:
                r.simhash_values_SET.add(simhash_value)
                r.simhash_values_LIST.append(Simhash(simhash_value))
        return r



if __name__ == "__main__":
    r = Results()
    r.add_subdomain("http://www.google.com")
    r.add_subdomain("http://testing.ics.uci.edu/rhee/vi")
    r.add_subdomain("http://testing.ics.uci.edu/blah/foo")
    
    print(r.subdomains.items())