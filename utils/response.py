import pickle

class Response(object):
    def __init__(self, resp_dict):
        self.url = resp_dict["url"]
        self.status = resp_dict["status"]
        self.error = resp_dict["error"] if "error" in resp_dict else None
        print("")
        try:
            self.raw_response = (
                pickle.loads(resp_dict["response"])
                if "response" in resp_dict else
                None)
            if self.raw_response:
                print(len(self.raw_response.content))
            if not self.raw_response or len(self.raw_response.content) > 50000:
                self.raw_response = None
        except TypeError:
            self.raw_response = None
