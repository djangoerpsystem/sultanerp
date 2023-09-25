function filterCategory() {
    // https://www.w3schools.com/jsref/met_document_queryselector.asp
    const form = document.querySelector("form[action]");
    form.querySelector('input[name="action_type"]').value = "filter";
    form.submit();
}
    