import time
import numpy as np
from typing import List, Optional

import threading
import pandas as pd
import requests
import plotly.express as px

def generate_data() -> List[int]:
    """Generate some random data."""
    return np.random.randint(100, 10000, 1000).tolist()

def process1(data: List[int]) -> List[int]:
    """TODO: Document this function. What does it do? What are the inputs and outputs?"""
    # The input is a list of randomly generated data and the output is also a list of data
    # 
    def foo(x):
        """Find the next largest prime number."""
        while True:
            x += 1
            if all(x % i for i in range(2, x)):
                return x
    return [foo(x) for x in data]

def process2(data: List[int]) -> List[int]:
    """TODO: Document this function. What does it do? What are the inputs and outputs?"""
    # The input is a list of randomly generated data and the output is also a list of data
    def foo(x):
        """Find the next largest prime number."""
        while True:
            x += 1
            if int(np.sqrt(x)) ** 2 == x:
                return x
    return [foo(x) for x in data]

def final_process(data1: List[int], data2: List[int]) -> List[int]:
    """TODO: Document this function. What does it do? What are the inputs and outputs?"""
    # The inputs are two different lists containing data and the output is a list
    return np.mean([x - y for x, y in zip(data1, data2)])

offload_url = 'http://172.20.10.2:5000' # TODO: Change this to the IP address of your server

def run(offload: Optional[str] = None) -> float:
    """Run the program, offloading the specified function(s) to the server.
    
    Args:
        offload: Which function(s) to offload to the server. Can be None, 'process1', 'process2', or 'both'.

    Returns:
        float: the final result of the program.
    """
    data = generate_data()
    if offload is None: # in this case, we run the program locally
        data1 = process1(data)
        data2 = process2(data)
    elif offload == 'process1':
        data1 = None
        def offload_process1(data):
            nonlocal data1
            # TODO: Send a POST request to the server with the input data
            data1 = response.json()
            post_request = requests.post(offload_url,data1)

        thread = threading.Thread(target=offload_process1, args=(data,))
        thread.start()
        data2 = process2(data)
        thread.join()
        # Question 2: Why do we need to join the thread here?
        # Question 3: Are the processing functions executing in parallel or just concurrently? What is the difference?
        #   See this article: https://oxylabs.io/blog/concurrency-vs-parallelism
        #   ChatGPT is also good at explaining the difference between parallel and concurrent execution!
        #   Make sure to cite any sources you use to answer this question.
    elif offload == 'process2':
        # TODO: Implement this case
        data2 = None
        def offload_process2(data):
            nonlocal data2
            # TODO: Send a POST request to the server with the input data
            data2 = response.json()
            post_request = requests.post(offload_url,data2)

        thread = threading.Thread(target=offload_process2, args=(data,))
        thread.start()
        data1 = process1(data)
        thread.join()
        pass
    elif offload == 'both':
        # TODO: Implement this case
        data1 = None
        data2 = None
        def offload_process1(data):
            nonlocal data1
            # TODO: Send a POST request to the server with the input data
            data1 = response.json()
            post_request = requests.post(offload_url,data1)

        def offload_process2(data):
            nonlocal data2
            # TODO: Send a POST request to the server with the input data
            data1 = response.json()
            post_request = requests.post(offload_url,data2)

        thread1 = threading.Thread(target=offload_process1, args=(data,))
        thread1.start()
        thread1.join()

        thread2 = threading.Thread(target=offload_process2, args=(data,))
        thread2.start()
        thread.join()

        pass

    ans = final_process(data1, data2)
    return ans 

def main():
    # TODO: Run the program 5 times for each offloading mode, and record the total execution time
    #   Compute the mean and standard deviation of the execution times
    #   Hint: store the results in a pandas DataFrame, use previous labs as a reference

    modes = [None, 'process1', 'process2', 'both']
    data = []

    for i in (5):
        time_list = []
        
        for n in modes:
            start = time.time()
            run(n)
            end = time.time
            time_list.append(end - time)

        data_mean = np.mean(time_list)
        data_std = np.std(time_list)
        data.append(modes, data_mean, data_std)

    df = pd.DataFrame(data, columns=['mode', 'data_mean', 'data_std'])


    fig = px.bar(df, x='mode', y='data_mean', error_y='data_std')
    fig.show()
    # Question 8: Why is it important to plot the error bars? What do they tell us?

    # write the plot to a file - make sure to commit the PNG file to your repository along with your code
    fig.write_image("makespan.png")
            



        


    # TODO: Plot makespans (total execution time) as a bar chart with error bars
    # Make sure to include a title and x and y labels


    # TODO: save plot to "makespan.png"


    # Question 4: What is the best offloading mode? Why do you think that is?
    # Question 5: What is the worst offloading mode? Why do you think that is?
    # Question 6: The processing functions in the example aren't very likely to be used in a real-world application. 
    #   What kind of processing functions would be more likely to be used in a real-world application?
    #   When would you want to offload these functions to a server?
    
    
if __name__ == '__main__':
    main()