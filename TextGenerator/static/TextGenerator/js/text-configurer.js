var person = null;
var tokenType = null;
var nGram = 0;
var nGramListIndices = {};
var personChoices = document.getElementById('person-dropdown').getElementsByClassName('text-center');
for (var i = 0; i < personChoices.length; i++) {
    personChoices[i].addEventListener('click', function () {
        var personChoice = this.innerHTML;
        document.getElementById('person-choice').innerHTML = personChoice + ' <span class="caret"></span>';
        person = personChoice;
    });
}
var tokenTypeChoices = document.getElementById('token-type-dropdown').getElementsByClassName('text-center');
for (var i = 0; i < tokenTypeChoices.length; i++) {
    tokenTypeChoices[i].addEventListener('click', function () {
        var tokenTypeChoice = this.innerHTML;
        document.getElementById('token-type-choice').innerHTML = tokenTypeChoice + ' <span class="caret"></span>';
        tokenType = tokenTypeChoice;
    });
}
var nGramChoices = document.getElementById('n-gram-dropdown').getElementsByClassName('text-center');
for (var i = 0; i < nGramChoices.length; i++) {
    nGramListIndices[nGramChoices[i].innerHTML] = i + 1;
    nGramChoices[i].addEventListener('click', function () {
        var nGramChoiceLabel = this.innerHTML;
        var nGramChoiceIndex = nGramListIndices[nGramChoiceLabel];
        document.getElementById('n-gram-choice').innerHTML = nGramChoiceLabel + ' <span class="caret"></span>';
        nGram = nGramChoiceIndex;
    });
}
var messageElement = document.getElementById('message');
var loaderElement = document.getElementById('loader');
document.getElementById('generate-button').addEventListener('click', function () {
    console.log(person);
    console.log(tokenType);
    console.log(nGram);
    if (person !== null && tokenType !== null && nGram > 0) {
        console.log('readying request...');
        messageElement.style.display = 'none';
        loaderElement.style.display = '';
        var data = JSON.stringify({ 'person': person, 'tokenType': tokenType, 'nGram': nGram });
        axios.post(window.location.href, data)
            .then(function (res) {
            loaderElement.style.display = 'none';
            messageElement.style.display = '';
            messageElement.innerHTML = res.data.message;
        });
    }
});
