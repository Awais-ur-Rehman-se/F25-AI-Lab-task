
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

passages = [
    'Reset a forgotten password using the recovery link.',
    'Submit assignments through the learning portal.',
    'Check ink levels when a printer produces blank pages.'
]

query = 'How can I recover my login?'

passage_vectors = model.encode(passages, normalize_embeddings=True)

query_vector = model.encode(query, normalize_embeddings=True)

scores = passage_vectors @ query_vector

print('Query:', query)
print('Embedding shape:', passage_vectors.shape)

for i in np.argsort(-scores):
    print(f'{i}: similarity={scores[i]:.3f} | {passages[i]}')

print('All vectors are normalized:',
      np.allclose(np.linalg.norm(passage_vectors, axis=1), 1, atol=1e-5))

