# main.py

import time
from logic.side_bar import *
from logic.powerbi import *

def main():
    st = Side()
    pw = Pwbi()

    st.header()
    st.footer()

    with st.st.spinner('Loading...'):
        start_time = time.time()
        data = st.side()
        if isinstance(data, pd.DataFrame) and not data.empty:
            pw.items = data
            pw.dashboard()
        else:
            print(type(data))
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time:.2f} seconds")

if __name__ == '__main__':
    main()