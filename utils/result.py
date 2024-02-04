from simhash import Simhash
import re
from collections import defaultdict

class Results:
    def __init__(self):
        # self.unique_urls = 0
        self.visited_urls = set()
        self.max_words_per_page = 0
        self.common_words = defaultdict(int)
        self.subdomains = defaultdict(int)
        self.stop_words = self.initialize_stop_words()
        self.simhash_values_SET = set()
        self.simhash_values_LIST = []

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

    def handle_simhash(self, simhash):
        if not self.is_similar_simhash(simhash):
            self.simhash_values_SET.add(simhash.value)
            self.simhash_values_LIST.append(simhash)
            return True
        return False

    def add_word_to_common_count(self, word):
        if word not in self.stop_words:
            self.common_words[word] += 1
    
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