import os
from spacetime import Node, Dataframe
from utils.pcc_models import Register

# Define a function to get the cache server information
def get_cache_server(config, restart, init_wrapper):
    try:
        # Create a Dataframe configuration
        dataframe_details = Dataframe(appname=config.host, server_port=config.port, types=[Register])
        # print(dataframe_details.details)
        
        # Initialize the Node with the wrapper function
        init_node = Node(target=init_wrapper, Types=[Register], dataframe=dataframe_details)
        
        # Start the node and wait for it to complete
        cache_server_info = init_node.start  # Use start_async if you want non-blocking behavior
        # print(f"Cache server information: {init_node.dataframe_details}")
        return cache_server_info
    except Exception as e:
        print(f"Error: {e}")
        raise e  # It's usually better to raise the exception after logging to ensure calling code can handle it