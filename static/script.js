function show(element) {
    document.getElementById('dias').innerHTML = element.getAttribute('name');

    setTimeout(function () {
        document.getElementById('dias').innerHTML = '';
    }, 5000);
}