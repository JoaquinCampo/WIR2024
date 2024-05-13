from transformers import AutoTokenizer, TFAutoModelForSequenceClassification, pipeline

def analyse_sentiment(entity, phrases):
   model_name = 'yangheng/deberta-v3-base-absa-v1.1'
   tokenizer = AutoTokenizer.from_pretrained(model_name)
   model = TFAutoModelForSequenceClassification.from_pretrained(model_name)
   classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)

   results = []

   for phrase in phrases:
      evaluation = classifier(phrase,  text_pair=entity)
      results.append(evaluation[0])

   return results