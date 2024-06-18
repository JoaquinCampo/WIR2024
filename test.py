import requests

statistics = {
  "Politician": "Donald Trump",
  "stats": [
    {
      "Date": "20240617",
      "Reputation": 0.0647391319093907
    },
    {
      "Date": "20240616",
      "Reputation": 0.126446874438897
    },
    {
      "Date": "20240615",
      "Reputation": 0.0929965351904172
    },
    {
      "Date": "20240614",
      "Reputation": 0.139685146555011
    },
    {
      "Date": "20240613",
      "Reputation": 0.0928796840232533
    },
    {
      "Date": "20240612",
      "Reputation": 0.171563666596684
    },
    {
      "Date": "20240611",
      "Reputation": 0.139682325955787
    },
    {
      "Date": "20240610",
      "Reputation": 0.157381714585067
    }
  ],
  "min": {
    "related_entity": "Donald Trump",
    "id": "1de9brx",
    "name": "1de9brx",
    "title": "Donald Trump says Ken Paxton would be a good choice for U.S. attorney general. I’ve been reporting on Paxton for 10 years and have exposed allegations of bribery, self-dealing and more. I’m investigative reporter Lauren McGaughy. AMA!",
    "text": "If he wins the White House back, [Donald Trump said he’d consider Ken Paxton](https://www.houstonpublicmedia.org/articles/news/politics/2024/05/20/487975/donald-trump-says-hed-consider-ken-paxton-for-u-s-attorney-general/) for a top job in his administration. Paxton is a Republican who’s been Texas attorney general since 2015. You might best know him as the [guy who got impeached](https://www.kut.org/politics/2023-09-16/texas-senate-acquits-state-attorney-general-ken-paxton-in-impeachment-trial) last year for alleged corruption. He ended up [being acquitted of those charges](https://www.kut.org/politics/2023-09-16/texas-senate-acquits-state-attorney-general-ken-paxton-in-impeachment-trial), but his legal troubles are not behind him.\n\nI recently broke the news that the [FBI continued to investigate Paxton](https://www.kut.org/2024-05-23/donald-trump-fbi-investigation-texas-attorney-general-ken-paxton-grand-jury) after he beat impeachment. I also got my hands on some [federal grand jury documents](https://www.documentcloud.org/documents/24679686-house-board-of-managers-exhibit-540) that lay out the scope of the investigation. [These records are sealed](https://www.kut.org/2024-05-23/donald-trump-fbi-investigation-texas-attorney-general-ken-paxton-grand-jury). But I got them through scouring thousands of pages of never-before-published impeachment trial records.\n\nPaxton says all of this has been part of a [massive witch hunt](https://x.com/KenPaxtonTX/status/1748269090236473540?lang=en). If he’s not indicted, Paxton could become one of the most powerful politicians in the country. I’ve covered [Paxton for a decade](https://twitter.com/lmcgaughy) at two Texas newspapers and now for [The Texas Newsroom](https://www.kut.org/people/lauren-mcgaughy), a statewide collaboration of public radio stations here. Over the years, I’ve broken stories about allegations of [bribery](https://www.dallasnews.com/news/politics/2017/10/27/kaufman-county-da-closes-bribery-investigation-into-texas-ag-ken-paxton/), [insider deals](https://www.dallasnews.com/news/politics/2016/03/23/collin-county-grand-jury-ends-investigation-into-texas-ag-ken-paxton-s-role-in-land-deal/), [ethical lapses](https://www.kut.org/politics/2023-12-07/ken-paxton-texas-attorney-general-personal-finance-reports) and [even infidelity](https://www.dallasnews.com/news/investigations/2020/11/05/deposition-reveals-new-links-between-texas-attorney-general-ken-paxton-and-developer-nate-paul/). I know way too much about this man. So, ask me anything!\n\nFollow me on [X (formerly Twitter)](https://twitter.com/lmcgaughy), [Instagram](https://www.instagram.com/laurenmcgaughy/), [Facebook](https://www.facebook.com/laurenrmcgaughy) and [LinkedIn](https://www.linkedin.com/in/lauren-mcgaughy/)!\n\n[PROOF!](https://imgur.com/a/Lq7kand)\n\nEDIT: That's all for now. Thanks for your questions! I'll be checking in for new questions I haven't answered in case you missed the AMA! If you'd like to keep in touch, my social handles are linked above. If you want us to dig into something, email tips@KUT.org. ",
    "date": "20240612",
    "thumbsup": 2,
    "link": "reddit.com/r/politics/comments/1de9brx/donald_trump_says_ken_paxton_would_be_a_good/l8c4t0w/",
    "subreddit": "r/politics",
    "comment": "As a Texan, I'm sorry America. He is truly awful and fits right in with the dictator party.",
    "sentiment": "Negative",
    "score": 0.995901525020599
  },
  "neutral": {
    "related_entity": "Donald Trump",
    "id": "1dgp93e",
    "name": "1dgp93e",
    "title": "Donald Trump gets to sidestep the consequences of his conviction. Most people with criminal records don’t",
    "text": "No text available",
    "date": "20240615",
    "thumbsup": 175,
    "link": "reddit.com/r/politics/comments/1dgp93e/donald_trump_gets_to_sidestep_the_consequences_of/l8rn6zm/",
    "subreddit": "r/politics",
    "comment": "&gt; Donald Trump gets to\n\nStory of his entire life.",
    "sentiment": "Neutral",
    "score": 0.994945466518402
  },
  "max": {
    "related_entity": "Donald Trump",
    "id": "1dey9um",
    "name": "1dey9um",
    "title": "Donald Trump Gets Worst Poll Yet in State He Has Always Won",
    "text": "No text available",
    "date": "20240614",
    "thumbsup": 1,
    "link": "reddit.com/r/politics/comments/1dey9um/donald_trump_gets_worst_poll_yet_in_state_he_has/l8jbw7z/",
    "subreddit": "r/politics",
    "comment": "Forget the polls. VOTE! Please …",
    "sentiment": "Positive",
    "score": 0.97130411863327
  },
  "max_reputation": {
    "Date": "20240612",
    "Reputation": 0.171563666596684
  },
  "average_reputation": 0.123171884906813
}

api_key = "sk-proj-z6rWKgWBEbggbLhwhRKZT3BlbkFJ6sLN8xRemfw8SuvMIRRo"
endpoint = "https://api.openai.com/v1/chat/completions"

prompt = f"Contexto: Tengo un conjunto de datos que incluye la reputación diaria de un politico de estados unidos en un formato específico. Los datos están organizados de la siguiente manera: Politician: El nombre del político (en este caso, 'Donald Trump'). stats: Una lista de objetos que contienen la fecha y la reputación de Trump en esa fecha. min: Información del evento con la reputación mínima. neutral: Información del evento con la reputación neutral. max: Información del evento con la reputación máxima. max_reputation: La fecha y reputación más alta. average_reputation: La reputación promedio. Crea una frase dando un overview de los datos. Esta frase sera leida por millones de usuarios, por lo que tiene que ser simple y capturar la escencia de los datos sin dar demasiado detalle. Tu respuesta debe incluir un breve analisis de los datos, y al final la frase entre corchetes de esta forma ['frase' \n 'comentario personal']. Estos son los datos: {statistics}, ten en cuenta que los datos representan un porcentaje, es decir, 0.37 debes interpetarlo como 37%"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

send = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }


response = requests.post(endpoint, headers=headers, json=send)
print(response)
if response.status_code == 200:
    results = response.json()
    results['choices'][0]['message']['content']
    print(results['choices'][0]['message']['content'])
else:
    response.raise_for_status()