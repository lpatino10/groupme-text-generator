# groupme-text-generator

## About
This project generates text based on a GroupMe chat I've had with my best friends for a few years. Text can be generated using training text from an indivual group member or from the full chat history, and it can be generated on a word-by-word or character-by-character basis.

## Demo
![Demo](https://cloud.githubusercontent.com/assets/8710772/25773371/3660a70c-324a-11e7-99d1-c51753bb72cd.gif)
[Try it yourself!](http://groupme-text-generator.herokuapp.com/)

## How it Works
Text is generated using a trigram language model, with the trigram probabilities estimated using the maximum likelihood estimate (MLE).

To explain further, the trigram model is a specific case of n-gram language models, where n is the number of consecutive tokens said to be correlated. As an example, using a trigram model, we can make the following simplification to a sentence probability (where &lt;s&gt; is a special token before the sentence):

&nbsp;&nbsp;&nbsp;&nbsp;**Original probability:**

&nbsp;&nbsp;&nbsp;&nbsp;P("the dog is very cute") = P("the") x P("dog"|"the") x P("is"|"the dog") x P("very"|"the dog is") x
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;P("cute"|"the dog is very")

&nbsp;&nbsp;&nbsp;&nbsp;**Trigram probability:**

&nbsp;&nbsp;&nbsp;&nbsp;P("the dog is very cute") = P("the"|"&lt;s&gt; &lt;s&gt;") x P("dog"|"&lt;s&gt; the") x P("is"|"the dog") x P("very"|"dog is") x &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;P("cute"|"is very")

More information about trigram and other n-gram language models can be found [here](https://en.wikipedia.org/wiki/N-gram).

The simplest way to find a specific trigram probability is by using MLE, which is basically a division of counts. An example using the trigram "the dog is" is shown below:

&nbsp;&nbsp;&nbsp;&nbsp;P("the dog is") = C("the dog is") / C("the dog")

where C stands for the count of its parameter. Essentially, each trigram probability is derived by counting up the amount of times it appears and then dividing my the number of times the first two tokens in said probability appears.

Once all trigram probabilities have been calculated for a corpus, text generation can begin. Sentences start with a token randomly chosen from a set of all tokens which started sentences in the training corpus. To generate the next token, we first narrow the possible set by selecting trigrams which start with the same first two tokens that the preceding trigram ended with (e.g., "that is cool" could be followed by "is cool that"). Once that set of probable continuations is calculated, it's chosen at random, but weighted according to each trigram's probability, using [NumPy's random.choice function](https://docs.scipy.org/doc/numpy/reference/generated/numpy.random.choice.html).

This process continues until a trigram is chosen which ends in an ending tag, specifying that it was used to end a sentence in the training corpus.
