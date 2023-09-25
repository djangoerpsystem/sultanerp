function checkAmounts() {
    let pos = false;
    let neg = false;
    const amountInputs = document.querySelectorAll('input[type="number"]');
    for (let input of amountInputs) {
        const intValue = parseInt(input.value || "0");
    if (intValue < 0) {
            pos = true;
            break;
        } else if (intValue > 0) {
            neg = true;
        }
    }
    if (pos) {
        window.alert("The order can't have a negative amount!");
        return false;
    }
    if (!neg) {
        window.alert("The order needs at least one positive amount!");
        return false;
    }
    return true;
}
