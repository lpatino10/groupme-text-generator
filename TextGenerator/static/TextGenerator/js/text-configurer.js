var person = null;
var tokenType = null;
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
$('#generate-button').click(function () {
    if (person != null && tokenType != null) {
        var data = JSON.stringify({ 'person': person, 'tokenType': tokenType });
        var reponse = $.post(window.location.href, data);
        reponse.done(function (data) {
            $('#message').text(data.message);
        });
    }
});
