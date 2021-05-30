
import tensorflow as tf
import pandas as pd

from transformers import BertTokenizer, TFBertForSequenceClassification
from transformers import InputExample, InputFeatures

devices = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(devices[0], True)

model = TFBertForSequenceClassification.from_pretrained("bert-base-uncased")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

model.load_weights("./movie_reviews.h5")

pred_sentences = [
                  'The near future, a time when both hope and hardships drive humanity to look to the stars and beyond.',
                  'While a mysterious phenomenon menaces to destroy life on planet Earth, astronaut Roy McBride undertakes a mission across the immensity of space and its many perils to uncover the truth about a lost expedition that decades before boldly faced emptiness and silence in search of the unknown.',
                  'Harley Quinn joins forces with a singer, an assassin and a police detective to help a young girl who had a hit placed on her after she stole a rare diamond from a crime lord.',
                  "After he and his wife are murdered, marine Ray Garrison is resurrected by a team of scientists.",
                  "Enhanced with nanotechnology, he becomes a superhuman, biotech killing machine—'Bloodshot'.",
                  "As Ray first trains with fellow super-soldiers, he cannot recall anything from his former life.",
                  "But when his memories flood back and he remembers the man that killed both him and his wife, he breaks out of the facility to get revenge, only to discover that there's more to the conspiracy than he thought.",
                  "Armed with the astonishing ability to shrink in scale but increase in strength, master thief Scott Lang must embrace his inner-hero and help his mentor, Doctor Hank Pym, protect the secret behind his spectacular Ant-Man suit from a new generation of towering threats.",
                  "Against seemingly insurmountable obstacles, Pym and Lang must plan and pull off a heist that will save the world.",
                  "In 1800s England, a well-meaning but selfish young woman meddles in the love lives of her friends."]
tf_batch = tokenizer(pred_sentences, max_length=128, padding=True, truncation=True, return_tensors='tf')
tf_outputs = model(tf_batch)
tf_predictions = tf.nn.softmax(tf_outputs[0], axis=-1)
labels = ['Negative','Positive']
label = tf.argmax(tf_predictions, axis=1)
label = label.numpy()
for i in range(len(pred_sentences)):
  print(pred_sentences[i], ": \n", labels[label[i]])
