declare var axios: any;

var person = null;
var tokenType = null;
var nGram: number = 0;
var nGramListIndices: {[x: string]: any} = {};

var personChoices: NodeListOf<Element> = document.getElementById('person-dropdown').getElementsByClassName('text-center');
for (var i: number = 0; i < personChoices.length; i++) {
    personChoices[i].addEventListener('click', function() {
        var personChoice: string = this.innerHTML;
        document.getElementById('person-choice').innerHTML = personChoice + ' <span class="caret"></span>';
        person = personChoice;
    });
}

var tokenTypeChoices: NodeListOf<Element> = document.getElementById('token-type-dropdown').getElementsByClassName('text-center');
for (var i: number = 0; i < tokenTypeChoices.length; i++) {
    tokenTypeChoices[i].addEventListener('click', function() {
        var tokenTypeChoice: string = this.innerHTML;
        document.getElementById('token-type-choice').innerHTML = tokenTypeChoice + ' <span class="caret"></span>';
        tokenType = tokenTypeChoice;
    });
}

var nGramChoices: NodeListOf<Element> = document.getElementById('n-gram-dropdown').getElementsByClassName('text-center');
for (var i: number = 0; i < nGramChoices.length; i++) {
    nGramListIndices[nGramChoices[i].innerHTML] = i + 1;
    nGramChoices[i].addEventListener('click', function() {
        var nGramChoiceLabel: string = this.innerHTML;
        var nGramChoiceIndex: number = nGramListIndices[nGramChoiceLabel];
        document.getElementById('n-gram-choice').innerHTML = nGramChoiceLabel + ' <span class="caret"></span>';
        nGram = nGramChoiceIndex;
    });
}

var messageElement: HTMLElement = document.getElementById('message');
var loaderElement: HTMLElement = document.getElementById('loader');

document.getElementById('generate-button').addEventListener('click', function() {
    if (person !== null && tokenType !== null && nGram > 0) {
        messageElement.style.display = 'none';
        loaderElement.style.display = '';
        var data = JSON.stringify({ 'person': person, 'tokenType': tokenType, 'nGram': nGram });
        axios.post(window.location.href, data)
            .then(res => {
                loaderElement.style.display = 'none';
                messageElement.style.display = '';
                messageElement.innerHTML = res.data.message;
            });
    }
});