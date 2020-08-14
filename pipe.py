def softmax(x):
    #создадим вероятностное распределение 
    proba = np.exp(-x)
    return proba/sum(proba)
class NeighborSampler(BaseEstimator):
    #класс для случайного выбора одного из ближайших соседей
    def __init__(self, k=12, temperature=1.0):
        self.k = k
        self.temperature = temperature
    def fit(self, X, y):
        self.tree_ = BallTree(X)
        self.y_ = np.array(y)
    def predict(self, X, random_state=None):
        distances, indices = self.tree_.query(X, return_distance=True, k=self.k)
        result = []
        for distance, index in zip(distances, indices):
            result.append(np.random.choice(index, p=softmax(distance*self.temperature)))
        return self.y_[result]
from sklearn.pipeline import make_pipeline
ns = NeighborSampler()
ns.fit(matrix_small, df.iloc[:,0])
pipe = make_pipeline(vectorizer, svd, ns)  
