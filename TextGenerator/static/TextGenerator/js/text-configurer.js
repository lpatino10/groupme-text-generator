var person = null;
var tokenType = null;
var nGram = 0;
$('#person-dropdown li > a').click(function (e) {
    var personChoice = this.innerHTML;
    $('#person-choice').html(personChoice + ' <span class="caret"></span>');
    person = personChoice;
});
$('#token-type-dropdown li > a').click(function (e) {
    var tokenTypeChoice = this.innerHTML;
    $('#token-type-choice').html(tokenTypeChoice + ' <span class="caret"></span>');
    tokenType = tokenTypeChoice;
});
$('#n-gram-dropdown li > a').click(function (e) {
    var nGramChoiceLabel = this.innerHTML;
    var nGramChoiceIndex = $(this).closest('li').index() + 1;
    $('#n-gram-choice').html(nGramChoiceLabel + ' <span class="caret"></span>');
    nGram = nGramChoiceIndex;
});
$('#generate-button').click(function () {
    if (person != null && tokenType != null && nGram > 0) {
        $('#message').hide();
        $('#loader').show();
        var data = JSON.stringify({ 'person': person, 'tokenType': tokenType, 'nGram': nGram });
        var reponse = $.post(window.location.href, data);
        reponse.done(function (data) {
            $('#loader').hide();
            $('#message').show();
            $('#message').text(data.message);
        });
    }
});
