import ast
import pandas as pd
import numpy as np


def read_parquet(path : str):
        print("Reading parquet")
        df = pd.read_parquet(path,engine='pyarrow')

        # get description and image url as payload
        payload = df[['description', 'image', 'vector']]
        payloads = payload.to_dict(orient='records')
        payloads_updated = []
        print(len(payloads))
        for i in range(len(payloads)):
            vector_byte = payloads[i]['vector']
            vector_list = ast.literal_eval(vector_byte.decode('utf-8'))
            vector_np = np.array(vector_list).tolist()
            payloads_updated.append({'vectors': vector_np, 'payload': {
                'description': payloads[i]['description'], 'image': payloads[i]['image'], }})
        return payloads_updated

def get_embeddings(model, query):
    embeddings = model.encode(query)
    return embeddings
