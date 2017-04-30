var personDropdown: HTMLElement = document.getElementById('person-dropdown');
var tokenTypeDropdown: HTMLElement = document.getElementById('token-type-dropdown');

function getEventTarget(e) {
    e = e || window.event;
    return e.target || e.srcElement; 
}

function changeText(event, id: string) {
    var target = getEventTarget(event);
    var choice = document.getElementById(id);
    choice.innerHTML = target.innerHTML + ' <span class="caret"></span>';
}

personDropdown.onclick = function(event) {
    changeText(event, 'person-choice');
}

tokenTypeDropdown.onclick = function(event) {
    changeText(event, 'token-type-choice');
}