import numpy as np

class cosine():

    @staticmethod
    def similarity(v_a, v_b):
        dot = np.dot(v_a, v_b)
        norm_a = np.linalg.norm(v_a)
        norm_b = np.linalg.norm(v_b)
        return dot/ (norm_a * norm_b)