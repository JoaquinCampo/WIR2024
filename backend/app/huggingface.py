from transformers import AutoTokenizer, TFAutoModelForSequenceClassification, pipeline
import tensorflow as tf

def analyse_sentiment(entity, posts):
    """
    Analyzes the sentiment of posts by classifying them using a pre-trained sentiment analysis model.

    Args:
        entity (str): The entity to compare the posts against.
        posts (list): A list of dictionaries representing the posts to analyze. Each dictionary should have 'title' and 'text' keys.

    Returns:
        list: A list of dictionaries representing the analyzed posts. Each dictionary will have 'title', 'text', 'sentiment', and 'score' keys.
    """
    # Ensure TensorFlow uses the GPU if available
    physical_devices = tf.config.list_physical_devices('GPU')
    for device in physical_devices:
        tf.config.experimental.set_memory_growth(device, True)
    if len(physical_devices) > 0:
        print(f"Using GPU(s): {physical_devices}")
    else:
        print("No GPU found, using CPU.")

    model_name = 'yangheng/deberta-v3-base-absa-v1.1'
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = TFAutoModelForSequenceClassification.from_pretrained(model_name)
    classifier = pipeline('text-classification', model=model, tokenizer=tokenizer, device=0 if len(physical_devices) > 0 else -1)

    results = []

    phrases = [post['comment'] for post in posts]


    batch_size = 4
    for i in range(0, len(phrases), batch_size):
        batch_phrases = phrases[i:i + batch_size]
        evaluations = classifier(batch_phrases, text_pair=entity)

        for j, evaluation in enumerate(evaluations):
            posts[i + j]['sentiment'] = evaluation['label']
            posts[i + j]['score'] = evaluation['score']
            results.append(posts[i + j])
            print(evaluation)

    return results
