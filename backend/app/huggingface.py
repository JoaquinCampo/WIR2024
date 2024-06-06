from transformers import AutoTokenizer, TFAutoModelForSequenceClassification, pipeline

def analyse_sentiment(entity, posts):
   """
   Analyzes the sentiment of posts by classifying them using a pre-trained sentiment analysis model.

   Args:
      entity (str): The entity to compare the posts against.
      posts (list): A list of dictionaries representing the posts to analyze. Each dictionary should have 'title' and 'text' keys.

   Returns:
      list: A list of dictionaries representing the analyzed posts. Each dictionary will have 'title', 'text', 'sentiment', and 'score' keys.
   """
   model_name = 'yangheng/deberta-v3-base-absa-v1.1'
   tokenizer = AutoTokenizer.from_pretrained(model_name)
   model = TFAutoModelForSequenceClassification.from_pretrained(model_name)
   classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)

   results = []

   for post in posts:
      phrase = post['title'] + ' ' + post['text']
      evaluation = classifier(phrase,  text_pair=entity)

      post['sentiment'] = evaluation[0]['label']
      post['score'] = evaluation[0]['score']

      results.append(post)
      print(evaluation[0])

   return results