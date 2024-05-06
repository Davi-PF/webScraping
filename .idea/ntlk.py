import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk.tokenize import word_tokenize
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Certifique-se de que os recursos necessários estão disponíveis
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('rslp')
nltk.download('vader_lexicon')  # Baixar o léxico VADER

# Definindo as stopwords em português
stop_words = set(stopwords.words('portuguese'))
stemmer = RSLPStemmer()

# Função para extrair características dos textos
def extract_features(document):
    words = word_tokenize(document)
    words = [stemmer.stem(word.lower()) for word in words if word.isalpha() and word not in stop_words]
    return {word: True for word in words}

# Lendo o arquivo CSV e preparando o dataset
data = []
df = pd.read_csv('ratings.csv', names=['comment'], encoding='utf-8')  # Lendo o CSV e renomeando a coluna para 'comment'

# Carregar o modelo pré-treinado e o tokenizador
tokenizer = BertTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased')
model = BertForSequenceClassification.from_pretrained('neuralmind/bert-base-portuguese-cased', num_labels=3)  # 3 labels: positivo, negativo, neutro

# Função para classificar o sentimento
def classify_sentiment(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    if predicted_class == 0:
        return 'negative'
    elif predicted_class == 1:
        return 'neutral'
    else:
        return 'positive'

for text in df['comment']:  # Iterando sobre os comentários
    if isinstance(text, str):  # Verificando se o comentário é uma string
        sentiment_label = classify_sentiment(text)
        data.append((text.strip(), sentiment_label))

# Criando um novo DataFrame com os dados de positivo, negativo e neutro
new_df = pd.DataFrame(data, columns=['comment', 'sentiment'])
new_df.to_csv('sentiment_analysis.csv', index=False)  # Salvando o DataFrame como um novo arquivo CSV

# Exibindo os valores no console
print("Quantidade de sentimentos positivos:", new_df[new_df['sentiment'] == 'positive'].shape[0])
print("Quantidade de sentimentos neutros:", new_df[new_df['sentiment'] == 'neutral'].shape[0])
print("Quantidade de sentimentos negativos:", new_df[new_df['sentiment'] == 'negative'].shape[0])
